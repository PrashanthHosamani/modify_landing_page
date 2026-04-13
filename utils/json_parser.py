import json
import re

def extract_json(text):
    try:
        # Try direct parse first
        return json.loads(text)

    except:
        try:
            # Try to extract JSON block
            match = re.search(r'\{.*', text, re.DOTALL)
            if match:
                json_str = match.group()

                # Fix missing closing brace
                if not json_str.strip().endswith("}"):
                    json_str += "}"

                return json.loads(json_str)

            return {"error": "No JSON found", "raw": text}

        except Exception as e:
            return {"error": str(e), "raw": text}