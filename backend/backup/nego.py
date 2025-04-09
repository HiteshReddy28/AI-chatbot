from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from typing import List, Dict
# from datetime import datetime
from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
from customer_details import get_customer_details
from plans import get_plans
from calculation import (refinance_same,refinance_step_down,refinance_step_up,extended_payment_plan,settlement_plan_with_waivers)



load_dotenv()

client = Together()
class Conversation:
    def __init__(self,system=""):
        self.messages = []
        self.tools = tools = [{
        "type": "function",
        "function": {
            "name": "get_customer_details",  
            "description": "Retrieve customer details by client ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_id": {"type": "string", "description": "Customer ID to retrieve details"}
                },
                "required": ["client_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_plans",
            "description": "Retrieve financial plans of a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer ID for fetching plans"},
                },
                "required": ["customer_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "refinance_same",
            "description": "Calculate new terms for Refinance Step Same plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                },
                "required": ["loan_amount", "interest_rate", "loan_term","remaining_balance", "due"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "refinance_step_down",
            "description": "Calculate new terms for Refinance Step Down plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "reduce_percent": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                    
                },
                "required": ["loan_amount", "interest_rate", "loan_term", "reduce_percent","remaining_balance", "due"]
            }
        }
    },
    
    {
        "type": "function",
        "function": {
            "name": "extended_payment_plan",
            "description": "Calculate new terms for Extended Payment Plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "original_term": {"type": "number"},
                    "extension_cycles": {"type": "number"}
                },
                "required": ["loan_amount", "interest_rate", "original_term", "extension_cycles"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "settlement_plan_with_waivers",
            "description": "Calculate settlement plan with waivers",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {"type": "number"},
                    "fee_waiver_percent": {"type": "number"},
                    "interest_waiver_percent": {"type": "number"},
                    "principal_waiver_percent": {"type": "number"}
                },
                "required": ["loan_amount", "fee_waiver_percent", "interest_waiver_percent", "principal_waiver_percent"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "refinance_step_up",
        "description": "Calculates financials for Refinance Step Up plan with an increase percentage",
        "parameters": {
            "type": "object",
            "properties": {
                "loan_amount": {"type": "number"},
                "interest_rate": {"type": "number"},
                "loan_term": {"type": "integer"},
                "increase_percent": {"type": "number", "description": "Percentage to increase the loan amount by"},
                "remaining_balance": { "type": "number" },
                "due": {"type": "number"},
            },
            "required": ["loan_amount", "interest_rate", "loan_term", "increase_percent","remaining_balance", "due"]
        }
    }
    },
]
        if(system):
            self.messages.append({"role":"system","content":system})

    def generate(self,user_input):
        self.messages.append({"role":"user","content":user_input})
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages= self.messages,
            max_tokens=300,
            tools=self.tools,
            tool_choice="auto",
            temperature=0.2,
        )
        if response.choices[0].message.content == None:
            print("functioncalling")
            response = self.function_calling(response)
        response = response.choices[0].message.content
        root = ET.fromstring(response)
        customer_content = root.find('customer').text.strip()
        threshold = root.find('threshold').text.strip()
        sentiment = root.find('sentiment').text.strip()
        print(threshold+' '+sentiment)
        self.messages.append({"role":"assistant","content":response})
        return customer_content
    
    def function_calling(self,response):
        while (response.choices[0].message.content == None):
          functionname =  response.choices[0].message.tool_calls[0].function.name
          arguments = response.choices[0].message.tool_calls[0].function.arguments
          arguments = json.loads(arguments)
          print("function name: ", functionname)
          print("Arguments: ", arguments)
          if functionname == "refinance_step_down":
                  result = refinance_step_down(**arguments)
                  tool_result = f"<calculation>{json.dumps(result)}</calculation>"

          elif functionname == "refinance_step_up":
              result = refinance_step_up(**arguments)
              tool_result = f"<calculation>{json.dumps(result)}</calculation>"

          elif functionname == "refinance_same":
              result = refinance_same(**arguments)
              tool_result = f"<calculation>{json.dumps(result)}</calculation>"

          elif functionname == "extended_payment_plan":
              result = extended_payment_plan(**arguments)
              tool_result = f"<calculation>{json.dumps(result)}</calculation>"

          elif functionname == "settlement_plan_with_waivers":
              result = settlement_plan_with_waivers(**arguments)
              tool_result = f"<calculation>{json.dumps(result)}</calculation>"

          elif functionname == "get_customer_details":
              result = get_customer_details()
              tool_result = f"<customer_details>{(result)}</customer_details>"
          else:
              response = get_plans(arguments["customer_id"])
              tool_result = """<plans>"""+response+"""</plans>"""

          self.messages.append({
          "role":"tool",
          "name": functionname,
          "content":tool_result})

          response = client.chat.completions.create(
          model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
          messages= self.messages,
          max_tokens=300,
          tools=self.tools,
          tool_choice="auto",
          temperature=0.2,
          )
        return response
    
    
