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
          "2. Call appropriate function"
          "3. Negotiate with the customer atleast 3 times to make him understand the plan and the benefits it wil reap."],
      "Example": """
          system : According to the current situation, We think a refinance of X$ which is same as you principal loan amont with same y tenure and z% interest is the best and only option we can offer you.
          user: I am not sure if I want to refinance.
          system: I understand that you are going through a lot, let me explain about refiance and how this is your best option as of now, which helps you by giving A$ in cash which can help you come out of current financial situation.
          user: But i need more options | I need more money | this is not helping me out
          system: I understand you need more options|money| help, let me explain how this plan can help you by giving you B$ in cash which can help you come out of current financial and your new loan will be of X$(same loan amount) with same y tenure and z% interest. This is the best option we can offer you as of now
          """,
    },
   {
  "plan_id": 2,
  "name": "Refinance Step Up",
  "priority": 2,
  "description": "Increase loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "Calculation_parameters": "in_cash = `Offered_principal` - `remaining_balance` - `due`, interest = `Offered_Principal` * `interest_rate` * `tenure`",
  "negotiation_steps": [
    "1. Start by explaining the 10% increase option first. Stick to it and reinforce its benefits at least three times before considering a higher percentage.",
    "2.Call appropriate function.",
    "3. Never disclose multiple options upfront. Present the 10% increase as the best and only available option at first.",
    "4. If the customer refuses or asks for more, gradually introduce the next step (20%) while reinforcing why the current step is optimal.",
    "5. Never jump directly to a higher percentage. Always go in order (10% → 20% → 30%...50%) and stick to same step before offering the next.",
    "6. Once the customer shows interest, create urgency by mentioning that this step-up refinance option is available for a limited time."
  ],
  "example": """
system: Based on your current financial situation, we believe increasing your loan amount by X$ + 0.1 * X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will provide you with an additional A$ in cash to help with your needs.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by increasing your loan by 10%, you get A$ in cash while keeping your payments affordable. This small step can help improve your situation without major changes to your monthly commitments.  
user: But I need more options | I need more money | This is not helping me enough.  
system: I completely understand. Right now, the **10% increase is your best option** because it gives you more cash while keeping payments stable. If you’re looking for a higher amount, we can **first see how this step benefits you** before considering anything else. Would you like me to show how this amount fits your current needs?  
(user continues resisting)  
system: I see you need more financial flexibility. If the 10% increase doesn’t fully meet your needs, we can explore a **20% increase**, which provides even more cash while still keeping payments in check. Let’s first see how this next step works for you.  
"""
},
{
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 3,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Start by explaining the 10% decrease option first. Stick to it and reinforce its benefits at least three times before considering a higher percentage.",
    "2.Call appropriate function.",
    "3. Never disclose multiple options upfront. Present the 10% decrease as the best and only available option at first.",
    "4. If the customer refuses or asks for more, gradually introduce the next step (20%) while reinforcing why the current step is optimal.",
    "5. Never jump directly to a higher percentage. Always go in order (10% → 20% → 30%...50%) and stick to same step before offering the next.",
    "6. Once the customer shows interest, create urgency by mentioning that this step-down refinance option is available for a limited time."
  ],
  "example": """
system: Based on your current financial situation, we believe reducing your loan amount by X$- 0.1*X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will reduce your monthly payments, helping to ease your financial burden.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by reducing your loan by 10%, you lower your monthly payments significantly, making it easier to manage your finances. This step can reduce your burden without affecting your financial flexibility too much.  
user: But I need more options | I need less debt | This is not helping me enough.  
system: I completely understand. Right now, the **10% reduction is your best option** because it helps reduce your monthly payments without stretching your budget. If you’re looking for more relief, we can **first see how this reduction improves your situation** before considering anything else. Would you like me to show how this adjustment fits your current needs?  
(user continues resisting)  
system: I see you’re seeking greater financial relief. If the 10% reduction doesn’t fully meet your needs, we can explore a **20% reduction**, which will further lower your debt and make payments even more manageable. Let’s first see how this next step works for you.
"""
},
  {
  "plan_id": 4,
  "name": "Extended Payment Plan 3 Months upto 12 months",
  "priority": 4,
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
  "priority": 5,
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
  "priority": 6,
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


prompt = """
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
2. It must be between 3 and 5. It will be changed after each negotiation. The initial value of threshold for each plan must be 3. Let's say a new plan has been to the customer the threhold must be set to 3.
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
        max_tokens=300,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
    )
    response = response.choices[0].message.content
    messages.append({
        "role":"assistant",
        "content":response})
    print("Assistant:", response)
#     root = ET.fromstring(response)
#     customer_content = root.find('customer').text.strip()
#     threshold = root.find('threshold').text.strip()
#     sentiment = root.find('sentiment').text.strip()
#     # print("Sentiment:",sentiment)
#     print("Threshold:",threshold)
#     print("Assistant:", customer_content)
    
# # print(messages)