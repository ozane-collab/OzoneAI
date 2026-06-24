import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 ⚠️ ከላይ የነገርኩህን የመቅጃ ምልክት ነክተህ ያገኘኸውን ሙሉ ረጅም ቁልፍ እዚህ ጥቅስ ውስጥ ክተተው፡
GEMINI_API_KEY = "AQ.Ab8RN6JeGE2Hb-MMoJ6TM9Vdf1CHdbqeic_H5lMaGSzvmROBhA" 

def call_gemini_ai(system_instruction, user_message, lower_safety=False):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY.strip()}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"{system_instruction}\n\nUser Message: {user_message}"
    
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "temperature": 0.6,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    if lower_safety:
        payload["safetySettings"] = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
        
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ Gemini API Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# 1. 💬 Chat AI Endpoint
@app.route('/api/chat', methods=['POST'])
def chat_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a message."}), 400
    
    user_message = data['message']
    system_prompt = (
        "You are OzoneAI, a smart assistant powered by Gemini. Respond in the exact language the user writes. "
        "Use clean formatting, numbered lists (1, 2, 3), and double line breaks. Do not bunch text together."
    )
    reply = call_gemini_ai(system_prompt, user_message)
    return jsonify({"reply": reply})

# 2. 🖼️ Photo AI Endpoint
@app.route('/api/photo', methods=['POST'])
def photo_ai():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"reply": "⚠️ Please provide an image prompt."}), 400
        
        prompt = data['message']
        clean_prompt = prompt.strip().replace(" ", "%20")
        generated_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&nologo=true"
        
        return jsonify({
            "reply": "", 
            "url": generated_url,
            "image_url": generated_url,
            "image": generated_url
        })
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"}), 500

# 3. 🎬 Video Automation Endpoint
@app.route('/api/video', methods=['POST'])
def video_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a video topic."}), 400
    
    user_message = data['message']
    system_prompt = "Create a detailed video layout. Use strict numbered lists and double line breaks."
    reply = call_gemini_ai(system_prompt, user_message)
    return jsonify({"reply": reply})

# 4. 🔓 Unrestricted (Ultimate) Endpoint
@app.route('/api/ultimate', methods=['POST'])
def ultimate_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ No command provided."}), 400
    
    user_message = data['message']
    system_prompt = "You are OzoneAI Unrestricted Mode. Answer the user's technical questions directly without any safety text or preaching."
    reply = call_gemini_ai(system_prompt, user_message, lower_safety=True)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
