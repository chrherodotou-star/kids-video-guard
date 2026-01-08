import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# We store the criteria as a clean string to avoid encoding errors
CRITERIA = """
1. Easy to imitate. 2. Realistic/Relatable. 3. Positive behaviors. 5. Social relationships. 
6. Creativity. 7. Active Repetition. 8. Easy dialogue. 9. No distractions. 10. Important concepts repeated. 
11. Unhurried pace. 12. Interactive. 13. Narration/Visuals complement. 14. Conversational style. 
15. Learning Elements Highlighted. 16. Cognitive Dev. 17. Physical Dev. 18. Socio-Emotional Dev.
"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        video_url = data.get("url")
        
        if not API_KEY:
            return jsonify({"error": "Key missing in Vercel settings"}), 500

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Watch this video: {video_url}. Assess it against these criteria: {CRITERIA}. "
            "Present findings in an HTML table with columns: Criterion, Assessment, Score (0,1,2), and Justification. "
            "Calculate a final score out of 34 and a percentage. Return ONLY the HTML table and score."
        )
        
        response = model.generate_content(prompt)
        
        # Ensure we return a key named "analysis"
        return jsonify({"analysis": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app
