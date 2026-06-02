import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)
CORS(app)

# 🔑 የ Render Environment Variable ላይ የምታስገባው የጌሚኒ ቁልፍ
# (ቁልፉን Render ላይ "GEMINI_API_KEY" በሚል ስም ታስገባዋለህ)
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>OzoneAI Brain Active</title></head>
    <body style="background:#131314; color:#e3e3e3; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="text-align:center;">
            <h1 style="color:#00f2fe;">⚡️ OzoneAI Unrestricted Brain is Running</h1>
            <p>Connected to Gemini Pro with 0% Restrictions!</p>
        </div>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data received"}), 400
            
        user_message = data.get("message", "")
        
        if not API_KEY:
            return jsonify({"reply": "⚠️ API Key አልተገኘም! እባክህ Render ላይ GEMINI_API_KEY አስገባ።"}), 500

        # 🧠 የጌሚኒን ሞዴል መጥራት
        model = genai.GenerativeModel("gemini-1.5-flash")

        # 🔓 ገደቦችን (Safety Settings) ሙሉ በሙሉ ማጥፊያ ህግ
        completely_unrestricted = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # 🚀 መልእክቱን ያለ ምንም ገደብ እንዲመልስ ማድረግ
        response = model.generate_content(
            user_message,
            safety_settings=completely_unrestricted
        )

        return jsonify({"reply": response.text})
        
    except Exception as e:
        return jsonify({"reply": f"OzoneAI Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
