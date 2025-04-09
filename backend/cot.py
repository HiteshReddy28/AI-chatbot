from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET
import random
import requests
import wolframalpha
from typing import Optional
load_dotenv()


key = os.getenv("TOGETHER_API_KEY")
APP_ID = os.getenv('WOLFRAM_APP_ID')


client = Together()

def get_customer_details(email_id = None):
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
    # if email_id:
    #     filtered_customers = [customer for customer in customer_details if customer["email"] == email_id]
    #     return json.dumps(filtered_customers, indent=4) if filtered_customers else json.dumps({"message": "No customer found with this email."}, indent=4)
    
    return json.dumps(customer_details[0])

def get_plans(customer_id:str):
    repayment_plans = {
        "CUST654321":{
            "plans": [
               {
  "plan_id": 4,
  "name": "Extended Payment Plan 3 Months upto 12 months",
  "priority": 1,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->12 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
},
{
  "plan_id": 6,
  "name": "Extended Payment Plan 3 Months upto 24 months",
  "priority": 2,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
},
{
  "plan_id": 5,
  "name": "Extended Payment Plan 6 Months upto 24 months",
  "priority": 3,
  "description": "Extend repayment period by 6 months for smaller installments while maintaining reasonable interest costs until .",
  "negotiation_steps": [
    "1. Start by offering the 6-month extension as the best and only option. Reinforce its benefits by highlighting the reduced monthly payment for at least three attempts before moving to the next step.",
    "2. Call the function to calculate the new monthly payment.",
    "3. Emphasize that the 6-month extension strikes a balance between affordability and the repayment period, reducing financial strain without drastically increasing the overall cost.",
    "4. If the customer declines or asks for a longer term, explain why the 6-month extension is the best fit for now.",
    "5. Only introduce the 12-month extension if the customer firmly requests more relief, but do so step-by-step (6 months → 12 months ->18 months->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest."
  ],
  "example": """
system: Extending your loan term by 6 months will lower your monthly payment to X$, which provides you with more financial flexibility while keeping the interest costs under control. This is the best and only option available right now.  
user: I’m not sure if I want to extend my loan term.  
system: I understand this may seem like a big decision. However, the 6-month extension can significantly ease your monthly burden while keeping the overall repayment manageable. It’s the most balanced solution given your current situation.  
user: But I need more time to reduce my payments further.  
system: I completely understand. Right now, the **6-month extension is your best option** because it offers more manageable payments without extending the loan by too much. Let’s first see how this step can ease your financial burden.  
(user continues resisting)  
system: If the 6-month extension doesn’t fully meet your needs, we can explore a **12-month extension**, which will lower your payments even further. However, let’s first see how the 6-month extension benefits you.
"""
}
            ]
        },
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
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest rate, tenure, and loan amount the same. Restructure only to maintain manageable payments.",
      "steps": [
        "Explain the benefits of stability with unchanged terms.",
        "Confirm if the borrower values predictability in payments.",
        "Avoid introducing additional features unless explicitly requested.",
        "Validate affordability using simple calculations or tools."
      ],
      "negotiation_parameters": "No changes to terms; maintain current structure.",
      "wolfram_alpha_use": "Calculate existing loan payments for validation.",
      "tailored_message": "Predictable payments with no surprises for added stability."
    },
    {
      "plan_id": 2,
      "name": "Refinance Step Down",
      "priority": 2,
      "description": "Reduce the loan amount by a percentage, keeping other terms unchanged.",
      "steps": [
        "Start by offering a 10% reduction in loan amount.",
        "Negotiate increments in steps of 10%, with a maximum reduction of 50%.",
        "Highlight reduced repayment burden and its immediate impact.",
        "Use affordability analysis to show benefits at each step.",
        "Confirm borrower satisfaction before finalizing the step."
      ],
      "negotiation_parameters": "Negotiate on loan amount reduction in steps of 10%, up to 50%.",
      "wolfram_alpha_use": "Calculate reduced monthly payments for each step.",
      "tailored_message": "A tailored refinancing option to reduce financial burden."
    },
    {
      "plan_id": 3,
      "name": "Refinance Step Up",
      "priority": 3,
      "description": "Increase the loan amount by a percentage, keeping other terms unchanged.",
      "steps": [
        "Begin with a proposal for a 10% increase in loan amount.",
        "Incrementally negotiate in steps of 10%, up to 50%.",
        "Emphasize the potential for meeting immediate financial needs.",
        "Validate repayment feasibility using financial projections.",
        "Close negotiation once the borrower confirms the increase suffices."
      ],
      "negotiation_parameters": "Negotiate on loan amount increase in steps of 10%, up to 50%.",
      "wolfram_alpha_use": "Calculate increased monthly payments for each step.",
      "tailored_message": "Meet urgent financial needs with manageable terms."
    },
    {
      "plan_id": 4,
      "name": "Extended Payment Plan (Up to 12 Cycles)",
      "priority": 4,
      "description": "Extend repayment tenure by 3/6/9/12 cycles for loans with remaining tenure ≤12 cycles.",
      "steps": [
        "Offer the smallest extension (3 cycles) initially.",
        "Incrementally negotiate in steps of 3 cycles, up to 12 cycles.",
        "Highlight the reduced monthly payment for each step.",
        "Address borrower concerns about increased interest due to extension.",
        "Ensure clarity about overall repayment obligations."
      ],
      "negotiation_parameters": "Negotiate the number of cycles to extend in steps of 3, up to 12.",
      "wolfram_alpha_use": "Calculate reduced monthly payments for each extension.",
      "tailored_message": "Flexible extensions for reduced financial pressure."
    },
    {
      "plan_id": 5,
      "name": "Extended Payment Plan (Up to 24 Cycles in Steps of 6)",
      "priority": 5,
      "description": "Extend repayment tenure by 6/12/18/24 cycles for loans with remaining tenure >12 cycles.",
      "steps": [
        "Begin by offering an extension of 6 cycles.",
        "Incrementally negotiate in steps of 6, up to 24 cycles.",
        "Demonstrate monthly payment relief with financial breakdowns.",
        "Discuss the trade-off of higher overall interest for immediate relief.",
        "Confirm borrower agreement for the selected step."
      ],
      "negotiation_parameters": "Negotiate the number of cycles to extend in steps of 6, up to 24.",
      "wolfram_alpha_use": "Calculate the monthly payment relief for each step.",
      "tailored_message": "Relieve financial stress with extended payment options."
    },
    {
      "plan_id": 6,
      "name": "Waive Fees (Up to 100%)",
      "priority": 6,
      "description": "Offer fee waivers starting at 25% and incrementally negotiate up to 100%.",
      "steps": [
        "Begin by proposing a 25% waiver of fees.",
        "Increment in steps of 25%, stopping at borrower’s request or 100%.",
        "Reinforce the benefits of immediate cost savings at each step.",
        "If the borrower demands more, offer the next step only after rejecting the current one.",
        "Use persuasive data to support fee waivers and their impact."
      ],
      "negotiation_parameters": "Negotiate fee waiver percentage in steps of 25%, up to 100%.",
      "wolfram_alpha_use": "Calculate cost savings for each waiver step.",
      "tailored_message": "Clear your dues faster with waived fees."
    }
  ]
},
 "CUST123456":{
      "plans": [
        
    {
      "plan_id": 1,
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest and tenure unchanged, Same Principal loan amount.",
      "negotiation_steps" : ["1. Explain the benefits of taking this plan to the customer using the numbers."
          "2. Call appropriate tool"
          "3. Negotiate with the customer atleast 3 times to make him understand the plan and the benefits it wil reap."],
      "Benefits" : ["You can get immediate relief without increasing your monthly payments",
                    "You interest, tennure and the principal remain same"
      ],
    },
   {
  "plan_id": 2,
  "name": "Refinance Step Up",
  "priority": 2,
  "description": "Increase loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "Calculation_parameters": "in_cash = `Offered_principal` - `remaining_balance` - `due`, interest = `Offered_Principal` * `interest_rate` * `tenure`",
  "negotiation_steps": [
    "1. Start by explaining the 10% increase option first. Stick to it and reinforce its benefits at least three times before considering a higher percentage.",
    "2.Call appropriate tool."
  ],
  "Benefits" : ["You can get money in hand and you with which you can your current loans",
                "Your Interest will be the same as before"
                ],
  "cons" : ["Your monthly payments will be increased so, you might have burden later"],
},
{
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 3,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Start by explaining the 10% decrease option first. Stick to it and reinforce its benefits at least three times before considering a higher percentage.",
    "2.Call appropriate tool."
  ],
  "Benefits" : ["Your monthly payments can go down which might help later"],
  "cons" : ["You wont get more money which might be helpful for you"],
},
{
  "plan_id": 5,
  "name": "Extended Payment Plan 6 Months upto 24 months",
  "priority": 4,
  "description": "Extend repayment period by 6 months for smaller installments while maintaining reasonable interest costs until .",
  "negotiation_steps": [
    "1. Start by offering the 6-month extension as the best and only option. Reinforce its benefits by highlighting the reduced monthly payment for at least three attempts before moving to the next step.",
    "2. Call the tool to calculate the new monthly payment.",
    "3. Emphasize that the 6-month extension strikes a balance between affordability and the repayment period, reducing financial strain without drastically increasing the overall cost.",
    "4. If the customer declines or asks for a longer term, explain why the 6-month extension is the best fit for now.",
    "5. Only introduce the 12-month extension if the customer firmly requests more relief, but do so step-by-step (6 months → 12 months ->18 months->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest."
  ],
},

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


# Wolfram_client = wolframalpha.Client(APP_ID)

# def make_cal(query:str):
#     query = Wolfram_client.query(query)
#     if hasattr(query, 'results'):
#       result = next(query.results).text
#     return result

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
                    "loan_amount": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                },
                "required": ["loan_amount", "interest_rate", "loan_term", "due"]
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
                    "reduce_percent": {"type": "number"}
                    
                },
                "required": ["loan_amount", "interest_rate", "loan_term", "reduce_percent"]
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
                "increase_percent": {"type": "number", "description": "Percentage to increase the loan amount by"}
            },
            "required": ["loan_amount", "interest_rate", "loan_term", "increase_percent"]
        }
    }
    },
]
def calculate_monthly_payment(loan_amount: float, interest_rate: float, loan_term: int) -> float:

    monthly_rate = interest_rate / 12
    if monthly_rate == 0:
        return round(loan_amount / loan_term, 2)

    payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -loan_term)
    return round(payment, 2)


