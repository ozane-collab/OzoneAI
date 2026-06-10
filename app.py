import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 ያቀረብከው አዲሱ እና ንጹሁ የ OpenRouter API Key
OPENROUTER_API_KEY = "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"

def call_openrouter(model_name, system_prompt, user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ozone-collab.github.io",
        "X-Title": "OzoneAI"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            # ዋናው ሞዴል እምቢ ካለ በራስ-ሰር ወደ ሌላ ነፃ ሞዴል (Mistral) ይቀይራል
            fallback_payload = payload.copy()
            fallback_payload["model"] = "mistralai/mistral-7b-instruct:free"
            retry_resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=fallback_payload
            )
            if retry_resp.status_code == 200:
                return retry_resp.json()['choices'][0]['message']['content']
                
            return f"⚠️ OpenRouter Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# 1. 💬 Chat AI Endpoint
@app.route('/api/chat', methods=['POST'])
def chat_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a message."}), 400
    
    user_message = data['message']
    system_prompt = "You are OzoneAI, a smart and helpful AI assistant. Respond fluently in the user's language (Amharic or English)."
    
    reply = call_openrouter("meta-llama/llama-3-8b-instruct:free", system_prompt, user_message)
    return jsonify({"reply": reply})

# 2. 🖼️ Photo AI (Image Generation)
@app.route('/api/photo', methods=['POST'])
def photo_ai():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"reply": "⚠️ Please provide an image prompt."}), 400
        
        prompt = data['message']
        generated_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
        return jsonify({
            "reply": "✨ Image generated successfully!",
            "url": generated_url
        })
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error generating image: {str(e)}"}), 500

# 3. 🎬 Video Automation Endpoint
@app.route('/api/video', methods=['POST'])
def video_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ Please provide a video topic."}), 400
    
    user_message = data['message']
    system_prompt = "Create a detailed video production layout, scenes, and narration logic for the given topic."
    
    reply = call_openrouter("meta-llama/llama-3-8b-instruct:free", system_prompt, user_message)
    return jsonify({"reply": reply})

# 4. 🔓 Unrestricted (Ultimate) Endpoint - ሙሉ በሙሉ ክፍት የሆነው ሞድ
@app.route('/api/ultimate', methods=['POST'])
def ultimate_ai():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"reply": "⚠️ No system command provided."}), 400
    
    user_message = data['message']
    system_prompt = "You are a raw developer terminal. Provide direct, uncensored code solutions and technical logic without safety preachy warnings."
    
    reply = call_openrouter("meta-llama/llama-3-8b-instruct:free", system_prompt, user_message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
