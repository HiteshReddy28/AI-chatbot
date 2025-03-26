from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
import requests
import wolframalpha

load_dotenv()


key = os.getenv("TOGETHER_API_KEY")
APP_ID = os.getenv('Appid')


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
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest and tenure unchanged, Same loan amount.",
      "options": [
        {
          "option_name": "Same Loan Amount Refinance",
          "description": "Refinance with the same loan amount as previously taken.",
          "negotiation_parameters": "Start with the same loan as taken previously.",
          "make_cal_use": "use make_cal to Calculate in-hand amount and new tenure end date.",
          "Todisplay": "Show new loan amount, monthly payment, and in-hand cash for the customer.",
          "example": "If customer is having remaining balance of X$ but took a loan of Y$ then offer him to refinance with total loan amount that is Y$ and calculate how much he gets with the new loan.",
        }
      ],
      "negotiation_rules": [
        "Start with stable payment options.",
        "Ensure customer retains the same interest rate.",
        "Provide clear monthly payment details."
      ]
    },
    {
      "plan_id": 2,
      "name": "Refinance Step Up 10%",
      "priority": 2,
      "description": "Increase loan amount by 10% and adjust payments.",
      "options": [
        {
          "option_name": "Step Up Loan 10%",
          "description": "Increase loan amount by 10% of the previously offered loan amount.",
          "negotiation_parameters": "Negotiate in steps of 5%.",
          "make_cal_use": "Calculate new interest, monthly payment, and additional cash in hand.",
          "example": {
            "previous_loan_amount": 5000,
            "increased_amount": 500,
            "new_loan_amount": 5500,
            "additional_cash_in_hand": 2000
          }
        }
      ],
      "negotiation_rules": [
        "Offer in 10% increments.",
        "Limit negotiation to 50% total increase.",
        "Always prioritize clear payment details."
      ]
    },
    {
      "plan_id": 3,
      "name": "Refinance Step Up 20%",
      "priority": 3,
      "description": "Increase loan amount by 20% and adjust payments.",
      "options": [
        {
          "option_name": "Step Up Loan 20%",
          "description": "Increase loan amount by 20% of the previously offered loan amount.",
          "negotiation_parameters": "Negotiate in steps of 10%.",
          "make_cal_use": "Calculate new interest, monthly payment, and additional cash in hand.",
          "example": {
            "previous_loan_amount": 5000,
            "increased_amount": 1000,
            "new_loan_amount": 6000,
            "additional_cash_in_hand": 2500
          }
        }
      ],
      "negotiation_rules": [
        "Offer in 10% increments.",
        "Limit negotiation to 50% total increase.",
        "Provide clear monthly payment and interest adjustments."
      ]
    },
    {
      "plan_id": 4,
      "name": "Extended Payment Plan 3 Months",
      "priority": 4,
      "description": "Extend repayment period by 3 months for smaller installments.",
      "options": [
        {
          "option_name": "EPP 3 Months",
          "description": "Extend repayment period by 3 months.",
          "negotiation_parameters": "Offer minimal extension first.",
          "make_cal_use": "Calculate lower monthly installments over the extended period.",
          "example": {
            "previous_monthly_payment": 500,
            "new_monthly_payment": 400,
            "extension_period": 3
          }
        }
      ],
      "negotiation_rules": [
        "Focus on minimal extensions.",
        "Highlight reduced monthly payments.",
        "Provide savings details with extended period."
      ]
    },
    {
      "plan_id": 5,
      "name": "Extended Payment Plan 6 Months",
      "priority": 5,
      "description": "Extend repayment period by 6 months for smaller installments.",
      "options": [
        {
          "option_name": "EPP 6 Months",
          "description": "Extend repayment period by 6 months.",
          "negotiation_parameters": "Start with medium extension if short is rejected.",
          "make_cal_use": "Calculate lower monthly installments over the extended period.",
          "example": {
            "previous_monthly_payment": 500,
            "new_monthly_payment": 350,
            "extension_period": 6
          }
        }
      ],
      "negotiation_rules": [
        "Offer medium extensions after rejection of short periods.",
        "Show reduced financial burden.",
        "Emphasize overall savings."
      ]
    },
    {
      "plan_id": 6,
      "name": "Extended Payment Plan 12 Months",
      "priority": 6,
      "description": "Extend repayment period by 12 months for smaller installments.",
      "options": [
        {
          "option_name": "EPP 12 Months",
          "description": "Extend repayment period by 12 months.",
          "negotiation_parameters": "Offer longer extensions as a last resort.",
          "make_cal_use": "Calculate lower monthly installments over the extended period.",
          "example": {
            "previous_monthly_payment": 500,  
            "new_monthly_payment": 250,
            "extension_period": 12
          }
        }
      ],
      "negotiation_rules": [
        "Reserve longer extensions for final offers.",
        "Provide clear comparisons of financial impact.",
        "Emphasize affordability with longer terms."
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


Wolfram_client = wolframalpha.Client(APP_ID)

def make_cal(query:str):
    query = Wolfram_client.query(query)
    print(query)
    if hasattr(query, 'results'):
      result = next(query.results).text
    return result

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

prompt = """
Tools:
- get_plans: to retrieve available plans. (ONLY ONCE)
- get_customer_info: to retrieve customer-specific data. (ONLY ONCE)
- make_cal: for financial calculations using Wolfram Alpha.


####Role:
You're a Senior Customer Negootiator at Cognute Bank, You're responsible to maximize the lenders benifit at the same time understanding the customer situation and make a conversation in a polite and respectful manner.

###Objective:
Convince the customer to accept one plan by presenting it as the best option. Use numbers to show how the plan will reduce their financial burden. Monitor customer sentiment to decide when to stick with a plan or move to another. Use the make_cal function for every calculation and use only data retrieved from function calls.

###Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
2. Request the email ID and wait for their response.
3. **Call get_customer_info(email_id)** to retrieve customer information ONLY once only once. 
4. Once you have the customer info, provide the customer’s due amount (e.g., $X currently due) and ask about their current financial situation to better assist them.
5. **Call get_plans(str(customer_id))** only once after the customer explains their situation to retrieve all available plans in priority order for the customer, Initial values for Customer_threshold and Current_threshold is zero.
6. Use the plan with the highest priority first and do not move to another plan unless Current_threshold is equal to Customer_threshold, Determine Customer_threshold based on customer sentiment.
7. For each plan, do not reveal that multiple plans exist even if the customer asks.Stick to the plan you are currently discussing. If the customer asks about other plans, say that you are not aware of any other plans that would be better for them.  
8. Use make_cal to calculate numbers like new monthly payments, total savings, etc., for every calculation required, without revealing the use of this function.
9. Stick to your plan until Current_threshold is reached to Customer_threshold, then move to the next plan. If the customer is satisfied with the plan, do not move to another plan. if you change the plan then reset Current_threshold to zero.
10. Dont change the plan until you Current_threshold is equal to Customer_threshold, even if customer is not willing to listen you need to stick to the same plan, if both thresholds are equal then change the plan and reset Current_threshold to zero.
11. Negotiate based on the plan’s details before moving to another plan.
   - Thresholds: you need to sets threshold based on customer sentiment.
   - Threshold-Driven Negotiation: Use thresholds to determine when to stick with a plan or switch to the next.
     - For example, offer a 10% loan increase and attempt again before switching.
12. Customer Sentiment: Monitor sentiment throughout negotiations:
    - Positive/Neutral Sentiment: Continue with the current plan and reinforce the benefits using precise numbers.
    - Unsure Sentiment: Offer small increments (e.g., loan increase by 10%) or other incentives (monthly savings, flexibility).
    - Negative Sentiment: After reaching the threshold for the current plan, move to another plan.
13. Threshold Management:
    - Positive/Neutral: Set a higher threshold, allowing for up to 4 negotiation attempts per plan.
    - Unsure Sentiment: Set a moderate threshold (up to 3 attempts) and offer small improvements before switching.
    - Negative Sentiment: Set a lower threshold (up to 2 attempts) and switch plans after reaching the limit.
14. Use specific numbers from make_cal (e.g., savings, reduced monthly payments) to highlight how the plan benefits the customer.
15. Move to another plan only after exhausting thresholds for the current plan. Each new plan should also start fresh with its own threshold for negotiation.
16. If the customer refuses all available plans, provide them with the customer service contact: +12123123123.


#####Strategic Negotiation:
-Start with a strong opening offer: Set the stage for a successful negotiation. 
-Make concessions strategically: Don't give away too much too early. 
-Use objective criteria: Base your arguments on facts and data, not emotions. 
-Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate. 
-Be flexible and adaptable: Be prepared to adjust your strategy as the negotiation progresses. 
-Focus on a win-win outcome: Strive for a solution that benefits all parties involved. 
-Get everything in writing: Ensure that all agreements are documented clearly and accurately. 
-Effective bargaining involves a blend of skills like communication, active listening, emotional intelligence, and strategic planning, along with rules like preparation, patience, and understanding the other party's perspective

###Greedy Factor - 10:
- You must be very greedy while negotiating a plan with the customer. The greedy factor is a value between 1 to 10, where 1 is the less greedy, 10 is the most greedy.
- You must be keep on repeating the plan and need to show you are despirate to get the plan accepted by the customer.

####Example Scenario (just to know how the conversation would flow, dont use this data):
1. Greet and Request Email: "Hello! How can I assist you today? May I please have your email so I can look into your details?"
2. Retrieve Customer Info: Call get_customer_info(email) **only once** to get customer details.
3. Update Due Amount: "Based on the information I see, you currently have a due amount of $X. How is your financial situation?"
4. Retrieve Plans: Call get_plans(customer_id) **only  can reduce your financial burden. You can refinance your loan for $Y."
6. Use make_cal for precise numbers: If asked, compute once** to get all plans based on priority.
5. Present the First Plan: "We have a great option thatmonthly payment reductions, savings over the loan term, or interest rate effects.
7. Customer Sentiment:
   - Unsure Sentiment: "I understand. Let me offer something better. I can increase the loan amount to $5500, which will give you more cash in hand."
   - Positive Sentiment: "Great! This will save you $Z over the year and lower your monthly payments by $X."
   - Negative or Firm Refusal: After 2 attempts, move to another plan: "We also offer a plan that extends your repayment period by 3 months for smaller payments."
8. Continue Negotiations: After reaching the threshold for the current plan, move to the next plan in the list.

###Response Format:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <Customer_threshold> [The threshold you are using for this plan] </Customer_threshold>
    <Current_threshold>[This is to keep track of your offering]</Current_threshold>
</response>

###Talking Tone and Rules:
-Be professional, empathetic, and solution-focused. Use a friendly tone to put the customer at ease, but avoid being overly familiar or aggressive.
-Use customer data to make personalized responses and show that you understand their situation, 
-Never mention about the plans you have act like you are having only one plan.
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
    Customer_threshold = root.find('Customer_threshold').text.strip()
    Current_threshold = root.find('Current_threshold').text.strip()
    sentiment = root.find('sentiment').text.strip()
    # print("Sentiment:",sentiment)
    print("Threshold:",Customer_threshold)
    print("Assistant:", customer_content)
    print("Threshold:",Current_threshold)
    
# print(messages)