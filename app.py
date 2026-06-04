import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 🔐 የቪዲዮ/ፎቶ ወይም የቻት AI ቁልፍህን እዚህ አስገባ
# በ Render Dashboard -> Environment Variables ላይ ማሰር ትችላለህ
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "ያንተን_የገሚኒ_ኤፒአይ_ኪይ_እዚህ_አስገባ")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET", "HEAD"])
def home():
    return "OzoneAI Server is Live and Running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "⚠️ ምንም መረጃ አልተላከም!"}), 400
            
        user_message = data.get("message", "")
        chat_mode = data.get("mode", "chat")
        
        # 🤖 በተመረጠው Mode መሰረት የ AI ባህሪን መለወጥ
        system_instruction = "You are OzoneAI, a helpful assistant."
        if chat_mode == "photo":
            system_instruction = "You are OzoneAI Photo Expert. Help users with professional image prompts and design concepts."
        elif chat_mode == "video":
            system_instruction = "You are OzoneAI Video Expert. Help users write scripts, storyboards, and video automation guidelines."

        # የጀነሬቲቭ ሞዴል ጥሪ
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # እውነተኛ የ AI ምላሽ ማመንጨት
        response = model.generate_content(user_message)
        bot_reply = response.text
        
        return jsonify({
            "reply": bot_reply,
            "image": None
        })
        
    except Exception as e:
        return jsonify({"reply": f"⚠️ ስህተት ተፈጥሯል: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
