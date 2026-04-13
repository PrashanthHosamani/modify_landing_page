import requests
import os
import streamlit as st

def get_api_key():
    return os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data, timeout=30)
    result = response.json()

    if "error" in result:
        return {"error": result["error"]["message"]}

    return result["choices"][0]["message"]["content"]