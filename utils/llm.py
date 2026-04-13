import requests
import os
import streamlit as st

def get_api_key():
    return os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY")

def call_llm(prompt):
    try:
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

        response = requests.post(url, headers=headers, json=data, timeout=30)

        # Handle HTTP errors
        if response.status_code != 200:
            return f"LLM API Error: {response.text}"

        result = response.json()

        # Handle API-level errors
        if "error" in result:
            return f"LLM Error: {result['error'].get('message', 'Unknown error')}"

        # Safe extraction
        choices = result.get("choices", [])
        if not choices:
            return "LLM Error: No response generated"

        message = choices[0].get("message", {})
        content = message.get("content", "")

        if not content:
            return "LLM Error: Empty response"

        return content

    except Exception as e:
        return f"LLM Exception: {str(e)}"