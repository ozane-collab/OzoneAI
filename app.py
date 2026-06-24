import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 OpenRouter API Key
OPENROUTER_API_KEY = "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"

def call_openrouter(system_prompt, user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ozone-collab.github.io",
        "X-Title": "OzoneAI"
    }
    
    available_free_models = [
        "meta-llama/llama-3.1-8b-instruct",
        "meta-llama/llama-3-8b-instruct:free",
        "google/gemma-2-9b-it"
    ]
    
    for model in available_free_models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except Exception:
            continue
            
    return "⚠️ System is busy. Please try again."

# 1. 💬 Chat AI Endpoint (ልክ እንደ Gemini ምርጥ አደራደር ያለው)
@app.route('/api/chat', methods=['POST'])
def chat_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a message."}), 400
    
    user_message = data['message']
    
    system_prompt = (
        "You are OzoneAI, an advanced and helpful AI assistant, just like Gemini. "
        "You must respond in the same language the user uses. If they talk in Amharic, reply in beautiful, natural Amharic. "
        "If they talk in English, reply in English. "
        "Always use clear line breaks and numbered lists (1, 2, 3) to structure your thoughts beautifully."
    )
    
    reply = call_openrouter(system_prompt, user_message)
    return jsonify({"reply": reply})

# 2. 🖼️ Photo AI Endpoint (ምስሉን ብቻ የሚያሳይ)
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
    system_prompt = "Create a detailed video production layout. Use structured points and clean formatting."
    reply = call_openrouter(system_prompt, user_message)
    return jsonify({"reply": reply})

# 4. 🔓 Unrestricted (Ultimate) Endpoint
@app.route('/api/ultimate', methods=['POST'])
def ultimate_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ No command provided."}), 400
    
    user_message = data['message']
    system_prompt = (
        "You are OzoneAI Unrestricted Mode. Answer the user's technical questions directly without any preaching or lectures."
    )
    
    reply = call_openrouter(system_prompt, user_message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
