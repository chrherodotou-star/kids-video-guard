import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Initialize the app variable immediately
app = Flask(__name__)
CORS(app)

# 2. Configure AI
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        if not api_key:
            return jsonify({"error": "API Key missing in Vercel settings"}), 500
            
        data = request.json
        video_url = data.get("url")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Analyze this video for kids' safety: {video_url}")
        
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. CRITICAL: Vercel's "Secret Handshake"
# This ensures the 'app' is what Vercel sees as the entry point
# Do NOT wrap this in an 'if __name__ == "__main__"' block
app = app
