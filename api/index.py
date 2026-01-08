import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini
API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Your specific 18-point criteria
CRITERIA_TEXT = """
Use these 18 criteria: 1. Easy to imitate. 2. Realistic/Relatable. 3. Positive behaviors. 
5. Social relationships. 6. Creativity. 7. Active Repetition. 8. Easy dialogue. 
9. No distractions. 10. Concepts repeated. 11. Unhurried pace. 12. Interactive elements. 
13. Narration/Visuals complement. 14. Conversational style. 15. Learning elements highlighted. 
16. Cognitive development. 17. Physical development. 18. Socio-emotional development.

SCORING: No (0), Partial (1), Yes (2). Total out of 34.
"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        video_url = data.get("url")
        
        if not API_KEY:
            return jsonify({"error": "API Key not set in Vercel"}), 500

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = (
            f"Watch this YouTube video: {video_url}. "
            f"Assess it using these rules: {CRITERIA_TEXT}. "
            "Output an HTML table with columns: Criterion, Assessment, Score, Justification. "
            "End with 'Final Score: X/34' and 'Percentage: X%'."
        )
        
        response = model.generate_content(full_prompt)
        return jsonify({"analysis": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel entry point
app = app
