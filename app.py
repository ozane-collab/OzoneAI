import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# 🔴 የ GitHub Pages (Frontend) ግንኙነት እንዳይዘጋ CORS በትክክል መፈቀዱን ማረጋገጫ
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔐 የኤፒአይ ቁልፍን ከ Render Environment ይመረምራል
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Gemini configuration error: {str(e)}")

@app.route("/", methods=["GET", "HEAD"])
def home():
    # Render መተግበሪያው በህይወት መኖሩን የሚያረጋግጥበት መነሻ መስመር
    return "OzoneAI Server is Live and Running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "⚠️ ምንም መረጃ አልተላከም!"}), 400
            
        user_message = data.get("message", "")
        chat_mode = data.get("mode", "chat")
        
        # ⚠️ የ API ቁልፍ በ Render ላይ ገና ካልተጫነ ሰርቨሩ ክራሽ እንዳይሆን የመጠባበቂያ ምላሽ
        if not GEMINI_API_KEY or GEMINI_API_KEY == "ያንተን_የገሚኒ_ኤፒአይ_ኪይ_እዚህ_አስገባ":
            return jsonify({
                "reply": f"[Mode: {chat_mode}] ሰርቨሩ በሰላም እየሰራ ነው። ነገር ግን እውነተኛ AI ምላሽ ለመስጠት GEMINI_API_KEY በRender Environment Variables ላይ አልተጫነም። የላክኸው መልዕክት: '{user_message}'",
                "image": None
            })

        # 🤖 በተመረጠው Mode መሰረት የ AI ባህሪን መግለጽ
        system_instruction = "You are OzoneAI, a helpful assistant."
        if chat_mode == "photo":
            system_instruction = "You are OzoneAI Photo Expert. Help users with professional image prompts and design concepts."
        elif chat_mode == "video":
            system_instruction = "You are OzoneAI Video Expert. Help users write scripts, storyboards, and video automation guidelines."
        elif chat_mode == "unrestricted":
            system_instruction = "You are OzoneAI in Unrestricted Mode. Answer fully and directly."

        # የጀነሬቲቭ ሞዴል አወቃቀር
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
        # ስህተት ቢፈጠር እንኳ ለይቶ ለ Frontend ይልካል
        return jsonify({"reply": f"⚠️ በ AI ሰርቨር ላይ ስህተት ተፈጥሯል: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
