import requests
import os

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY_1")
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

def query_llm(prompt: str, input_text: str) -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text}
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
