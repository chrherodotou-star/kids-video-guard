import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Connect to Gemini
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        video_url = data.get("url")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Analyze this video for kids' safety: {video_url}")
        
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel needs this to run
def handler(event, context):
    return app(event, context)
