from utils.llm import call_llm

prompt = "Explain what a landing page is in one line"

response = call_llm(prompt)

print(response)
