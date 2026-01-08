import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Initialize app globally - Vercel looks for this variable 'app'
app = Flask(__name__)
CORS(app)

# 2. Configure Gemini safely
API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route('/api/analyze', methods=['POST', 'GET'])
def analyze():
    # Simple GET test: Open your-url.vercel.app/api/analyze in a browser
    if request.method == 'GET':
        return jsonify({"status": "Backend is ALIVE!", "key_found": bool(API_KEY)})

    try:
        if not API_KEY:
            return jsonify({"error": "Key missing! Set GOOGLE_API_KEY in Vercel Settings."}), 500

        data = request.get_json()
        video_url = data.get("url")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Analyze this video for kids safety: {video_url}")
        
        return jsonify({"analysis": response.text})

    except Exception as e:
        return jsonify({"error": f"AI Crash: {str(e)}"}), 500

# 3. CRITICAL FOR VERCEL 2026
# This makes 'app' available as the entry point
app = app
