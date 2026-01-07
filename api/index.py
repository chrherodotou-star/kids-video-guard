import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- THE KEY FIX ---
# This looks for the key in multiple ways to make sure Vercel finds it
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    # If the standard way fails, it throws a clear error we can see in logs
    raise ValueError("CRITICAL: GOOGLE_API_KEY is not set in Vercel Environment Variables!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
# --------------------

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # ... (the rest of your analyze code remains the same)
