import requests
import time

def verify_token(token: str) -> bool:
    """Verify if the token has proper access"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        "https://huggingface.co/api/whoami",
        headers=headers
    )
    return response.status_code == 200

def chat_with_model(prompt: str) -> str:
    """
    Have a conversation with LLaMA model.
    
    Args:
        prompt (str): The user's input message
        
    Returns:
        str: The model's response
    """
  
    
    # First verify the token
    if not verify_token(TOKEN):
        return "Error: Invalid token. Please make sure you have accepted the model's terms and have proper access rights."
    
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    
    # Format the prompt for better results
    formatted_prompt = f"""<s>[INST] {prompt} [/INST]"""
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_length": 500,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True,
            "return_full_text": False
        }
    } 



       
    while True:
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()[0]["generated_text"]
        except requests.exceptions.HTTPError as e:
            if response.status_code == 503:
                # Model is loading, wait and retry
                print("Model is loading, waiting...")
                time.sleep(20)  # Wait for 20 seconds before retrying
                continue
            return f"Error: {str(e)}"
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # First verify token
    
    if verify_token(TOKEN):
        print("Token is valid! Testing the model...")
        # Test the model with a question
        prompt = "Explain what is Python programming in 2 sentences."
        print(f"User: {prompt}")
        print(f"Assistant: {chat_with_model(prompt)}")
    else:
        print("Error: Invalid token. Please make sure you:")
        print("1. Have accepted the model's terms at: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf")
        print("2. Have waited for access approval")
