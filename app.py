import os
import time
import threading
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)
CORS(app)

# 🔑 የጌሚኒ ቁልፍ መውሰጃ
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# ⏰ ሰርቨሩ በፈለግከው ደቂቃ እንዲሰራ ራሱን በራሱ በየ 10 ደቂቃው የሚቀሰቅስ ፈንክሽን (Anti-Sleep)
def keep_alive():
    while True:
        try:
            # ራሱን በራሱ ፒንግ ያደርጋል
            requests.get("https://ozoneai.onrender.com/")
        except Exception:
            pass
        time.sleep(600) # በየ 10 ደቂቃው

# ሰርቨሩ ሲነሳ ይቺን በጀርባ ያስጀምራታል
threading.Thread(target=keep_alive, daemon=True).start()

@app.route('/')
def home():
    return "⚡️ OzoneAI Unrestricted Engine is Running Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received"}), 400
            
        user_message = data.get("message", "").strip()
        
        if not API_KEY:
            return jsonify({"reply": "⚠️ API Key አልተገኘም! እባክህ Render ላይ GEMINI_API_KEY አስገባ።"}), 500

        # 🧠 የጌሚኒ ሞዴል (Gemini 1.5 Flash)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # 🔓 0% ገደብ (ሙሉ በሙሉ ያልተገደበ ማድረጊያ ህግ)
        completely_unrestricted = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # 🚀 መልስ ማመንጨት
        response = model.generate_content(
            user_message,
            safety_settings=completely_unrestricted
        )

        return jsonify({"reply": response.text})
        
    except Exception as e:
        return jsonify({"reply": f"OzoneAI Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
