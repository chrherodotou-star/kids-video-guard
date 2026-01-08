import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# THE SYSTEM PROMPT WITH YOUR 18 CRITERIA
SYSTEM_PROMPT = """
You are an expert in early childhood education. Analyze the provided YouTube video based on these 18 criteria:
1. Easy for child to imitate. 2. Realistic/Relatable. 3. Positive behaviors modeled. 
5. Social relationships positive. 6. Encourages creativity. 7. Encourages active repetition. 
8. Easy dialogue. 9. No multiple scenes/distractions. 10. Concepts repeated. 
11. Unhurried pace. 12. Interactive elements. 13. Narration/Visuals complement. 
14. Conversational style. 15. Learning elements highlighted. 16. Supports cognitive development. 
17. Supports physical development. 18. Supports socio-emotional development.

OUTPUT REQUIREMENTS:
- Present findings in an HTML table with columns: [Criterion, Assessment, Score, Justification].
- Scoring: No (0 points), Partial (1 point), Yes (2 points).
- If unsure, state "I am not certain" in Justification.
- After the table, provide: "Final Score: [Total]/34" and "Percentage: [X]%".
- Return ONLY the HTML code for the table and the final score text.
"""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        video_url = data.get("url")
        
        if not API_KEY:
            return jsonify({"error": "API Key missing"}), 500

        model = genai.GenerativeModel('gemini-1.5-flash')
        # We combine the system prompt with the specific video URL
        full_prompt = f"{SYSTEM_PROMPT}\n\nVideo to analyze: {video_url}"
        
        response = model.generate_content(full_prompt)
        
        return jsonify({"analysis": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = app