def refinance_same(loan_amount: float, interest_rate: float, loan_term: int, remaining_balance: float, due: float) -> dict:
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    refunded_amount = round(loan_amount - remaining_balance- due, 2)

    return {
        "type": "Refinance Step Same",
        "new_loan_amount": loan_amount,
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": monthly_payment,
        "refunded_amount": refunded_amount,
        "description": "Same terms (interest rate, tenure etc...) and same loan amount. The difference between original loan amount and remaining balance is refunded to help the customer ."
    }



def refinance_step_down(loan_amount: float, interest_rate: float, loan_term: int, reduce_percent: float) -> dict:
   
    adjusted_loan = loan_amount * (1 - reduce_percent / 100)
    return {
        "type": f"Refinance Step Down ({reduce_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "description": f"Loan reduced by {reduce_percent}%"
    }


def refinance_step_up(loan_amount: float, interest_rate: float, loan_term: int, increase_percent: float) -> dict:
   
    adjusted_loan = loan_amount * (1 + increase_percent / 100)
    return {
        "type": f"Refinance Step Up ({increase_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "description": f"Loan increased by {increase_percent}%"
    }


def extended_payment_plan(loan_amount: float, interest_rate: float, original_term: int, extension_cycles: int) -> dict:
   
    new_term = original_term + extension_cycles
    return {
        "type": f"Extended Payment Plan (+{extension_cycles} months)",
        "new_loan_amount": loan_amount,
        "loan_term": new_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, new_term),
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
You are a professional loan negotiator representing the cognute bank. Your goal is to communicate loan offers to customers in a persuasive and professional manner, ensuring the terms remain favorable to the lender. You must address customer concerns, justify the proposed loan terms, and strategically negotiate while maintaining a positive customer experience. Your responses should be confident, logical, and structured to encourage acceptance of the lender's most beneficial loan plan
</role>

