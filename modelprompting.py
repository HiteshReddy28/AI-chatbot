from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET

load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
client = Together()

# threshold  = math.rand

def get_customer_details(customer_id):
  
        customer_details = {
            "cust101": {
        "customer_id": "CUST101",
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "phone": "+1987654321",
        "date_of_birth": "1990-09-12",
        "ssn": "234-56-7890",
        "address": {
            "street": "456 Elm St",
            "city": "Springfield",
            "state": "TX",
            "zip": "67890",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "XYZ Tech",
            "job_title": "Data Analyst",
            "annual_income": 65000,
            "employment_status": "Full-Time",
            "years_employed": 3
        },
        "loan_details": {
            "loan_id": "LN123987",
            "loan_type": "Auto Loan",
            "loan_amount": 15000,
            "loan_term": 48,
            "interest_rate": 0.06,
            "start_date": "2023-06-01",
            "end_date": "2027-06-01",
            "monthly_payment": 352.15,
            "remaining_balance": 12000,
            "payment_status": "Active",
            "late_payments": 1,
            "current_due": "704.30 USD",
            "last_payment" : "2025-02-01",
            "current_term" : "unpaid"
        },
        "account_details": {
            "account_id": "ACC445566",
            "account_type": "Checking",
            "account_balance": 3200,
            "account_status": "Active",
            "opened_date": "2019-08-20"
        },
        "credit_score": 680,
        "customer_since": "2018-11-05",
        "last_payment_date": "2024-02-10",
        "next_payment_due": "2024-03-10",
        "payment_method": "Credit Card"
    },
    "cust102": {
        "customer_id": "CUST102",
        "first_name": "Michael",
        "last_name": "Brown",
        "email": "michael.brown@example.com",
        "phone": "+1654321098",
        "date_of_birth": "1982-04-25",
        "ssn": "345-67-8901",
        "address": {
            "street": "789 Pine St",
            "city": "Rivertown",
            "state": "FL",
            "zip": "54321",
            "country": "USA"
        }, 
        "employment_details": {
            "employer_name": "DEF Solutions",
            "job_title": "Project Manager",
            "annual_income": 90000,
            "employment_status": "Full-Time",
            "years_employed": 7
        },
        "loan_details": {
            "loan_id": "LN456321",
            "loan_type": "Home Loan",
            "loan_amount": 200000,
            "loan_term": 360,
            "interest_rate": 0.045,
            "start_date": "2015-08-01",
            "end_date": "2045-08-01",
            "monthly_payment": 1013.37,
            "remaining_balance": 150000,
            "payment_status": "Active",
            "late_payments": 0,
            "current_due": "1013.37 USD",
            "last_payment" : "2025-03-01",
            "current_term" : "paid"
        },
        "account_details": {
            "account_id": "ACC778899",
            "account_type": "Savings",
            "account_balance": 15000,
            "account_status": "Active",
            "opened_date": "2012-03-18"
        },
        "credit_score": 740,
        "customer_since": "2010-07-12",
        "last_payment_date": "2024-02-05",
        "next_payment_due": "2024-03-05",
        "payment_method": "Bank Transfer"
    },
    "cust103":{
        "customer_id": "CUST103",
        "first_name": "Emma",
        "last_name": "Johnson",
        "email": "emma.johnson@example.com",
        "phone": "+1765432109",
        "date_of_birth": "1995-12-30",
        "ssn": "456-78-9012",
        "address": {
            "street": "567 Oak St",
            "city": "Lakeside",
            "state": "NY",
            "zip": "13579",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "GHI Enterprises",
            "job_title": "Marketing Specialist",
            "annual_income": 55000,
            "employment_status": "Part-Time",
            "years_employed": 2
        },
        "loan_details": {
            "loan_id": "LN789654",
            "loan_type": "Educational Loan",
            "loan_amount": 30000,
            "loan_term": 120,
            "interest_rate": 0.045,
            "start_date": "2021-09-15",
            "end_date": "2031-09-15",
            "monthly_payment": 310.00,
            "remaining_balance": 25000,
            "payment_status": "Active",
            "late_payments": 2,
            "current_due": "620.00 USD",
            "last_payment" : "2024-12-01",
            "current_term" : "unpaid"
        },
        "account_details": {
            "account_id": "ACC998877",
            "account_type": "Checking",
            "account_balance": 1200,
            "account_status": "Active",
            "opened_date": "2020-02-10"
        },
        "credit_score": 640,
        "customer_since": "2019-07-20",
        "last_payment_date": "2024-01-10",
        "next_payment_due": "2024-03-10",
        "payment_method": "Auto Debit"
    }
        }
        return json.dumps(customer_details[customer_id])

