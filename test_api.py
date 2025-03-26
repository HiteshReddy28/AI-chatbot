from together import Together
import os
import dotenv
dotenv.load_dotenv()

sample_email = "test@example.com"
def get_email(emai):
    if(email == sample_email):
        return True
    return False

user_plans = [
    {"plan1" : " 1. Pay "}
]

def get_userPlans():
    return user_plans
# Set 
client = Together()
messages = []
system_message = """
<Role> You are a senior negotiation agent in a money lending company..</Role>
<Instruction> <start> You have to respond with a short and concise message.</start>
              <authentication> check user eith his email adressusing {get_email()} function</authentication>
            rules>Get




</Instruction>
<Context> 
"""
messages.append({"role": "system", "content": system_message})
# Create a completion
while True:
    prompt = input("Enter prompt:")
    messages.append({"role": "user", "content": prompt})
    if prompt == "exit":
        break
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages = messages,
        max_tokens=300,
        temperature=0.1
    )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print("Response received:", response.choices[0].message.content)
    

# print("Response received:", response.choices[0].message.content)
# if 'output' in response:
#     print("\nGenerated text:", response['output']['choices'][0]['text'])
