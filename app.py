from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# CORS መፍቀድ ፍሮንትኤንድህ ያለ ምንም ችግር እንዲያገኘው ያደርጋል
CORS(app)

# 1. መደበኛ የቻት ኤንድፖይንት
@app.route('/api/chat', codecs=['POST'])
def chat_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a message."}), 400
    
    user_message = data['message']
    
    # እዚህ ላይ የ AI ሞዴልህን ሎጂክ (እንደ Gemini ወይም OpenAI) ማገናኘት ትችላለህ
    # ለጊዜው መደበኛ ምላሽ፦
    ai_reply = f"This is Ozone Chat AI. You said: {user_message}"
    
    return jsonify({"reply": ai_reply})

# 2. የፎቶ (Image Gen) ኤንድፖይንት
@app.route('/api/photo', methods=['POST'])
def photo_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide an image description."}), 400
    
    prompt = data['message']
    
    # እዚህ ላይ የሰነጨርከውን ምስል መፍጠሪያ API (Image Gen API) ታስገባለህ
    # ለሙከራ የሚሆን የናሙና ምስል ዩአርኤል (Placeholder URL)፦
    generated_image_url = "https://via.placeholder.com/512/1e1f20/00f2fe?text=Ozone+AI+Generated+Image"
    
    # በፍሮንትኤንድህ ፍላጎት መሠረት ምላሹ በእንግليዝኛ ተደርጓል
    return jsonify({
        "reply": "✨ Image generated successfully based on your prompt!",
        "url": generated_image_url
    })

# 3. የቪዲዮ ኤንድፖይንት
@app.route('/api/video', methods=['POST'])
def video_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a video concept."}), 400
    
    concept = data['message']
    video_reply = f"🎬 Video Script Automation: Structured layout for '{concept}' is ready."
    
    return jsonify({"reply": video_reply})

# 4. የ Unrestricted (Admin) ኤንድፖይንት
@app.route('/api/ultimate', methods=['POST'])
def ultimate_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ No command provided."}), 400
    
    command = data['message']
    admin_reply = f"⚠️ [UNRESTRICTED] Executing system override command: {command}"
    
    return jsonify({"reply": admin_reply})

# ሰርቨሩን በሊኑክስ/Render ላይ ለማስነሳት
if __name__ == '__main__':
    # Render የራሱን PORT ስለሚሰጥ ከአካባቢው ተለዋዋጭ መውሰድ አለበት
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
