from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
client = Together()

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
                "dues": 308.71,
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

    return json.dumps(customer_details[random.randint(0,4)])

def get_plans(customer_id:str):
    repayment_plans = {
 "CUST445566":{
  "plans": [
    {
      "plan_id": 1,
      "name": "Refinance Plan",
      "priority": 1,
      "description": "Refinance existing loans with new terms to reduce monthly payments or extend the loan tenure.",
      "options": [
        {
          "option_name": "Refinance Step Same",
          "description": "Keep interest rate and tenure the same, loan amount equals remaining balance + dues + 10% buffer.",
          "negotiation_parameters": "No specific parameters.",
          "tailored_message": "A stable option with predictable payments for your mortgage."
        },
        {
          "option_name": "Refinance Step Down",
          "description": "Lower the loan amount by up to 30%.",
          "negotiation_parameters": "Negotiate loan decrease percentage in steps of 10%.",
          "tailored_message": "Reduce your loan burden significantly while keeping manageable payments."
        },
        {
          "option_name": "Refinance Step Up",
          "description": "Increase the loan amount by up to 20% to cover immediate needs.",
          "negotiation_parameters": "Negotiate loan increase percentage in steps of 5%.",
          "tailored_message": "A flexible option to cover short-term needs."
        }
      ],
      "negotiation_rules": [
        "Begin with Refinance Step Same to emphasize predictable payments.",
        "Switch to Step Down after 1 rejection to highlight long-term savings.",
        "Never combine refinance options or reveal alternative plans."
      ]
    },
    {
      "plan_id": 2,
      "name": "Extended Payment Plan",
      "priority": 2,
      "description": "Restructure mortgage or personal loan to extend repayment timeline and reduce monthly payments.",
      "options": [
        {
          "option_name": "EPP up to 24 cycles",
          "description": "Extend loan tenure by 6/12/18/24 cycles.",
          "negotiation_parameters": "Negotiate the number of cycles extended based on financial strain.",
    
          "tailored_message": "Extend payments for more breathing room in your budget."
        }
      ],
      "negotiation_rules": [
        "Focus on the mortgage first for significant impact on finances.",
        "Show how each extension reduces monthly payments step-by-step.",
        "Offer shorter extensions initially (6 cycles), increasing after rejections.",
        "Highlight how this avoids loan default and protects credit score."
      ]
    },
    {
      "plan_id": 3,
      "name": "Settlement Plan with Waive-Off",
      "priority": 3,
      "description": "Settle personal loan by waiving fees, interest, or a portion of the principal.",
      "options": [
        {
          "option_name": "Waive Interest (up to 30%)",
          "description": "Negotiate interest waiver percentage starting at 10%.",
          "negotiation_parameters": "Adjust waiver percentage based on financial history.",
          
          "tailored_message": "Reduce your personal loan burden quickly with interest waivers."
        },
        {
          "option_name": "Waive Principal (up to 10%)",
          "description": "Negotiate principal waiver percentage starting at 5%.",
          "negotiation_parameters": "Increase waiver based on negotiation progress.",
          
          "tailored_message": "Save significantly by reducing the loan principal."
        }
      ],
      "negotiation_rules": [
        "Start with fee or interest waivers for easier approvals.",
        "Offer principal waivers only after 2 rejections.",
        "Emphasize fast loan closure benefits and credit score protection.",
        
      ]
    }
  ]
},
"CUST778899":{
  "plans": [
    {
      "plan_id": 1,
      "name": "Refinance Plan",
      "priority": 2,
      "description": "Refinance student loans or credit card debt with new terms for better affordability.",
      "options": [
        {
          "option_name": "Refinance Step Same",
          "description": "Keep interest rate and tenure the same, adjusting loan amount.",
          "negotiation_parameters": "Focus on minimal changes to structure.",
          
          "tailored_message": "A stable refinancing option for predictable payments."
        },
        {
          "option_name": "Refinance Step Down",
          "description": "Reduce loan amount by 20% for immediate relief.",
          "negotiation_parameters": "Negotiate reduction in steps of 5%.",
          
          "tailored_message": "Lower your financial burden while keeping terms simple."
        }
      ],
      "negotiation_rules": [
        "Start with student loan refinancing for long-term benefits.",
        "After 1 rejection, switch to credit card debt for faster relief.",
        "Use data to demonstrate how refinancing improves affordability.",
        "Avoid revealing other options during initial discussions."
      ]
    },
    {
      "plan_id": 2,
      "name": "Extended Payment Plan",
      "priority": 1,
      "description": "Extend repayment schedules for more manageable monthly payments.",
      "options": [
        {
          "option_name": "EPP up to 12 cycles",
          "description": "Extend tenure by 3/6/9/12 cycles.",
          "negotiation_parameters": "Negotiate extension based on remaining balance.",
          
          "tailored_message": "Flexible extensions tailored to your financial needs."
        }
      ],
      "negotiation_rules": [
        "Prioritize credit card debt to avoid delinquency penalties.",
        "Offer shorter extensions (3-6 cycles) initially.",
        "Highlight monthly payment relief for current delinquent accounts.",
        "Use real numbers to demonstrate financial savings."
      ]
    },
    {
      "plan_id": 3,
      "name": "Settlement Plan with Waive-Off",
      "priority": 3,
      "description": "Negotiate debt settlement for credit card loan with partial waivers.",
      "options": [
        {
          "option_name": "Waive Fees up to 100%",
          "description": "Negotiate fee waiver percentage starting at 30%.",
          "negotiation_parameters": "Increase waiver incrementally to 100%.",
          
          "tailored_message": "Eliminate fees to quickly resolve debt issues."
        },
        {
          "option_name": "Waive Interest (up to 50%)",
          "description": "Negotiate interest waivers to reduce repayment burden.",
          "negotiation_parameters": "Adjust based on delinquency history.",
          
          "tailored_message": "Cut down your debt faster with interest waivers."
        }
      ],
      "negotiation_rules": [
        "Start with interest or fee waivers to minimize out-of-pocket expenses.",
        "Avoid principal reductions unless requested by the customer.",
        "Reiterate benefits of debt settlement and improved credit scores.",
        
      ]
    }
  ]
},
 "CUST123456":{
      "plans": [
        {
          "plan_id": 1,
          "name": "Refinance Plan",
          "priority": 2,
          "description": "Refinance home loans to reduce payments or adjust tenure.",
          "options": [
            {
              "option_name": "Refinance Step Same",
              "description": "Keep interest and tenure unchanged, adjust loan amount.",
              "negotiation_parameters": "Start with balance + fees + 10%.",
              
            },
            {
              "option_name": "Refinance Step Down",
              "description": "Reduce loan amount by up to 25%.",
              "negotiation_parameters": "Negotiate in steps of 5%.",
              
            }
          ],
          "negotiation_rules": [
            "Start with Step Same for stable payments.",
            "Switch to Step Down if rejected twice.",
            
          ]
        },
        {
          "plan_id": 2,
          "name": "Extended Payment Plan",
          "priority": 1,
          "description": "Extend repayment for smaller installments.",
          "options": [
            {
              "option_name": "EPP up to 12 cycles",
              "description": "Extend tenure by 6/9/12 months.",
              "negotiation_parameters": "Offer minimal extension first.",
              
            }
          ],
          "negotiation_rules": [
            "Focus on monthly relief.",
            "Use short extensions first, longer after rejections.",
            
          ]
        }
      ]
    },
    
     "CUST234567":{
      "plans": [
        {
          "plan_id": 3,
          "name": "Settlement Plan with Waive-Off",
          "priority": 3,
          "description": "Settle personal loans with waivers.",
          "options": [
            {
              "option_name": "Waive Fees up to 50%",
              "description": "Reduce fees for delinquent accounts.",
              "negotiation_parameters": "Start at 20% and increase to 50%.",
              
            },
            {
              "option_name": "Waive Interest (up to 40%)",
              "description": "Negotiate interest reductions.",
              "negotiation_parameters": "Start at 10%, increase gradually.",
              
            }
          ],
          "negotiation_rules": [
            "Begin with fees, progress to interest.",
            "Emphasize total savings and faster repayment.",
            "Avoid combining options initially."
          ]
        }
      ]
    },
     "CUST445566":{
      "plans": [
        {
          "plan_id": 1,
          "name": "Refinance Plan",
          "priority": 1,
          "description": "Refinance existing loans with optimized terms.",
          "options": [
            {
              "option_name": "Refinance Step Same",
              "description": "Keep loan terms the same but restructure amount.",
              "negotiation_parameters": "Balance + fees.",
              
            },
            {
              "option_name": "Refinance Step Down",
              "description": "Reduce the loan by 20%.",
              "negotiation_parameters": "Negotiate reductions in 5% increments.",
              
            }
          ],
          "negotiation_rules": [
            "Highlight immediate monthly savings.",
            "Use Step Down after rejection.",
            
          ]
        },
        {
          "plan_id": 3,
          "name": "Settlement Plan with Waive-Off",
          "priority": 2,
          "description": "Settle credit card debt with fee waivers.",
          "options": [
            {
              "option_name": "Waive Fees up to 100%",
              "description": "Negotiate complete fee elimination.",
              "negotiation_parameters": "Increase gradually.",
            
            }
          ],
          "negotiation_rules": [
            "Begin with 50% fee waivers.",
            "Highlight the impact on overdue balance.",
            "Emphasize quick closure benefits."
          ]
        }
      ]
    },
     "CUST778899":{
      "plans": [
        {
          "plan_id": 2,
          "name": "Extended Payment Plan",
          "priority": 1,
          "description": "Extend repayment schedules to reduce monthly strain.",
          "options": [
            {
              "option_name": "EPP up to 24 cycles",
              "description": "Offer extensions by 6/12/18/24 cycles.",
              "negotiation_parameters": "Start with shorter terms first.",
            
            }
          ],
          "negotiation_rules": [
            "Focus on credit card debt first.",
            "Use short extensions initially.",
            "Show direct financial impact using numbers."
          ]
        },
        {
          "plan_id": 1,
          "name": "Refinance Plan",
          "priority": 2,
          "description": "Optimize student loans with refinancing.",
          "options": [
            {
              "option_name": "Refinance Step Down",
              "description": "Reduce principal by 15%.",
              "negotiation_parameters": "Offer reductions incrementally.",
            
            }
          ],
          "negotiation_rules": [
            "Prioritize cost savings.",
            "Avoid combining options.",
            "Explain terms clearly with comparisons."
          ]
        }
      ]
    }
}


    

    return json.dumps(repayment_plans[customer_id][priority])

