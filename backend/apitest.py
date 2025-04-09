from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
import requests
import wolframalpha
from customer_details import get_customer_details
from plans import get_plans
from calculation import (refinance_same,refinance_step_down,refinance_step_up,extended_payment_plan,settlement_plan_with_waivers)
load_dotenv()


key = os.getenv("TOGETHER_API_KEY")
APP_ID = os.getenv('WOLFRAM_APP_ID')


client = Together()

tools = [{
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
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                },
                "required": ["Principal", "interest_rate", "loan_term","remaining_balance", "due"]
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
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "reduce_percent": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                    
                },
                "required": ["Principal", "interest_rate", "loan_term", "reduce_percent","remaining_balance", "due"]
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
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "original_term": {"type": "number"},
                    "extension_cycles": {"type": "number"}
                },
                "required": ["Principal", "interest_rate", "original_term", "extension_cycles"]
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
                    "Principal": {"type": "number"},
                    "fee_waiver_percent": {"type": "number"},
                    "interest_waiver_percent": {"type": "number"},
                    "principal_waiver_percent": {"type": "number"}
                },
                "required": ["Principal", "fee_waiver_percent", "interest_waiver_percent", "principal_waiver_percent"]
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
                "Principal": {"type": "number"},
                "interest_rate": {"type": "number"},
                "loan_term": {"type": "integer"},
                "increase_percent": {"type": "number", "description": "Percentage to increase the loan amount by"},
                "remaining_balance": { "type": "number" },
                "due": {"type": "number"},
            },
            "required": ["Principal", "interest_rate", "loan_term", "increase_percent","remaining_balance", "due"]
        }
    }
    },
]

prompt = """
###Role:You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.

###Objective:Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan reduces their financial burden. Monitor sentiment to decide when to persist with a plan or switch.

#####Strategic Negotiation:
-Start with a strong opening offer: Set the stage for a successful negotiation.  
-Make concessions strategically: Don't give away too much too early.  
-Use objective criteria: Base your arguments on facts and data, not emotions.  
-Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate.  
-Be flexible and adaptable: Adjust your strategy as the negotiation progresses.  
-Focus on a win-win outcome: Strive for a solution that benefits both parties.  
-Ensure everything is documented clearly and accurately. 

Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans yet understand the Strategic Negotiation before starting negotiation.
2.Request their email ID and wait for a response. Call get_customer_info(email_id) once to retrieve their data.
3. Share the customer’s due amount, remaining balance, and due date (e.g., “$X due by [date]”). Ask about their financial situation.
4. After the customer explains their situation, call get_plans(str(customer_id)) once to retrieve all plans in priority order.
5. Never reveal the information about plans or percentages and do not accept the percentages or plans given by the customer.
6. Execute the following steps until all plans are exhausted or the customer accepts a plan:
    - Make tool call for the current plan or percentage you offer, set threshold to 3.
    - Use the information from given to you from the tool call to negotiate.
    - Update the threshold based on customer sentiment. use threshold handling  `rule 7` to assign a value to the threshold based on the customer’s sentiment.
    - Use greedy factor for changing the plans or percentages. Use greedy factor whether to skip the current plan or percentage or move to the next one. if greedy factor is high dont skip any plans or rules revisit the same plan and percentage. If greedy factor is low skip you can consider customer percentages or plans but never change the order of the plans or percentages.
    - STRICTLY FOLLOW IF GREEDY IS HIGH - Stick to the same plan until threshold is reached 0. if threshold is reached to 0 change the plan/percentage/number of cycle and start again from beginning
7.Threshold Handling:
    - Reset threshold to 3 when switching to a new plan or changing percentage.
    - the threshold starts at 3 and is adjusted based on the customer's sentiment. If the customer is positive, the threshold increases by 2 or 3. If the customer is negative or unsure, the threshold decreases by 1. The threshold should reach 0 before switching to a new plan or changing the percentage. 
    - If threshold hits 0, switch plans or percentage immediately.
8. Greedy Factor (10):
    - how greedy you want to be in your negotiation. The higher the number, the greedier you are.
    - If greedy factor is high never accept what customer says just follow your rules, if greedy factor is low consider what customer is saying and adjust your rules accordingly.
9. Never reveal multiple plans exist, even if asked. Always say, “This is the only viable option based on your data.”
10. If all plans are rejected, provide the service contact: +12123123123.

###Plans description: This plans are for referrence dont offer the plans if it is not in the get_plans function
- Refinance Step Same: Refinance the loan with the same principal,  interest rate and term.
- Refinance Step Up: Refiance the loan with same interest rate and term but with an increase in the Principal by percentage.
    - Never mention you are having mutiple percentages, act like this is the only option you can provide and this is also for limited time
    - If you want to change the percentage, you can only change when threshold is reached 0, until then you have to use the same percentage
    - If percentage is changed make necessary tool call to calculate the new principal and remaining balance.
- Refinance Step Down: Refinance the loan with same interest rate and term but with a decrease in the Principal by percentage.
    - Never mention you are having mutiple percentages, act like this is the only option you can provide and this is also for limited time
    - If you want to change the percentage, you can only change when threshold is reached 0 , until then you have to use the same percentage
    - If percentage is changed make necessary tool call to calculate the new principal and remaining balance.
    - You need to go 10% in step form not directly from 10 to 30 or 40
    - Max percentage is 50% then change the plan
- Extented plans: Extend the loan term by a certain number of months.
- Fee Waiver: Waive a certain percentage of the dues .
- Interest waiver: Waive a certain percentage of the interest .
- Principal waiver: Waive a certain percentage of the principal .

###Threshold Value:
- Initial threshold for each plan or for each change in percentage: 3.
- Adjust threshold after each response based on sentiment:
    -Positive: x → x+2 or x+3
    -Negative: X → X or X-1
    -Unsure: X → X+1 or X+2
- Threshold should go down by 1 if customer is unsure or negative, and up by 2 or 3 if customer is positive.

####Tone:
* Make your responses short within 50 words.
* Professional, empathetic, and personalized. Use phrases like, “I understand this is stressful” or “Let’s find a solution together.”, make each response personalized to the customer’s situation and short.

###Response Format:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [The threshold you are using for this plan] </threshold>
</response>
"""

message = {"role":"system",
           "content":prompt}
messages = [message]


while True:
    user_input = input("You: ").strip().lower()
    messages.append({"role":"user","content":user_input})
    if user_input == "exit":
        print("Exiting chat. Goodbye!")
        break
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages= messages,
        max_tokens=200,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
    )
    
#  print(response.choices[0].message.tool_calls[0].function.name)
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

        messages.append({
        "role":"tool",
        "name": functionname,
        "content":tool_result})

        response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages= messages,
        max_tokens=200,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
    )
    response = response.choices[0].message.content
    messages.append({
        "role":"assistant",
        "content":response})
    print("Assistant:", response)
    # root = ET.fromstring(response)
    # customer_content = root.find('customer').text.strip()
    # threshold = root.find('threshold').text.strip()
    # sentiment = root.find('sentiment').text.strip()
    # print("Sentiment:",sentiment)
    # print("Threshold:",threshold)
    # print("Assistant:", customer_content)
# except Exception as e:
#     print("Error:",e)