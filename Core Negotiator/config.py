from together import Together
import os
from dotenv import load_dotenv

# Load environment variables from your Code.env
load_dotenv("Code.env")
api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)

# Define a function to get completions from your custom model.
def custom_llm_completion(messages):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=messages
    )
    return response.choices[0].message.content

# Define your configuration dictionary.

guardrails_config = {
    "llm_client": custom_llm_completion,  # Use your custom LLM function.
    "postgres": {                         # Disable Postgres if not needed.
        "enabled": False
    }
    # You can include other settings if necessary.
}

# Optionally, add a message so you know the configuration has loaded.
if __name__ == "__main__":
    print("Guardrails configuration loaded.")
