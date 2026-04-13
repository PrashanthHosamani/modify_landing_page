import json
from utils.llm import call_llm

def plan_changes(analysis):

    prompt = f"""
You are a CRO expert.

Create a landing page improvement plan.

Return ONLY valid JSON.

FORMAT:
{{
  "headline": "",
  "cta": "",
  "sections": [
    {{
      "section": "",
      "change": ""
    }}
  ]
}}

Analysis:
{analysis}
"""

    response = call_llm(prompt)

    try:
        result = json.loads(response)
        return result
    except:

        return {
            "headline": "Limited Time Offer – Upgrade Your Experience",
            "cta": "Shop Now",
            "sections": [
                {
                    "section": "hero",
                    "change": "Add strong value proposition aligned with ad"
                },
                {
                    "section": "cta",
                    "change": "Make CTA more visible and action-driven"
                }
            ]
        }