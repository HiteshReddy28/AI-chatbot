import os
from typing import Tuple, Union
from together import Together

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Load API keys
API_KEYS = os.getenv("GUARD_API_KEYS", "").split(",")
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

_key_index = 0

def get_next_api_key():
    global _key_index
    key = API_KEYS[_key_index % len(API_KEYS)]
    _key_index += 1
    return key.strip()

def get_together_client():
    key = get_next_api_key()
    return Together(api_key=key)

def query_llm(prompt: str, user_input: str) -> Tuple[bool, int]:
    for _ in range(len(API_KEYS)):
        try:
            client = get_together_client()
            res = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200,
                temperature=0.2
            )
            content = res.choices[0].message.content.strip().lower()
            total_tokens = res.usage.total_tokens
            return "yes" in content, total_tokens
        except Exception as e:
            print(f"[Guard LLM ERROR]: {e}")
            continue
    return False, 0

# Guard Definitions

INPUT_GUARDS = [
    ("Detected offensive content.", "Does this input contain profanity or toxic language like idiot, stupid, etc Ignore words like no, ok? Reply yes or no.")
]

# OUTPUT_GUARDS = [
#      ("Detected offensive content.", "Does this input contain profanity or toxic language like idiot, stupid, etc? Reply yes or no.")]

def enforce_guardrails(text: str, checks) -> Tuple[bool, Union[int, dict]]:
    total_tokens = 0
    for message, prompt in checks:
        violated, tokens = query_llm(prompt, text)
        total_tokens += tokens
        if violated:
            return True, {
                "violations": [{"message": message}],
                "tokens_used": total_tokens
            }
    
    # Return total_tokens as int if no violation
    return False, total_tokens



def enforce_input_guardrails(text: str):
    return enforce_guardrails(text, INPUT_GUARDS)

# def enforce_output_guardrails(text: str):
#      return enforce_guardrails(text, OUTPUT_GUARDS)
