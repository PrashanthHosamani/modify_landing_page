import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "meta-llama/llama-3-8b-instruct",
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

    response = requests.post(url, headers=headers, json=data)
    result = response.json()


    print("RAW RESPONSE:", result)

   
    if "error" in result:
        return f"Error: {result['error']['message']}"


    return result["choices"][0]["message"]["content"]
