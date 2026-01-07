from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini
# You will set this 'GOOGLE_API_KEY' in the Vercel Dashboard later
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    video_url = data.get('url')

    prompt = f"""
    Analyze this YouTube video for child developmental quality: {video_url}
    
    Use these 17 criteria. For each, give a score of 0, 1, or 2 (2 is best) and a brief 1-sentence assessment.
    Criteria: 1. Ease of Imitation, 2. Relatability, 3. Unhurried Pace, 4. No Overstimulation, 5. Pro-Social Modeling, 6. Language Quality, 7. Age Appropriateness, 8. Real-World Connection, 9. Diversity/Inclusion, 10. Educational Value, 11. Emotional Regulation, 12. Active Participation, 13. Narrative Logic, 14. Audio Quality, 15. Visual Clarity, 16. Moral Lessons, 17. Creativity.

    RETURN ONLY A JSON OBJECT with this structure:
    {{
        "totalScore": 34,
        "details": [
            {{"criterion": "Criterion Name", "score": 2, "assessment": "Text here"}}
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        # We clean the response in case the AI adds markdown backticks
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        return json_text, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel needs this 'app' variable to run