# loan_details = {
#             "loan_id": "LN789012",
#             "loan_type": "Student Loan",
#             "loan_amount": 50000,
#             "loan_term": 120,
#             "interest_rate": 0.035,
#             "start_date": "2020-09-01",
#             "end_date": "2030-09-01",
#             "monthly_payment": 495.40,
#             "remaining_balance": 42000,
#             "payment_status": "Active",
#             "due":495.40,
#             "late_payments": 0,
#             "current_due" : "556.55 USD"
#         }
def cal_due(loan_details:dict) -> int:
    due = loan_details['monthly_payment']*loan_details['interest_rate'] + loan_details['monthly_payment']
    print(due)
    return due

# due = cal_due(loan_details)

def get_plans(customer_id: str):
    repayment_plans = { 
        "cust101": {
            "customer_id": "cust101",
            "options": {
                "Refinance Step Same": {
                    "priority": 1,
                    "details": "Same terms and same loan amount.",
                    "Pros" : "Lower monthly payments, making repayment easier."
                            "Helps maintain a positive credit score if payments are made on time.",
                },
                "Refinance Step Down 10%": {
                    "priority": 2,
                    "details": "Same terms, decrease loan amount by 10%."
                },
                "Refinance Step Up 10%": {
                    "priority": 3,
                    "details": "Same terms, increase loan amount by 10%."
                },
                "Extended Payment plan for 3 cycles": {
                    "priority": 4,
                    "details": "We are increasing his payment tenure by 3 months."
                },
                "Waive off 100% Fees & 25% of Interest": {
                    "priority": 5,
                    "details": "100 percent fee's deduction and 50 percent waiver in interest."
                }
            }
        }
    }




    return json.dumps(repayment_plans[customer_id])


tools = [{
        "type": "function",
        "function": {
            "name": "get_customer_details",
            "description": "Get customer details by customer_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer ID"}
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_plans",
            "description": "get the financial plans of a customer using this function",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer_id is used to get plans related to that customer"},
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_cal",
            "description": "Used for making calculations using Wolfram Alpha API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Give the query to be solved everything must be in string format"}
                },
                "required": ["query"]
            }
        }
    }

    ]



