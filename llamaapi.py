import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('LLAMA_API_KEY')
print(f"API Key found: {'Yes' if api_key else 'No'}")

def get_llama_response(prompt, max_tokens=100):
    try:
        print(f"Sending prompt: {prompt}")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.95
        }
        
        response = requests.post(
            "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            print(f"Received response: {result}")
            return result
        else:
            error_msg = f"API Error: Status {response.status_code}, {response.text}"
            print(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    test_prompt = "Write a short joke about programming"
    print("\nStarting test...")
    response = get_llama_response(test_prompt)
    print("\nFinal output:")
    print(f"Prompt: {test_prompt}")
    print(f"Response: {response}")
