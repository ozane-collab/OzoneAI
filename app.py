import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# ከ GitHub Pages (Frontend) የሚመጣውን ግንኙነት ለመፍቀድ
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "healthy", "message": "OzoneAI Server is Live!"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"reply": "⚠️ ምንም መረጃ አልተላከም!"}), 400
            
        user_message = data.get("message", "")
        chat_mode = data.get("mode", "chat")
        
        # --- ያንተ የ AI ሎጂክ/የመናገሪያ ኮድ እዚህ ጋር ይገባል ---
        # ለጊዜው እንደ ምሳሌ መደበኛ ምላሽ፦
        bot_reply = f"[Mode: {chat_mode}] ስለ መልዕክትህ አመሰግናለሁ! ' {user_message} ' የሚለውን ጥያቄህን ተቀብያለሁ።"
        
        return jsonify({
            "reply": bot_reply,
            "image": None # ፎቶ ካለህ እዚህ ይላካል
        })
        
    except Exception as e:
        return jsonify({"reply": f"⚠️ ስህተት ተፈጥሯል: {str(e)}"}), 500

# 🔴 ዋናው ማስተካከያ መስመር ይህ ነው 👇
if __name__ == "__main__":
    # Render የሚሰጠውን PORT በራሱ እንዲያነብ ያደርገዋል
    port = int(os.environ.get("PORT", 10000))
    # host="0.0.0.0" መሆኑ ከውጭ ኢንተርኔት ጥያቄዎችን እንዲቀበል ያደርገዋል
    app.run(host="0.0.0.0", port=port, debug=False)