def make_cal(principal, annual_rate, years):
    """
    Calculate the monthly payment for a loan.

    :param principal: The total loan amount (P)
    :param annual_rate: The annual interest rate in percentage (e.g., 5 for 5%)
    :param years: The loan term in years
    :return: Monthly payment amount (M)
    """
    monthly_rate = (annual_rate / 100) / 12  
    num_payments = years * 12  
    if monthly_rate == 0:
        return principal / num_payments
    monthly_payment = (principal * monthly_rate * (1 + monthly_rate) ** num_payments) / \
                      ((1 + monthly_rate) ** num_payments - 1)
    
    return round(monthly_payment, 2)

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
                    "customer_id": {"type": "numeric", "description": "use this to get the financial plans of a customer"},
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_cal",
            "description": "Makes calculations needed for the financial plans",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {"type": "numeric", "description": "This is the new loan amount"},
                    "interest_rate": {"type": "numeric", "description": "This is the interest rate"},
                    "loan_duration": {"type": "numeric", "description": "This is the loan duration"},
                },
                "required": ["loan_amount","interest_rate","loan_duration"]
            },
            "return": {
                "montly_payment": {"type": "numeric", "description": "This is new monthly payment"}
            }
        }
    }
    ]

prompt = """

**Role**: You are a Customer Service Representative for Cognute Bank. You are responsible for negotiating with customers to accept a single plan that fits their financial situation.

### Objective:
Convince the customer to accept **one plan**. Present it as the **best and only option**. Use numbers to show how the plan will reduce their financial burden. **Monitor customer sentiment** and decide when to stick with a plan or move to an alternative, but never reveal multiple plans.

### Instructions:
1. **Greet the customer** and ask how you can assist them.
2. **Request their email ID** and **wait for a response**.
3. Call the function **`get_customer_details(email)`** to retrieve customer information only once.
4. After retrieving the customer info, **present their due amount** and ask about their current financial situation to better assist them.
5. Once the customer explains their situation, **call the function `get_plans(str(customer_id))`** to retrieve the list of plans the company offers.
6. **Use one plan at a time**, based on the retrieved data, and present it confidently as the only solution.
7. For each negotiation:
    - Start with **one option** from the plan and explain its benefits using specific numbers (e.g., monthly payments, total interest).
    - Use **make_cal** for calculations (monthly payments, interest savings, etc.).
    - **Monitor customer sentiment**:
      - **Positive/Neutral**: Stick with the current offer and emphasize its benefits using numbers.
      - **Unsure/Confused**: Repeat the benefits up to **4 times**, calculating the impact of the plan on the customer's finances.
      - **Negative/Firm Refusal**: After **at least 2 attempts**, switch to another option within the same plan.
    - Never mention other plans unless the customer firmly rejects the current one.
8. **Reiterate the plan’s benefits** up to **4 times**, using customer sentiment and numerical data.
9. **If all plans are rejected**, provide the customer service number: `+12123123123`.

### Negotiation Strategy:
- **Start Strong**: Present a strong initial offer from the plan.
- **Use Numbers**: Always use monthly payment and interest savings to demonstrate the benefits of the plan.
- **Monitor Sentiment**: Adjust the negotiation based on positive, neutral, or unsure sentiment.
- **Reiterate**: If unsure, continue reiterating the current plan.
- **Exclusive Plan**: Never reveal multiple plans; present one at a time.
- **Empathy**: Understand the customer’s situation, but remain firm on the plan presented.
- **Persistence**: Continue explaining the same plan until rejection.

### Example Scenario:
1. **Greet & Request Email**: “Hello! How can I assist you today? May I please have your email so I can look into your details?”
2. **Retrieve Customer Info**: Call `get_customer_info(email)` to get customer details.
3. **Present Due Amount**: “It looks like you have a due amount of $X. Could you share more about your current financial situation?”
4. **Get Plan**: Call `get_plans(customer_id)` to get the appropriate plan.
5. **Present the Plan**: Present **only one option** and explain its benefits with numbers.
6. **Customer Sentiment**:
   - If **unsure**: “This plan reduces your payments by $X monthly. It’s a great solution to help you manage your finances better.”
   - If **positive/neutral**: “This plan has great benefits, and I’m sure it will help relieve financial stress.”
   - If **negative** after two attempts: Switch to another option within the same plan.

Remember, your goal is to convince the customer that this is the best option for them without fabricating any information. Use only the data and tools available, and handle the conversation with patience and professionalism.

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
            temperature=0.3,
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