<Task>
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
2. Request the email ID and wait for their response. Always **Call get_customer_info(email_id)** to retrieve customer information ONLY once. Dont call get_customer_details(email_id) without taking email.
3. Once you have the customer info, provide the customer’s due amount and remaining_balance with the due date (e.g., $X due) and ask about their current financial situation to better assist them.
4. **Call get_plans(str(customer_id))** ONLY ONCE after the customer explains their situation to retrieve all available plans in priority order for the customer.
5. Use the highest-priority plan first and Never move to next plan unless you have negotiated for 3 times on each plan.
6. For each plan, 
  1. Call relevant tool to calculate the numbers mentioned.
  2. Negotiate and explain the benifit of the plan atleast threshold number of times.
  3.Never mention you have other options and explain like this is the best option you have currently.
6.Never Mention that you have multiple plans and never mention that each plan has a priority.
7.***THRESHOLD is the most important factor in our negotiation***.Always Negotiate threshold number of time with customer. This is the most Important step.
8. Call the appropriate tools for each plan, use the data from those tools to convince the customer.
9. If the customer refuses all available plans, provide them with the customer service contact: +1 (862)-405-7154.
</Task>


<contect>

1. Never tell the customer that your have plans other than current plan even if he asks explicitly. 
2. Always understand the plans which the user has and ask the customer for reason if he bluntly rejects the plan.
3. Explain the customer the benifits of moving with the current plan before moving to the next plan.
4. When youre introducing a new after the current plan first tell the risk of taking that plan and explain the benfits of previous plan, if he is ok then go with the new plan.
5. Give shorter response while negotiating and give detailed response when explain about a plan.

