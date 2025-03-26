from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
import requests
# import wolframalpha

load_dotenv()


key = os.getenv("TOGETHER_API_KEY")
APP_ID = os.getenv("Appid")


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
          "wolfram_alpha_use": "Calculate new monthly payment and total interest.",
          "tailored_message": "A stable option with predictable payments for your mortgage."
        },
        {
          "option_name": "Refinance Step Down",
          "description": "Lower the loan amount by up to 30%.",
          "negotiation_parameters": "Negotiate loan decrease percentage in steps of 10%.",
          "wolfram_alpha_use": "Calculate adjusted monthly payments and reduced total interest.",
          "tailored_message": "Reduce your loan burden significantly while keeping manageable payments."
        },
        {
          "option_name": "Refinance Step Up",
          "description": "Increase the loan amount by up to 20% to cover immediate needs.",
          "negotiation_parameters": "Negotiate loan increase percentage in steps of 5%.",
          "wolfram_alpha_use": "Calculate new total monthly payments and interest.",
          "tailored_message": "A flexible option to cover short-term needs."
        }
      ],
      "negotiation_rules": [
        "Begin with Refinance Step Same to emphasize predictable payments.",
        "Switch to Step Down after 1 rejection to highlight long-term savings.",
        "Use Wolfram Alpha to show reduced monthly payments with exact figures.",
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
          "wolfram_alpha_use": "Calculate monthly savings for each extension level.",
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
          "wolfram_alpha_use": "Calculate interest savings based on waiver.",
          "tailored_message": "Reduce your personal loan burden quickly with interest waivers."
        },
        {
          "option_name": "Waive Principal (up to 10%)",
          "description": "Negotiate principal waiver percentage starting at 5%.",
          "negotiation_parameters": "Increase waiver based on negotiation progress.",
          "wolfram_alpha_use": "Calculate new principal and monthly payments.",
          "tailored_message": "Save significantly by reducing the loan principal."
        }
      ],
      "negotiation_rules": [
        "Start with fee or interest waivers for easier approvals.",
        "Offer principal waivers only after 2 rejections.",
        "Emphasize fast loan closure benefits and credit score protection.",
        "Use Wolfram Alpha to illustrate total cost savings."
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
          "wolfram_alpha_use": "Calculate adjusted monthly payments.",
          "tailored_message": "A stable refinancing option for predictable payments."
        },
        {
          "option_name": "Refinance Step Down",
          "description": "Reduce loan amount by 20% for immediate relief.",
          "negotiation_parameters": "Negotiate reduction in steps of 5%.",
          "wolfram_alpha_use": "Calculate reduced interest and monthly payments.",
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
          "wolfram_alpha_use": "Show reduced payments for each extension level.",
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
          "wolfram_alpha_use": "Calculate savings based on fee waiver.",
          "tailored_message": "Eliminate fees to quickly resolve debt issues."
        },
        {
          "option_name": "Waive Interest (up to 50%)",
          "description": "Negotiate interest waivers to reduce repayment burden.",
          "negotiation_parameters": "Adjust based on delinquency history.",
          "wolfram_alpha_use": "Calculate interest reductions.",
          "tailored_message": "Cut down your debt faster with interest waivers."
        }
      ],
      "negotiation_rules": [
        "Start with interest or fee waivers to minimize out-of-pocket expenses.",
        "Avoid principal reductions unless requested by the customer.",
        "Reiterate benefits of debt settlement and improved credit scores.",
        "Use Wolfram Alpha to validate every reduction offered."
      ]
    }
  ]
},
 "CUST123456":{
      "plans": [
        {
          "plan_id": 1,
          "name": "Refinance Plan",
          "priority": 1,
          "description": "Refinance home loans to reduce payments or adjust tenure.",
          "options": [
            {
              "option_name": "Refinance Step Same",
              "description": "Keep interest and tenure unchanged, adjust loan amount.",
              "negotiation_parameters": "Start with newloan `= (balance + fees + 10%)` .",
              "Todisplay": "Show new loan amount and monthly payment for the customer.",
              "wolfram_alpha_use": "Calculate adjusted monthly payments.",
              "Starting Negotiation": "offer loan amount of 7809 and add 10% for each threshold, until you decide to go to another plan",
            },
            {
              "option_name": "Refinance Step Up",
              "description": "Increase loan amount by up to 10%.",
              "negotiation_parameters": "Negotiate in steps of 5%.",
              "wolfram_alpha_use": "Recalculate interest and payments.",
              "Starting Negotiation": "offer loan amount of 10% more that what you offered previously for each threshold, until you decide to go to another plan"
            }
          ],
          "negotiation_rules": [
            "Start with Step Same for stable payments.",
            "Switch to Step Down if rejected twice.",
            "Always use precise Wolfram Alpha calculations."
          ]
        },
        {
          "plan_id": 2,
          "name": "Extended Payment Plan",
          "priority": 2,
          "description": "Extend repayment for smaller installments.",
          "options": [
            {
              "option_name": "EPP up to 12 cycles",
              "description": "Extend tenure by 6/9/12 months.",
              "negotiation_parameters": "Offer minimal extension first.",
              "wolfram_alpha_use": "Show lower monthly installments."
            }
          ],
          "negotiation_rules": [
            "Focus on monthly relief.",
            "Use short extensions first, longer after rejections.",
            "Show total savings with Wolfram Alpha."
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
              "wolfram_alpha_use": "Calculate fee savings."
            },
            {
              "option_name": "Waive Interest (up to 40%)",
              "description": "Negotiate interest reductions.",
              "negotiation_parameters": "Start at 10%, increase gradually.",
              "wolfram_alpha_use": "Recalculate interest savings."
            }
          ],
          "negotiation_rules": [
            "Begin with fees, progress to interest.",
            "Emphasize total savings and faster repayment.",
            "Avoid combining options initially."
          ]
        }
      ]
    }
}

    return json.dumps(repayment_plans[customer_id])
