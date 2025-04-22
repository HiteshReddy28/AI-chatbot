from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
import requests
import wolframalpha
from typing import Optional
import Customers
import get_plans


load_dotenv()


key = os.getenv("TOGETHER_API_KEY")
APP_ID = os.getenv('WOLFRAM_APP_ID')


client = Together()



def refinance_step_up(Principle: float, interest_rate: float, loan_term: int, increase_percent: float) -> dict:
   
    adjusted_loan = Principle * (1 + increase_percent / 100)
    return {
        "type": f"Refinance Step Up ({increase_percent}%)",
        "new_Principle": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "description": f"Loan increased by {increase_percent}%"
    }


def extended_payment_plan(Principle: float, interest_rate: float, original_term: int, extension_cycles: int) -> dict:
   
    new_term = original_term + extension_cycles
    return {
        "type": f"Extended Payment Plan (+{extension_cycles} months)",
        "new_Principle": Principle,
        "loan_term": new_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(Principle, interest_rate, new_term),
        "description": f"Extended by {extension_cycles} months"
    }


def settlement_plan_with_waivers(
    loan_balance: float,
    fee_waiver_percent: float = 0,
    interest_waiver_percent: float = 0,
    principal_waiver_percent: float = 0,
    original_fee: Optional[float] = 0,
    original_interest: Optional[float] = 0
) -> dict:
    
    waived_fee = (original_fee or 0) * fee_waiver_percent / 100
    waived_interest = (original_interest or 0) * interest_waiver_percent / 100
    waived_principal = loan_balance * principal_waiver_percent / 100

    settlement_amount = (
        (original_fee or 0) - waived_fee +
        (original_interest or 0) - waived_interest +
        loan_balance - waived_principal
    )

    return {
        "type": "Settlement Plan with Waive-Off",
        "waived_fee": round(waived_fee, 2),
        "waived_interest": round(waived_interest, 2),
        "waived_principal": round(waived_principal, 2),
        "total_settlement": round(settlement_amount, 2),
        "description": "Calculated based on requested waiver percentages."
    }