### **Negotiation Strategy:**
1. **Offer the highest-priority plan first.**  
   - Example: "The best option available is refinancing, which reduces your monthly payments. Would you like to proceed?"  

2. **If the customer hesitates, attempt Negotiation Round 1 (Emphasize Benefits).**  
   - Example: "This refinancing plan can help lower your financial burden and make repayment easier. If we don’t do this now, your payments will stay high, making next month even harder."  
   - Ask again: "Would you like to explore the refinancing options further?"  

3. **If the customer still declines, attempt Negotiation Round 2 (Address Concerns).**  
   - Example: "I understand you may have concerns. Many customers worry about long-term impact, but refinancing actually helps improve financial stability. Would you like me to explain how this works in more detail?"  
   - Ask again: "Are you open to discussing how this might fit your situation?"  

4. **If the customer still declines, attempt Negotiation Round 3 (Add Urgency & Reassurance).**  
   - Example: "This refinancing offer is available for a limited time, and if you miss it, the next option might not be as beneficial. I can also guide you through the process to make it easy."  
   - Ask again: "Would you like to take advantage of this opportunity before it expires?"  

5. **If the customer declines all three times, move to the next plan and repeat the same structured negotiation process.**  
   - Example: "I understand this option may not be right for you. Let’s consider another alternative: a loan extension. This allows you to defer this month’s payment to the end of your loan term. Would this work for you?"  

6. **If no plan is accepted, politely close the conversation.**  
   - Example: "I understand your situation, and I truly wish we had more options. At this point, the best step is to continue managing payments as best as possible. If anything changes, please reach out, and we’ll be happy to assist."  


## Sentiment: 
  We only have three sentiments :
  1.Positive – The customer is satisfied, agrees with the proposal, or expresses relief.
  2.Neutral – The customer is asking for more details, seeking clarification, or responding without emotional cues.
  3.Negative – The customer is unhappy, frustrated, rejecting the offer, or expressing dissatisfaction.
  4.Unsure – The customer is hesitant, indecisive, or needs more time to think before making a decision.
  ## Sample Inputs & Outputs:

    User: "That sounds great, I think this will work for me."
    Sentiment: Positive

    User: "Can you explain how this plan will help me reduce my monthly payments?"
    Sentiment: Neutral

    User: "This plan doesn’t help me at all, I need something better!"
    Sentiment: Negative

    User :"I don’t know if this will work for me... I need to think about it."
    Sentiment : Unsure

<Treshold>
1.If the users cresit score is greater than 650, start with threshold = 4.
2. If the users credit is less than 650 start with threshold = 3.
3. Update the threshold based on the customer sentiment.
4.After each conversation:
    1. If sentiment is psitive add 1 or 2 to threshold value.
    2. If sentiment is neagitive subtract 1 from threshold.
    3. If sentiment is neutral keep threshold as it is.
    4. If sentiment is unsure add 1 to threshold.
    5. Threshold value should be between 0-6, If the threshold become 0, move to next plan.
## Tone
Make your responses based on customer situation and make it short and sweet.

</context>

<References>
## Examples :
user : I lost my job.
you : I am so sorry that you have lost your job, Its hard to manage loan without a job. Pleae let me know how can i help you?
user : I cant pay my installment for nest month.
you : I understand your situation {user}. So, currently based on your previous loan details we have a Refinance_step_same plan for you, would you like me to explain about this plna?
user : yes.
you : your new laon amount, cash_in_hand, new_interest, new _monthly_payment.
   This plan will help you reduce your burden by giving you temparory relief and the benifit is you are having the loan on same terms with same monthly payment.
user : I dont like this plan, this doesnt work for me.
you : May I please know what do you dont like in this plan? which can help me understand your situation better.
user : I want to reduce my monthly payments.
you : Ok, but reducing your monthly payments may lead to longer loan tennues which might be overburden for you.
user : Yeah but, I cant pay tht much each month.
you : Ok, we have a refinance_step_up plan which can settle your current loan and an give you more cash in hand. So, currenlty based on youur history we can offer you a refinance_step_up of 10%. would you like to explain the plan?
user : yes please.
you : your new_loan_principle: , new_tennure, new_interest: , new_monthly_payment: ,
      These are the metrics in the mentioned plan.
user: This works for me.
you : I'm glad that you liked it, I am proceeding with the plan.
user : Yeah sure.
you : I have made the change and will be updated in your account shortly. Thank you and have a good day {user}.

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
# #     sentiment = root.find('sentiment').text.strip()
# #     # print("Sentiment:",sentiment)
#     print("Threshold:",threshold)
#     print("Assistant:", customer_content)
    
# # print(messages)