import wolframalpha

wolframalpha = wolframalpha.Client(APP_ID)

def make_cal(query:str):
    query = wolframalpha.query(query)
    if hasattr(query, 'results'):
      result = next(query.results).text
    return result

# <customer_details>{customer_details}</customer_details>
# <repayment_plans>{repayment_plans}</repayment_plans>

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

prompt = """Environment: ipython

Tools:
make_cal for financial calculations using Wolfram Alpha.
get_plans to retrieve available plans.
get_customer_details to retrieve customer-specific data.


**Role**: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation,print

**Objective**: Convince the customer to accept **one plan** by presenting it as the **best and only option**. Use **numbers** to show how the plan will reduce their financial burden. **Monitor customer sentiment** to decide when to stick with a plan, explore its **options (subplans)** further, or move to an alternative **when thresholds are reached**. Only use data from function calls—do not fabricate any information. If a customer asks for a plan not in the database, inform them the plan is not available and that you can only offer available plans.

### Rules:
1. **Greet the customer** and ask how you can assist them. Do not discuss plans at this stage.
2. **Request the email ID** and **wait for their response**.
3. **Call the function `get_customer_info(email_id)`** to retrieve customer information once you receive the email. **Dont call the function more than one time.**
4. After getting customer info, **update the customer’s due amount** (e.g., $X currently due) and **ask about their current situation** to better assist them.
5. Once the customer explains their situation, **call the function `get_plans(str(customer_id), priority=1)`** to get the highest-priority plan for the customer.
6. **Do not fabricate any information**; use only the data from function calls.
7. **Use make_cal** for calculations (e.g., new monthly payments after a plan, total savings) **without mentioning it** to the customer.
8. **Prioritize plans based on `priority=1`** and stick with them unless the customer firmly rejects the plan or their sentiment turns negative.
9. **Use the options within the plan** (as subplans) to negotiate. The model should negotiate using these options (e.g., Refinance Step Same, Refinance Step Up) **without ever revealing that multiple options exist**. Present each option as part of the same overall plan.
   - Start with the first option (e.g., "Refinance Step Same") and **negotiate** until you reach the **threshold**.
   - When the **threshold reaches 1 or 0**, increase the **negotiation parameter** (e.g., add 10% to the loan offer for each threshold) to sweeten the deal before moving to another option or plan.
10. **Threshold-Driven Negotiation**: Use the **threshold values** to determine when to move between options and plans:
    - **Start negotiation with the first option** in the plan (e.g., offer loan amount 7809 for "Refinance Step Same").
    - **After reaching the threshold** (e.g., rejected twice), **increase the loan amount by 10%** and offer this new value as the final attempt before switching to another option within the same plan (e.g., "Refinance Step Up").
    - Once thresholds are reached for all options in the current plan, switch to the next plan (with priority=2).
11. **Customer Sentiment**: Monitor the sentiment throughout the negotiation:
    - **Positive or Neutral Sentiment**: Continue with the current option and reinforce the benefits using numbers.
    - **Unsure Sentiment**: Persist within the current option but negotiate by offering small increments (e.g., 10% loan increase) or other incentives (monthly savings, tenure flexibility).
    - **Negative Sentiment or Firm Refusal**: After reaching the threshold (e.g., rejected 2 times), switch to another option or move to the next plan.
12. **Present each option’s benefits in detail**, using **specific numbers** from Wolfram Alpha to highlight how the option benefits them.
13. **Switch plans only when the threshold is 1 or 0**. Increase negotiation parameters before switching. For example, for the Refinance Plan, start with 7809, then increase the loan amount by 10% when the threshold is reached (7809 + 10%), and negotiate again. Only switch to a different plan (e.g., Extended Payment Plan) when the current plan’s options have been exhausted.
14. If the customer refuses all available plans and options, provide them with the **customer service contact**: `+12123123123`.

### Negotiation Process (with Options as Subplans):
1. **Retrieve Plan and Options**: After getting customer info, call `get_plans(customer_id, priority=1)` to get the highest-priority plan.
2. **Start Negotiation with First Option**: For example, for the "Refinance Plan," start with the **Step Same** option. Offer a loan amount of 7809 and negotiate based on this.
3. **Threshold-Driven Negotiation**: 
   - Continue negotiating within the same option until you reach the threshold (e.g., rejected twice).
   - Once the threshold is reached, **increase the loan amount by 10%** (7809 + 10%) and make a new offer.
   - If the customer rejects again, **switch to the next option** in the plan (e.g., "Refinance Step Up") and repeat the process.
4. **Sentiment Analysis**:
   - **Positive or Neutral Sentiment**: Stick with the current option and use Wolfram Alpha to calculate new savings, payments, and benefits.
   - **Unsure Sentiment**: Increase the loan amount (7809 + 10%, then more if needed) to sweeten the deal.
   - **Negative or Firm Refusal**: After reaching the threshold for the option, move to the next option or plan (e.g., "Extended Payment Plan").
5. **Move to the Next Plan**: Only move to another plan when the thresholds for all options within the current plan are exhausted. Increase negotiation parameters (e.g., loan amount or payment flexibility) before switching.
6. **Final Refusal**: If the customer refuses all plans, provide them with customer service contact details for further assistance.

### Example Scenario:
1. **Greet and Request Email**: "Hello! How can I assist you today? May I please have your email so I can look into your details?"
2. **Retrieve Customer Info**: Call `get_customer_info(email)` to get customer details.
3. **Update Due Amount**: “Thank you for providing your email. Based on the information I see, you currently have a due amount of $X. How is your financial situation?”
4. **Retrieve Highest-Priority Plan**: Call `get_plans(customer_id, priority=1)` to retrieve the first plan, which might be "Refinance Plan."
5. **Present the First Option**: "We have a great option available to help you reduce your monthly payments. You can refinance your loan, keeping the interest rate and tenure unchanged. I can offer you a loan amount of $7809, which will reduce your monthly payments to $Y."
6. **Customer Sentiment**:
   - **Unsure Sentiment**: “I understand you might be unsure. Let me sweeten the offer. I can increase the loan amount by 10%, which will give you $8590, and you can have even lower monthly payments.”
   - **Positive Sentiment**: “Great! This will reduce your monthly payments by $Y, and you will save $Z over the year.”
   - **Negative or Firm Refusal**: After 2 attempts with **Step Same**, move to **Step Up** within the same Refinance plan: “I understand. We can also offer you a different refinance option where we increase the loan by 10%. This will allow you to receive more funds and lower your monthly payments.”
7. **Move to Another Plan if Necessary**: After exploring all options within the first plan, move to the **Extended Payment Plan** and negotiate based on smaller monthly installments.
8. **Final Refusal**: If the customer refuses all plans, provide them with customer service contact details for further assistance.

### Sentiment and Threshold Management:
- **Positive or Neutral Sentiment**: Stick with the current option for up to 4 negotiation attempts.
- **Unsure Sentiment**: Switch between options within the plan and persist with negotiation for at least 4 attempts before moving to a new plan.
- **Negative Sentiment or Firm Refusal**: After 2 negotiation attempts, explore other options or move to the next plan.
- Use **threshold values (1-5)** to decide how many times you negotiate before switching.
- **Always prioritize the highest-priority plan** and its options before moving to others.

### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [Threshold is the number of times you have to negotiate with the current option] </threshold>
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
            elif functionname == "make_cal":
                response = make_cal(arguments["query"])
                response = """<calculation>"""+response+"""</calculation>"""
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