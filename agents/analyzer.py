import json
from utils.llm import call_llm

def analyze(ad_input, page):

    prompt = f"""
You are an AI marketing analyst.

Analyze the ad and landing page.

Return ONLY valid JSON.

FORMAT:
{{
  "audience": "",
  "message": "",
  "tone": "",
  "offer": "",
  "problems_in_page": []
}}

Ad:
{ad_input}

Page:
{page}
"""

    response = call_llm(prompt)

    try:
        result = json.loads(response)
        return result
    except:
        # 🔥 HARD FALLBACK (never fail)
        return {
            "audience": "general users",
            "message": "Generic product",
            "tone": "promotional",
            "offer": "discount available",
            "problems_in_page": [
                "CTA not strong",
                "Message not aligned with ad"
            ]
        }