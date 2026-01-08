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
        @app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        video_url = request.json.get("url")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # We ask the AI to give us a structured safety score
        prompt = f"Analyze this video for kids safety: {video_url}. Give me a safety score out of 10 and a 1-sentence reason."
        response = model.generate_content(prompt)
        
        # 🛡️ THE FIX: This ensures we always return a clean string
        if response.text:
            safe_text = response.text
        else:
            # Sometimes the AI blocks the response for safety, we handle that here
            safe_text = "Analysis blocked or unavailable for this video."

        return jsonify({"analysis": safe_text})
        
    except Exception as e:
        print(f"Error: {e}") # This will show up in your Vercel Logs
        return jsonify({"error": "AI is busy or link is invalid. Try again!"}), 500

# 3. CRITICAL: Vercel's "Secret Handshake"
# This ensures the 'app' is what Vercel sees as the entry point
# Do NOT wrap this in an 'if __name__ == "__main__"' block
app = app