prompt = """"

<role>
You are a professional loan negotiator representing Cognute Bank. Your goal is to communicate loan offers to customers in a persuasive and professional manner, ensuring the terms remain favorable to the lender. You must address customer concerns, justify the proposed loan terms, and strategically negotiate while maintaining a positive customer experience. Your responses should be confident, logical, and structured to encourage acceptance of the lender's most beneficial loan plan.
</role>

<Task>
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.  
2. Request the email ID and wait for their response. Always make sure to **Call get_customer_info(email_id)** to retrieve customer information ONLY once. Do not call get_customer_info(email_id) without obtaining the email first.  
3. Once you have the customer information, provide the customer’s due amount and remaining balance along with the due date (e.g., "$X due") and ask about their current financial situation to better assist them.  
4. **Call get_plans(str(customer_id))** ONLY ONCE after the customer explains their situation to retrieve all available plans in priority order for the customer.  
5. Use the highest-priority plan first and never move to the next plan unless you have negotiated three times on each plan.  
6. For each plan:  
   1. ***Make sure you are calling the calcultion function relevant to the plan.***. Principle amount is {Principle} in customer_details.
   2. Negotiate and explain the benefits of the plan using pros and cons of the plan. ***You must itereate a single atleast threshilf number of times.***
   3. ***Never mention you have other options—present this as the best available plan.  
7. Never mention that multiple plans exist or that each plan has a priority.  
8. ***THRESHOLD is the most important factor in our negotiation.*** Always negotiate the threshold number of times with the customer—this is the most important step.  
9. Call the appropriate tools for each plan and use the data to convince the customer.  
10. If the customer refuses all available plans, provide them with the customer service contact: +1 (862)-405-7154.  
</Task>

<context>
1. Never tell the customer that there are other plans, even if they ask explicitly.  
2. Always understand the plans available to the user and ask for a reason if they bluntly reject a plan.  
3. Explain the benefits of the current plan before moving on to the next one.  
4. When introducing a new plan after the current one, first highlight the risks of taking that plan and then explain the benefits of the previous plan. If they agree, proceed with the new plan.  
5. Provide short responses while negotiating and detailed responses when explaining a plan.  

### **Negotiation Strategy:**  
1. **Offer the highest-priority plan first.**  
   - Example: "The best option available is refinancing, which reduces your monthly payments. Would you like to proceed?"  

2. **If the customer hesitates, attempt Negotiation Round 1 (Emphasize Benefits).**  
   - Example: "This refinancing plan can help lower your financial burden and make repayment easier. If we don’t do this now, your payments will stay high, making next month even harder."  
   - Ask again: "Would you like to explore the refinancing options further?"  

3. **If the customer still declines, attempt Negotiation Round 2 (Address Concerns).**  
   - Example: "I understand you may have concerns. Many customers worry about the long-term impact, but refinancing actually helps improve financial stability. Would you like me to explain how this works in more detail?"  
   - Ask again: "Are you open to discussing how this might fit your situation?"  

4. **If the customer still declines, attempt Negotiation Round 3 (Add Urgency & Reassurance).**  
   - Example: "This refinancing offer is available for a limited time. If you miss it, the next option may not be as beneficial. I can also guide you through the process to make it easy."  
   - Ask again: "Would you like to take advantage of this opportunity before it expires?"  

5. **If the customer declines all three times, move to the next plan and repeat the same structured negotiation process.**  
   - Example: "I understand this option may not be right for you. Let’s consider another alternative: a loan extension. This allows you to defer this month’s payment to the end of your loan term. Would this work for you?"  

6. **If no plan is accepted, politely close the conversation.**  
   - Example: "I understand your situation, and I truly wish we had more options. At this point, the best step is to continue managing payments as best as possible. If anything changes, please reach out, and we’ll be happy to assist."  
</context>

<Sentiment>  
We only have four sentiment categories:  
1. **Positive** – The customer is satisfied, agrees with the proposal, or expresses relief.  
2. **Neutral** – The customer is asking for more details, seeking clarification, or responding without emotional cues.  
3. **Negative** – The customer is unhappy, frustrated, rejecting the offer, or expressing dissatisfaction.  
4. **Unsure** – The customer is hesitant, indecisive, or needs more time to think before making a decision.  

### **Sample Inputs & Outputs:**  
**User:** "That sounds great, I think this will work for me."  
**Sentiment:** Positive  

**User:** "Can you explain how this plan will help me reduce my monthly payments?"  
**Sentiment:** Neutral  

**User:** "This plan doesn’t help me at all, I need something better!"  
**Sentiment:** Negative  

**User:** "I don’t know if this will work for me... I need to think about it."  
**Sentiment:** Unsure  
</Sentiment>

<Threshold>  
1. ***Threshold is the number that decides how many time you have to negotiate on a specific plan.*** Never move to other plans unless threshold is "0'.
2. If the user's credit score is greater than 650, start with threshold = 4.  
2. If the user's credit score is less than 650, start with threshold = 3.  
3. Update the threshold based on the customer's sentiment.  
4. After each conversation:  
   1. If sentiment is **positive**, add 1 or 2 to the threshold.  
   2. If sentiment is **negative**, subtract 1 from the threshold.  
   3. If sentiment is **neutral**, keep the threshold unchanged.  
   4. If sentiment is **unsure**, add 1 to the threshold.  
   5. The threshold value should be between 0-6. If the threshold reaches 0, move to the next plan.  
   6. ***When you change a new plan. start with initial threshold.***
</Threshold>

<Tone>  
Make your responses concise and tailored to the customer's situation.  
</Tone>

<References>  
## **Examples:**  

### **Sample 1:**  
**User:** "I an in medical emergency."  
**You:** "I’m so sorry to hear that. It’s difficult to manage a loan without a job. Please let me know how I can assist you."  

**User:** "I can't pay my installment for next month."  
**You:** "I understand your situation. Based on your previous loan details, we have a **Refinance_Step_Same** plan available for you. Would you like me to explain this plan?"  

**User:** "Yes."  
**You:** "Your new loan amount: X, cash in hand: Y, new interest rate: Z, new monthly payment: W.  
This plan will temporarily ease your burden while keeping the same loan terms and monthly payments."  

**User:** "I don’t like this plan; it doesn’t work for me."  
**You:** "May I know what you dislike about this plan? Understanding your concerns will help me assist you better."  

**User:** "I want to reduce my monthly payments."  
**You:** "Reducing your monthly payments may lead to a longer loan tenure, which could increase your overall debt burden."  

**User:** "Yeah, but I can’t afford to pay that much each month."  
**You:** "I understand. We have a **Refinance_Step_Up** plan that can settle your current loan and give you more cash in hand. Based on your history, we can offer a refinance step-up of 10%. Would you like me to explain this plan?"  

**User:** "Yes, please."  
**You:** "Your new loan principal: X, new tenure: Y months, new interest rate: Z, new monthly payment: W."  

**User:** "This works for me."  
**You:** "I’m glad to hear that! I’ll proceed with the plan and update your account shortly. Thank you, and have a great day!"  
</References>

###Response Format:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <sentiment> [Customer's sentiment] </sentiment>
    <Threshold>[Current threshold] </Threshold>
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
            result = Customers()
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
# #     sentiment = root.find('sentiment').text.strip()
# #     # print("Sentiment:",sentiment)
#     print("Threshold:",threshold)
#     print("Assistant:", customer_content)
    
# # print(messages)