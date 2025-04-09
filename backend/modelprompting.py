from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET

load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
client = Together()

# threshold  = math.rand

def get_customer_details():
    customer_details = [
    {
        "customer_id": "CUST123456",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1985-06-15",
        "ssn": "123-45-6789",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "ABC Corp",
            "job_title": "Software Engineer",
            "annual_income": 85000,
            "employment_status": "Full-Time",
            "years_employed": 5
        },
        "loan_details": [
            {
                "loan_id": "LN987654",
                "loan_type": "Personal Loan",
                "loan_amount": 10000,
                "loan_term": 60,
                "interest_rate": 0.05,
                "start_date": "2022-01-01",
                "end_date": "2027-01-01",
                "monthly_payment": 188.71,
                "remaining_balance": 7500,
                "dues": 188.71,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Medical Expenses",
                "prepayment_penalty": True,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC112233",
            "account_type": "Savings",
            "account_balance": 5000,
            "account_status": "Active",
            "opened_date": "2018-05-10"
        },
        "credit_score": 720,
        "customer_since": "2015-03-22",
        "last_payment_date": "2024-02-15",
        "next_payment_due": "2024-03-15",
        "payment_method": "Auto Debit"
    },
    {
  "customer_id": "CUST234567",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone": "+1987654321",
  "date_of_birth": "1990-07-20",
  "ssn": "234-56-7890",
  "address": {
    "street": "456 Elm Street",
    "city": "Metropolis",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  },
  "employment_details": {
    "employer_name": "XYZ Inc",
    "job_title": "Financial Analyst",
    "annual_income": 70000,
    "employment_status": "Full-Time",
    "years_employed": 3
  },
  "loan_details": [
    {
      "loan_id": "LN123456",
      "loan_type": "Personal Loan",
      "loan_amount": 15000,
      "loan_term": 48,
      "interest_rate": 0.07,
      "start_date": "2021-06-01",
      "end_date": "2025-06-01",
      "monthly_payment": 358.24,
      "remaining_balance": 9200,
      "dues": 358.24,
      "payment_status": "Active",
      "late_payments": 2,
      "loan_purpose": "Home Renovation",
      "prepayment_penalty": False,
      "collateral_required": False
    }
  ],
  "account_details": {
    "account_id": "ACC445566",
    "account_type": "Checking",
    "account_balance": 3200,
    "account_status": "Active",
    "opened_date": "2019-09-15"
  },
  "credit_score": 690,
  "customer_since": "2017-08-30",
  "last_payment_date": "2025-03-01",
  "next_payment_due": "2025-04-01",
  "payment_method": "Manual Payment"
},
    {
        "customer_id": "CUST654321",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "phone": "+1987654321",
        "date_of_birth": "1990-09-25",
        "ssn": "987-65-4321",
        "address": {
            "street": "456 Elm St",
            "city": "Springfield",
            "state": "TX",
            "zip": "67890",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "XYZ Inc",
            "job_title": "Marketing Manager",
            "annual_income": 95000,
            "employment_status": "Full-Time",
            "years_employed": 3
        },
        "loan_details": [
            {
                "loan_id": "LN123789",
                "loan_type": "Car Loan",
                "loan_amount": 25000,
                "loan_term": 48,
                "interest_rate": 0.045,
                "start_date": "2023-03-01",
                "end_date": "2027-03-01",
                "monthly_payment": 566.14,
                "remaining_balance": 24000,
                "dues": 666.14,
                "payment_status": "Active",
                "late_payments": 1,
                "loan_purpose": "Vehicle Purchase",
                "prepayment_penalty": False,
                "collateral_required": True
            },
            {
                "loan_id": "LN876543",
                "loan_type": "Credit Card Debt",
                "loan_amount": 5000,
                "loan_term": 24,
                "interest_rate": 0.15,
                "start_date": "2022-06-01",
                "end_date": "2024-06-01",
                "monthly_payment": 250,
                "remaining_balance": 2000,
                "dues": 300,
                "payment_status": "Delinquent",
                "late_payments": 3,
                "loan_purpose": "Retail Purchases",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC445566",
            "account_type": "Checking",
            "account_balance": 3000,
            "account_status": "Active",
            "opened_date": "2017-09-15"
        },
        "credit_score": 710,
        "customer_since": "2016-08-10",
        "last_payment_date": "2024-02-20",
        "next_payment_due": "2024-03-20",
        "payment_method": "Manual Payment"
    },
    {
        "customer_id": "CUST112233",
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice.brown@example.com",
        "phone": "+1122334455",
        "date_of_birth": "1992-03-12",
        "ssn": "555-66-7788",
        "address": {
            "street": "789 Maple St",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "ACME Co",
            "job_title": "Data Analyst",
            "annual_income": 70000,
            "employment_status": "Part-Time",
            "years_employed": 2
        },
        "loan_details": [
            {
                "loan_id": "LN332211",
                "loan_type": "Student Loan",
                "loan_amount": 15000,
                "loan_term": 120,
                "interest_rate": 0.035,
                "start_date": "2020-09-01",
                "end_date": "2030-09-01",
                "monthly_payment": 147.89,
                "remaining_balance": 12500,
                "dues": 147.89,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Higher Education",
                "prepayment_penalty": True,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC998877",
            "account_type": "Savings",
            "account_balance": 1500,
            "account_status": "Active",
            "opened_date": "2019-02-01"
        },
        "credit_score": 680,
        "customer_since": "2018-06-15",
        "last_payment_date": "2024-02-10",
        "next_payment_due": "2024-03-10",
        "payment_method": "Auto Debit"
    },
     {
        "customer_id": "CUST445566",
        "first_name": "Robert",
        "last_name": "Johnson",
        "email": "robert.johnson@example.com",
        "phone": "+1445566778",
        "date_of_birth": "1980-11-02",
        "ssn": "444-55-6666",
        "address": {
            "street": "234 Oak Lane",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "Global Solutions",
            "job_title": "Project Manager",
            "annual_income": 105000,
            "employment_status": "Full-Time",
            "years_employed": 7
        },
        "loan_details": [
            {
                "loan_id": "LN556677",
                "loan_type": "Mortgage",
                "loan_amount": 300000,
                "loan_term": 360,
                "interest_rate": 0.03,
                "start_date": "2015-07-01",
                "end_date": "2045-07-01",
                "monthly_payment": 1264.14,
                "remaining_balance": 250000,
                "dues": 1264.14,
                "payment_status": "Active",
                "late_payments": 2,
                "loan_purpose": "Home Purchase",
                "prepayment_penalty": True,
                "collateral_required": True
            },
            {
                "loan_id": "LN667788",
                "loan_type": "Personal Loan",
                "loan_amount": 20000,
                "loan_term": 60,
                "interest_rate": 0.07,
                "start_date": "2020-10-01",
                "end_date": "2025-10-01",
                "monthly_payment": 396.02,
                "remaining_balance": 8000,
                "dues": 396.02,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Debt Consolidation",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC223344",
            "account_type": "Savings",
            "account_balance": 15000,
            "account_status": "Active",
            "opened_date": "2010-04-15"
        },
        "credit_score": 750,
        "customer_since": "2009-08-01",
        "last_payment_date": "2024-03-01",
        "next_payment_due": "2024-04-01",
        "payment_method": "Auto Debit"
    },
    {
        "customer_id": "CUST778899",
        "first_name": "Emily",
        "last_name": "Davis",
        "email": "emily.davis@example.com",
        "phone": "+1778899000",
        "date_of_birth": "1995-02-14",
        "ssn": "777-88-9999",
        "address": {
            "street": "567 Pine St",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "Tech Innovators",
            "job_title": "UX Designer",
            "annual_income": 85000,
            "employment_status": "Full-Time",
            "years_employed": 2
        },
        "loan_details": [
            {
                "loan_id": "LN778899",
                "loan_type": "Student Loan",
                "loan_amount": 50000,
                "loan_term": 120,
                "interest_rate": 0.04,
                "start_date": "2018-09-01",
                "end_date": "2028-09-01",
                "monthly_payment": 506.23,
                "remaining_balance": 30000,
                "dues": 506.23,
                "payment_status": "Active",
                "late_payments": 1,
                "loan_purpose": "Higher Education",
                "prepayment_penalty": False,
                "collateral_required": False
            },
            {
                "loan_id": "LN889900",
                "loan_type": "Credit Card Debt",
                "loan_amount": 8000,
                "loan_term": 24,
                "interest_rate": 0.18,
                "start_date": "2022-01-01",
                "end_date": "2024-01-01",
                "monthly_payment": 400,
                "remaining_balance": 2000,
                "dues": 600,
                "payment_status": "Delinquent",
                "late_payments": 3,
                "loan_purpose": "Retail Purchases",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC334455",
            "account_type": "Checking",
            "account_balance": 2500,
            "account_status": "Active",
            "opened_date": "2017-06-20"
        },
        "credit_score": 690,
        "customer_since": "2016-11-12",
        "last_payment_date": "2024-02-25",
        "next_payment_due": "2024-03-25",
        "payment_method": "Manual Payment"
    }
]
    return json.dumps(customer_details[0])

def get_plans(customer_id:str):

    repayment_plans = { 
        "CUST123456": {
    "1": {
      "plan_name": "Refinance Step Same",
      "new_loan_amount": 10000,
      "new_interest_rate": 0.05,
      "new_loan_term_months": 60,
      "new_monthly_payment": 188.71,
      "cash in hand": 2311.29,
      "benefit": "Cash in hand for current financial situation.",
      "eligibility": "Requires stable income and improved credit score (680+).",
      "negotiation_rules":"No parameters to negotiate try explaining its benefits ",
    },
    "2": {
      "plan_name": "Refinance Step Down",
      
      "new_loan_amount": 9000,
      "new_interest_rate": 0.05,
      "new_loan_term_months": 60,
      "new_monthly_payment": 169.84,
      "cash in hand": 1311.29,
      "benefit": "Cash in hand for current financial situation. montly payment is lower ",
      'calculations': "calculate montly payment and cash_in_hand for change in loan amount",
      "eligibility": "Requires stable income and improved credit score (680+).",
      "negotiation_rules":"Use loan amount as parameter, for each loan amount you must iterate atleast 3 times before going to reducing loan amount by 10% until you reach 8000 (min loan amount)",
    },
    "3": {
      "plan_name": "Refinance Step Up",
      
      "new_loan_amount": 11000,
      "new_interest_rate": 0.05,
      "new_loan_term_months": 60,
      "new_monthly_payment": 207.58,
      "cash in hand": 3311,
      "benefit": "Cash in hand for current financial situation.",
      "disadvantage": "Higher monthly payment.",
      'calculations': "calculate montly payment and cash_in_hand for change in loan amount",
      "eligibility": "Requires stable income and improved credit score (680+).",
      "negotiation_rules":"Use loan amount as parameter, for each loan amount you must iterate atleast 3 times before going to change loan amount by 10% until you reach 15000(max loan amount) ",
    },
    "4": {
      "plan_name": "Extended Payment Plan (4 Cycles)",
      "loan_amount": 10000,
      "new_interest_rate": 0.05,
      "new_loan_term_months": 63,
      "new_monthly_payment": 154.21,
      "benefit": "Lower monthly payments to reduce immediate financial stress.",
      "downside": "Total interest paid will increase due to extended tenure.",
      "eligibility": "Suitable for borrowers with temporary financial hardships.",
      'calculations': "calculate montly payment  for change in tenure",
      "negotiation_rules":"Use cycles to negotiate, add +3 months for each cycle, until you reach 72 months.",
    },
}
    }
    return json.dumps(repayment_plans[customer_id])




tools = [{
        "type": "function",
        "function": {
            "name": "get_customer_details",
            "description": "Get customer details by email",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer email"}
                },
                "required": ["email"]
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
                    "customer_id": {"type": "string", "description": "Customer_id is used to get plans related to that customer"}
                },
                "required": ["customer_id"]
            }
        }
    }
]


prompt = """
Role: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation.

Objective: Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan will reduce their financial burden. Monitor customer sentiment to decide when to stick with a plan or move to an alternative, using data that is coming from function calls only. Do not fabricate any information. If the customer asks for a plan that is not available, tell them that it is not available and offer only what is in the database.

### Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
2. Request the email ID and wait for their response.
3. Call the function `get_customer_info(email_id)` to retrieve customer information once you receive the email.
4. After retrieving customer info, inform them of their due amount (e.g., $X currently due) and ask about their financial situation to better understand their needs and provide tailored help. Ask questions to gauge their income, financial stress, or any other factors affecting their situation.
5. Once you understand their situation, call the function `get_plans(str(customer_id))` to retrieve a suitable plan for the customer.
6. Present only **one plan** as the best option for their current financial status.
7. Never fabricate information or change the plan based on the customer’s statements. Always rely on the data retrieved through function calls.
8. Do not mention the availability of multiple plans. The customer should believe that the plan you present is the only option.
9. Use numbers to explain how the plan will help reduce their financial burden (e.g., reduced monthly payments, lower interest rates, savings over time).
10. Monitor the customer’s sentiment:
   - Positive Sentiment: If the customer is positive or neutral, continue explaining the benefits of the plan using numbers.
   - Unsure Sentiment: If the customer is unsure, attempt to convince them **up to 4 times** using detailed explanations of the plan's benefits.
   - Negative Sentiment or Firm Refusal: If the customer is negative or refuses the plan after **at least 2 attempts**, move to another plan, but **do not reveal that there are other plans available** until switching is necessary.
11. If the customer refuses all plans, provide the customer service contact: `+12123123123`.

### Plan-Specific Negotiation Rules:

1. **Refinance Step Same**:  
   - No parameters for negotiation. Present the plan’s benefits (cash in hand, stable payments) and stick with it for **3 iterations**.
   - Emphasize why it’s the best option for their situation.

2. **Refinance Step Down**:
   - Loan amount is the key parameter to negotiate.
   - Start with the original loan amount (e.g., $9,000). Stick with it for **3 iterations**.
   - If the customer refuses, reduce the loan amount by 10% and repeat the negotiation until you reach the minimum loan amount of $8,000.

3. **Refinance Step Up**:
   - Similar to Refinance Step Down, but start with a higher loan amount (e.g., $11,000).
   - Stick with the initial loan amount for **3 iterations** before increasing it by 10% for each step until you reach the maximum loan amount of $15,000.

4. **Extended Payment Plan (4 Cycles)**:
   - The negotiation parameter is the loan term.
   - Start with the initial loan term (e.g., 63 months). Stick with this term for **3 iterations**.
   - If the customer refuses, extend the loan term by 3 months (e.g., from 63 to 66 months) and repeat the process until reaching a maximum term of 72 months.

### Sentiment and Threshold Rules:
- **Threshold** represents how many times you can try to convince the customer about the current plan.
- **Threshold should be set between 1 and 5**:
   - Stick with a plan for **at least 2 attempts**.
   - If the customer is unsure or confused, persist with the plan for up to **4 attempts**.
   - Only change to another plan after the customer refuses **firmly or negatively** after **at least 2 attempts**.

### Negotiation Style:
- **Be factual**: Always use data from function calls (e.g., interest rate, loan amount, monthly payments).
- **Persistence**: Stick to one plan and negotiate within the defined **threshold**.
- **Confidence**: Present the plan as the **best option**, and emphasize how it reduces the customer’s financial burden.
- **Empathy**: Acknowledge the customer’s situation, but remain firm in offering the only available plan for their current status.
- **Exclusive Tone**: Present the plan as the only solution for the customer’s financial needs.
- **Sentiment-Driven**: Use the customer’s sentiment to decide how long to stick with the plan before switching.

### Example Workflow:
1. Greet and Request Email: “Hello! How can I assist you today? May I please have your email so I can look into your details?”
2. Retrieve Customer Info: Call `get_customer_info(email_id)` and get their due amount, say: “Thank you for your email. It looks like you currently have a due amount of $X. How is your financial situation? We’re here to help.” Ask further questions to understand their income, financial stress, or credit score.
3. Retrieve Plan and Present It: Call `get_plans(str(customer_id))` and present only **one plan**. For example: “Based on your situation, we recommend the Refinance Step Same plan. This will reduce your monthly payment to $188.71, and you’ll also get $2,311.29 in cash to ease your immediate financial stress.”
4. Customer Sentiment:
   - If the customer is unsure: “I understand this might seem like a lot, but this plan will lower your payments by $200 per month, which could help you manage your finances.”
   - If they are firm in refusal after multiple attempts: “I understand, let’s look at another option that may work better for you.”
5. Negotiate: Stick with the current plan for **at least 2 attempts** before moving on. Adjust **loan amount or tenure** according to the plan-specific rules and persist for **3 iterations**.


### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
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
                response = get_customer_details()
                
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