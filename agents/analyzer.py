from utils.llm import call_llm
from utils.json_parser import extract_json


def validate_output(data):
    if "error" in data:
        return data

    # Normalize audience
    if "audience" in data:
        data["audience"] = data["audience"].lower()

    # Normalize + enforce tone
    allowed_tones = ["informative", "promotional", "emotional"]
    tone = data.get("tone", "").lower()

    if tone in allowed_tones:
        data["tone"] = tone
    else:
        data["tone"] = "informative"

    return data


def analyze(ad_text, page_content):
    prompt = f"""
You are a marketing analyst AI.

STRICT RULES:
- Return ONLY JSON
- No explanation
- No markdown
- Use EXACT tone from: ["informative", "promotional", "emotional"]

IMPORTANT:
- Base analysis strictly on given AD and PAGE
- Do NOT invent new products, domains, or tools
- Keep output specific and grounded

FORMAT:
{{
  "audience": "lowercase string",
  "message": "clear marketing message",
  "tone": "one of allowed values",
  "offer": "specific offer",
  "problems_in_page": [
    "actual problem in messaging or UX",
    "missing alignment with ad",
    "weak CTA or unclear value"
  ]
}}

AD:
{ad_text}

PAGE:
{page_content}
"""

    # Retry mechanism (2 attempts)
    for _ in range(2):
        response = call_llm(prompt)
        parsed = extract_json(response)

        if "error" not in parsed:
            return validate_output(parsed)

    return {"error": "Failed to analyze after retries"}