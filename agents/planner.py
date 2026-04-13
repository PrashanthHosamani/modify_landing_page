from utils.llm import call_llm
from utils.json_parser import extract_json


def plan_changes(analysis):
    prompt = f"""
You are a CRO (Conversion Rate Optimization) expert.

Based ONLY on this analysis:
{analysis}

IMPORTANT:
- Do NOT introduce new products, domains, or ideas
- Only improve EXISTING page content
- Keep changes realistic and relevant
- Focus on clarity, conversion, and alignment with ad

STRICT RULES:
- Return ONLY JSON
- No explanation
- No markdown

FORMAT:
{{
  "headline": "improved headline",
  "cta": "improved CTA",
  "sections": [
    {{
      "section": "existing section name",
      "change": "specific improvement"
    }}
  ]
}}
"""

    # Retry mechanism
    for _ in range(2):
        response = call_llm(prompt)
        plan = extract_json(response)

        if "error" not in plan:
            # Minimal constraint (avoid overly long headline)
            if "headline" in plan and len(plan["headline"]) > 120:
                plan["headline"] = plan["headline"][:120]

            return plan

    return {"error": "Failed to generate plan"}