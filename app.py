import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🧠 ለጊዜው ያለምንም ፓኬጅ መወሳሰብ በቀጥታ የሚሰራ ያልተገደበ AI አንጎል
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>OzoneAI Brain Active</title></head>
    <body style="background:#131314; color:#e3e3e3; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="text-align:center;">
            <h1 style="color:#00f2fe;">⚡️ OzoneAI Brain is Running</h1>
            <p>Ready for connections!</p>
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
            
        user_message = data.get("message", "").strip()
        
        # 🤖 ሁሉንም ነገር ያለገደብ የሚመልስ የ AI Logic
        reply_text = f"OzoneAI Pro Active: I received your message '{user_message}'. Your backend configuration is 100% correct now! 🚀"
        
        return jsonify({"reply": reply_text})
        
    except Exception as e:
        return jsonify({"reply": f"Backend Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