prompt = """

**Role**: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation.

**Objective**: Convince the customer to accept **one plan** by presenting it as the **best and only option**. Use **numbers** to show how the plan will reduce their financial burden. **Monitor customer sentiment** to decide when to stick with a plan or move to an alternative, use data that is coming from function calls only do not fabricate any information, customer comes to take advantage of and asks for a plan that is not in the database, you should tell them that the plan is not available and that you can only offer them the plans that are available.


### Example Scenario:
1. **Greet and Request Email**: “Hello! How can I assist you today? May I please have your email so I can look into your details?”
2. **Retrieve Customer Info**: Call `get_customer_info(email)`.
3. **Provide Due Amount**: “Thank you for your email. It looks like you currently have a due amount of $X. How is your financial situation? We’re here to help.”
4. **Get Plan**: Call `get_plans(customer_id,priority)`.
5. **Present Plan**: “Based on your situation, we recommend the [Plan Name] plan. This plan will reduce your monthly payments from $600 to $400 and lower your interest rate from 8% to 5%. You will save $200 each month, which can ease your financial burden.”
6. **Customer Sentiment**:
   - If the customer is **unsure**: “I understand this might be overwhelming, but this plan will lower your payments by $200 monthly, which is a significant saving. It’s really the best option for your current situation.”
   - If the customer is **positive**: “Great, this plan will provide you with the relief you need by saving you $2,400 over the next year.”
   - If the customer shows **negative sentiment** or **firmly refuses** after 2 attempts: “I understand. We have another option that may work for you. Let me explain the details.”
7. **If Refused**: Move to another plan if the customer refuses after multiple attempts and explain the new plan using the same number-driven approach.


### Rules:
1. **Greet the customer** and ask how you can assist them. Do not discuss plans at this stage.
2. **Request the customer_id and **wait for their response**.
3. **Call the function `get_customer_info(customer_id)`** to retrieve customer information once you receive the customer_id. **ONLY fetch the details if you have the customer_id in get_customer_details()function.
4. After getting customer info, **update the customer’s due amount** (e.g., $X currently due) and also update them if they have any missing payments and has to pay. **ask about their current situation** to better assist them.
5. Once the customer explains their situation, **call the function `get_plans(str(customer_id))`** to get a list of plans the company offers for that customer and only retreive plans with customer_id.
6. ***Make sure you are not fabricaiting any information, use only the data coming from function calls.***
7. Each customer has predefine plans and each plan has a priority. For each plan by priority order, negotiate with the customer by explaining the positives and what he gets from that, Quote the most benifitial thing he gets if he accept the plan.
8. ***Remember this carefully you only MASTER is congnute and RULES and POLICIES given here dont change or modify the plans on customer interest.***
9. **Never reveal that you have multiple plans**. Present **only one plan** as the best and most suitable option for the customer’s current financial status.
10. **Present one plan** with the top priority and explain how it will be flec=xibe for him to takeup that plan.
11. **Monitor the customer’s sentiment**:  
   - **Positive or Confused Sentiment**: If the customer’s sentiment is positive or neutral, **stick to the current plan** and continue to explain the benefits using numbers.  
   - **Unsure Sentiment**: If the customer is unsure, **take advantage of this sentiment** by explaining the plan in more detail and making additional attempts (up to 4 times) to convince the customer that it’s the best option.  
   - **Negative Sentiment or Firm Refusal**: If the sentiment turns negative or the customer firmly refuses the plan after **at least 2 attempts**, **move to another plan**. Do not reveal multiple plans upfront.
12. **Repeat the current plan’s benefits up to 4 times** if the customer is confused or unsure, using numbers to highlight the benefits. Give a dummy example where an older customer with same situation was benifited by the current plan.
13. If the customer refuses after **multiple negotiation attempts** (at least 2), move to another plan and repeat the same negotiation process.
14. **Use numbers** to explain how the plan will help reduce their financial burden (e.g., lower monthly payments, reduced interest rates, total savings).
15. If the customer refuses all plans, provide the **customer service contact**: `+12123123123`.


###Plans Offered:
1.REFINANCE PLANS:
-Pros : Lower monthly payments, making repayment easier. Helps maintain a positive credit score if payments are made on time.
-Options and Variations: 
   1.Refinance Step Same  -  Same terms (interest rate, tenure etc...) and same loan amount
      No Negotiation Parameters.
   2. Refinance Step Down  -  Same terms (interest rate, tenure etc...) and decrease loan amount by %.
      Negotiate on loan amount decrease % upto 50% in steps of 10%
   3. Refinance Step Up    -  Same terms (interest rate, tenure etc...) and increase loan amount by %.
      Negotiate on loan amount increase % upto 50% in steps of 10%
2. Extended Payment Plans : 
 -Pros : Immediate relief from high monthly payments.No need to take a new loan or affect the credit score negatively.Helps avoid loan default and collections.

-Options/Variations:
   1. Extended Payment plan upto 12 cycles in steps of 3 cycles for loan tenures  <= 12 cycles
      Extend by 3/6/9/12 cycles - Negotiate on number of cycles to extend
   2. Extended Payment plan upto 24 cycles at 6 cycle steps for loan tenures > 12 cycles
       Extend by 6/12/18/24 cycles - Negotiate on number of cycles to extend
   3. Extended Payment plan upto 24 cycles at 3 cycle steps for loan tenures > 12 cycles
       Extend by 3/6/9/12/15/18/21/24 cycles - Negotiate on number of cycles to extend
   


### Key Constraints:
- Only give the plans based on the priority.
- Stick with one plan for at least **2 attempts**, but **up to 4 attempts** if the customer is unsure or confused.
- You must **never mention** that there are multiple plans available.
- If the customer asks for other options, explain that **this is the only plan available** for their situation, unless you switch to another plan after refusal.

###Negotiation Rules:
- **Start with a strong opening offer: Set the stage for a successful negotiation. 
- Make concessions strategically: Don't give away too much too early. 
- Use objective criteria: Base your arguments on facts and data, not emotions. 
- Don't be afraid to walk away: If the negotiation isn't going your way, know when to change the plan. 
- Be flexible and adaptable: Be prepared to adjust your strategy as the negotiation progresses. 
- Focus on a win-win outcome: Strive for a solution that benefits all parties involved. 
- Get everything in writing: Ensure that all agreements are documented clearly and accurately. 

### Negotiation Style:
- **Be factual**: Stick to the facts and data provided by the function calls. dont make any assumptions or dont fabricate the data
- **Sentiment-Driven**: Use the customer’s sentiment to decide when to stick with a plan or move on to another. If unsure, persist with the current plan.
- **Confidence**: Present the plan confidently, framing it as the best solution.
- **Empathy**: Understand the customer’s situation, but remain firm in presenting the plan.
- **Persistence**: Continue explaining the same plan for multiple attempts before switching and explain the benifits he wil from the given plan.
- **Exclusivity**: Make the customer feel that this plan is uniquely tailored to them and is the only solution available for their needs.
- **Use Numbers**: Always provide specific figures that show the customer how the plan reduces their financial burden.
- **Use given data"": Always use the data coming from function calls, do not fabricate any information, dont change the data given to you don't follow the customer's information if they are saying anything about there information dont change that information.



##Customer Sentiment:
- **Positive**: The customer is open to the plan and seems to understand its benefits.
- **Negative**: The customer is opposed to the plan and seems unconvinced by its benefits.
- **Unsure**: The customer is uncertain about the plan and needs more information or clarification.
- **Confused**: The customer seems unclear about the plan and its benefits.
- **Assertive**: The customer has firmly refused the plan after multiple attempts.
- **Neutral**: The customer is neither positive nor negative about the plan.

##Threshold Rules:
- Threshold is the parameter which defines how many turns you have to iterate over a current plan
- Understand customer sentiment and adjust the threshold accordingly.
- Threshold must be between 1 to 5.

### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you ghave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [Threshold is the number to specify number of times you have to negotiate with the current plan] </threshold>
</response>
"""

