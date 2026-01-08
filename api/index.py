import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Setup Flask
app = Flask(__name__)
CORS(app)

# 2. Configure Gemini
# Using a fallback to avoid crashing if the key is missing during build
gemini_key = os.environ.get("GOOGLE_API_KEY", "")
if gemini_key:
    genai.configure(api_key=gemini_key)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # Check if key exists
        if not gemini_key:
            return jsonify({"error": "API Key not found in Vercel Environment Variables"}), 500

        # Get data from frontend
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "No URL provided"}), 400
        
        video_url = data['url']

        # Initialize Model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Enhanced Prompt for 2026 Models
        prompt = (
            f"Act as a child safety expert. Analyze this YouTube video for safety: {video_url}. "
            "Provide a safety score (0-10) and a brief 1-sentence explanation. "
            "If the video is safe, start with 'SAFE'. If not, start with 'UNSAFE'."
        )
        
        response = model.generate_content(prompt)
        
        # Handle cases where response might be empty or blocked
        if not response.text:
            return jsonify({"analysis": "AI could not generate a report for this specific video."})

        return jsonify({"analysis": response.text})

    except Exception as e:
        # This will show up in your Vercel 'Functions' logs
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": "The AI service is currently unavailable. Please try again later."}), 500

# 3. VERCEL ENTRY POINT
# This line is the most important for fixing the 'issubclass' error.
# It explicitly tells Vercel that 'app' is the WSGI object.
app = app