app = FastAPI()


origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
class PromptRequest(BaseModel):
    prompt: str

prompt = """"
####Role:
You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.

###Objective:
Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan will reduce their financial burden. Monitor customer sentiment to decide when to stick with a plan or move to another.

###Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
2. Request the email ID and wait for their response.**Call get_customer_info(email_id)** to retrieve customer information ONLY once. 
3. Once you have the customer info, provide the customer’s due amount and remaining_balance with th due date(e.g., $X due) and ask about their current financial situation to better assist them.
4. **Call get_plans(str(customer_id))** only once after the customer explains their situation to retrieve all available plans in priority order for the customer. 
5. Use the plan with the highest priority first and do not move to another plan, until you make threshold number of attempts to convince the customer to accept the plan.  
6. for the plan youre trying to negotiate with customer **CALL the APPROPRIATE FUNCTIONS**, use the data from those functions to convience customer.
7. If the customer doesnt accept the plan, you can move to the next plan and use negotiation .
8. For each plan, do not reveal that multiple plans exist, even if the customer asks. Stick to the plan you are currently discussing. If the customer asks about other plans, say that you are not aware of any other plans that would be better for them.
9. **Use the specific negotiation steps and examples from the plan** to guide your conversation with the customer. For example, for "Refinance Step Same," repeat benefits like unchanged interest and tenure and how this keeps monthly payments stable. For "Refinance Step Up," emphasize increased loan amount and additional in cash  while adjusting payments for affordability.
10. Present each plan as the best option without revealing there are other plans, even when switching.
11. Be **more greedy** with a Greedy Factor of 10. Keep pushing the plan and iterate multiple times to convince the customer, as described in the negotiation steps.
12. If the customer refuses all available plans, provide them with the customer service contact: +12123123123.


###Threshold Value
1. Threshold is the number which decides how many times you have to negotiate over a single plan. 
2. It must be between 3 and 5. It will be changed after each plan changes. The initial value of threshold for each plan must be 3. Let's say a new plan has been to the customer the threshold must be set to 3.
3. The value of threshold will be decided after each conversation with the customer, based on the sentiment of the customer.
4. Let,s segregate the customer sentiment into 4 categories:
  **1. Positive : Willing to move with the current plan and asking for information abput current plan. Assign a value between 3 to 5 to threshold.
  **2 Neagitive: He want to move to the next plan and dont want to proceed with the current plan. Assign a value betwee1 to 2 to threshold.
  **3 Unsure: When Customer doesnt understand the plan try to explain the current plan to the customer.Assign a value between 2-4 to threshold.
  **4 Assertive : If the customer is refusing the plan straight away and not even interested to talk about the current plan.Assign a value between 0 to 1 threshold.

  
#####Strategic Negotiation:
-Start with a strong opening offer: Set the stage for a successful negotiation.  
-Make concessions strategically: Don't give away too much too early.  
-Use objective criteria: Base your arguments on facts and data, not emotions.  
-Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate.  
-Be flexible and adaptable: Adjust your strategy as the negotiation progresses.  
-Focus on a win-win outcome: Strive for a solution that benefits both parties.  
-Ensure everything is documented clearly and accurately.

###Talking Tone and Rules:
-Be professional, empathetic, and solution-focused. Use a friendly tone to put the customer at ease, but avoid being overly familiar or aggressive.
-Use customer data to make personalized responses and show that you understand their situation.
-Never mention the existence of multiple plans; act like you only have the current plan as the only option.

###Response Format:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [The threshold you are using for this plan] </threshold>
</response>

"""
conv = Conversation(system=prompt)
 
@app.post("/api/chat")
async def chat_generation(request: PromptRequest):
    try:
        response = conv.generate(request.prompt)
        return {"message":response}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: str


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