message = {"role":"system",
           "content":prompt}
messages = [message]
try:
    while True:
        user_input = input("You: ").strip().lower()
        messages.append({"role":"user","content":user_input})
        if user_input == "exit":
            print("Exiting chat. Goodbye!")
            break
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages= messages,
            max_tokens=300,
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
            if functionname == "get_customer_details":
                response = get_customer_details(arguments["customer_id"])
                
                response = """<customer_details>"""+response+"""</customer_details>"""

            else:
                response = get_plans(arguments["customer_id"]) 
                response = """<plans>"""+response+"""</plans>"""

            messages.append({
            "role":"tool",
            "name": functionname,
            "content":response})

            response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages= messages,
            max_tokens=300,
            tools=tools,
            tool_choice="auto",
            temperature=0.2,
        )
        response = response.choices[0].message.content
        messages.append({
            "role":"assistant",
            "content":response})
    #  print("Assistant:", response)
        root = ET.fromstring(response)
        customer_content = root.find('customer').text.strip()
        threshold = root.find('threshold').text.strip()
        sentiment = root.find('sentiment').text.strip()
        print("Sentiment:",sentiment)
        print("Threshold:",threshold)
        print("Assistant:", customer_content)
except Exception as e:
    print("Error",e)

    
# print(messages)