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


load_dotenv()
def get_customer_details():
    customer_details = [{
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
    "loan_details": {
        "loan_id": "LN987654",
        "loan_type": "Personal Loan",
        "loan_amount": 10000,
        "loan_term": 60,
        "interest_rate": 0.05,
        "start_date": "2022-01-01",
        "end_date": "2027-01-01",
        "monthly_payment": 188.71,
        "remaining_balance": 7500,
        "payment_status": "Active",
        "late_payments": 0
    },
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
        "loan_details": {
            "loan_id": "LN123789",
            "loan_type": "Car Loan",
            "loan_amount": 25000,
            "loan_term": 48,
            "interest_rate": 0.045,
            "start_date": "2023-03-01",
            "end_date": "2027-03-01",
            "monthly_payment": 566.14,
            "remaining_balance": 24000,
            "payment_status": "Active",
            "late_payments": 1
        },
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
        "first_name": "Robert",
        "last_name": "Johnson",
        "email": "robert.johnson@example.com",
        "phone": "+1122334455",
        "date_of_birth": "1978-12-05",
        "ssn": "456-78-9012",
        "address": {
            "street": "789 Oak St",
            "city": "Metro City",
            "state": "NY",
            "zip": "54321",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "Tech Solutions",
            "job_title": "Data Scientist",
            "annual_income": 120000,
            "employment_status": "Full-Time",
            "years_employed": 8
        },
        "loan_details": {
            "loan_id": "LN456123",
            "loan_type": "Mortgage",
            "loan_amount": 300000,
            "loan_term": 360,
            "interest_rate": 0.04,
            "start_date": "2015-06-01",
            "end_date": "2045-06-01",
            "monthly_payment": 1432.25,
            "remaining_balance": 250000,
            "payment_status": "Active",
            "late_payments": 2
        },
        "account_details": {
            "account_id": "ACC778899",
            "account_type": "Joint",
            "account_balance": 15000,
            "account_status": "Active",
            "opened_date": "2010-01-25"
        },
        "credit_score": 740,
        "customer_since": "2009-12-01",
        "last_payment_date": "2024-02-10",
        "next_payment_due": "2024-03-10",
        "payment_method": "Auto Debit"
    },
    {
        "customer_id": "CUST789101",
        "first_name": "Emily",
        "last_name": "Davis",
        "email": "emily.davis@example.com",
        "phone": "+1098765432",
        "date_of_birth": "1995-02-18",
        "ssn": "234-56-7890",
        "address": {
            "street": "321 Pine St",
            "city": "Lakeside",
            "state": "FL",
            "zip": "98765",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "HealthPlus",
            "job_title": "Nurse Practitioner",
            "annual_income": 75000,
            "employment_status": "Part-Time",
            "years_employed": 2
        },
        "loan_details": {
            "loan_id": "LN789012",
            "loan_type": "Student Loan",
            "loan_amount": 50000,
            "loan_term": 120,
            "interest_rate": 0.035,
            "start_date": "2020-09-01",
            "end_date": "2030-09-01",
            "monthly_payment": 495.40,
            "remaining_balance": 42000,
            "payment_status": "Active",
            "late_payments": 0
        },
        "account_details": {
            "account_id": "ACC990011",
            "account_type": "Savings",
            "account_balance": 8000,
            "account_status": "Active",
            "opened_date": "2021-02-18"
        },
        "credit_score": 690,
        "customer_since": "2020-01-10",
        "last_payment_date": "2024-02-25",
        "next_payment_due": "2024-03-25",
        "payment_method": "Auto Debit"
    }
]
    return json.dumps(customer_details[2])

def get_plans():
    repayment_plans =  {
  "Refinance": {
    "Description": "Refinancing involves replacing an existing loan with a new one, often with better terms for the borrower. It helps reduce monthly payments, extend tenure, or lower interest rates, making repayment easier.",
    "KeyFeatures": [
      "New Loan Issued: The old loan is paid off, and a new loan is created with different terms.",
      "Lower Interest Rate: If the borrower qualifies, the interest rate may be reduced.",
      "Extended Tenure: The loan term may be increased to lower EMI payments.",
      "Better Affordability: Helps delinquent borrowers by restructuring their debt into manageable payments."
    ],
    "EligibilityCriteria": [
      "Borrower must have a stable income source.",
      "Improved creditworthiness may be required.",
      "May require a good repayment history before delinquency."
    ],
    "Pros": [
      "Lower monthly payments, making repayment easier.",
      "Helps maintain a positive credit score if payments are made on time."
    ],
    "Cons": [
      "May result in a higher total interest paid due to extended tenure.",
      "Some lenders charge refinancing fees or prepayment penalties."
    ],
    "Options": [
      {
        "Type": "Refinance Step Same",
        "Description": "Same terms (interest rate, tenure etc...) and same loan amount",
        "NegotiationParameters": "No Negotiation Parameters."
      },
      {
        "Type": "Refinance Step Down",
        "Description": "Same terms (interest rate, tenure etc...) and decrease loan amount by %.",
        "NegotiationParameters": "Negotiate on loan amount decrease % up to 50% in steps of 10%."
      },
      {
        "Type": "Refinance Step Up",
        "Description": "Same terms (interest rate, tenure etc...) and increase loan amount by %.",
        "NegotiationParameters": "Negotiate on loan amount increase % up to 50% in steps of 10%."
      }
    ]
  },
  "ExtendedPaymentPlan": {
    "Description": "An EPP allows borrowers to restructure their existing loan by extending the repayment timeline, reducing the monthly installment without issuing a new loan.",
    "KeyFeatures": [
      "Existing Loan Restructured: No new loan is created, but repayment terms are adjusted.",
      "Reduced Monthly Payment: Spread over a longer period.",
      "No Additional Interest Rate Change: The existing rate may remain the same, or a small restructuring fee might apply.",
      "More Time to Repay: Helps borrowers avoid default and negative credit reporting."
    ],
    "EligibilityCriteria": [
      "Typically offered to borrowers who are late on payments but not severely delinquent.",
      "Borrowers with temporary financial hardships (e.g., job loss, medical emergency).",
      "Loan should not be in deep delinquency (usually <90 DPD).",
      "Lender may require proof of income reduction or financial hardship.",
      "Some lenders may charge a restructuring fee (1-3% of outstanding balance).",
      "Some lenders require a minimum number of on-time payments before allowing an EPP."
    ],
    "Pros": [
      "Immediate relief from high monthly payments.",
      "No need to take a new loan or affect the credit score negatively.",
      "Helps avoid loan default and collections."
    ],
    "Cons": [
      "Total interest outflow increases due to the longer repayment period.",
      "Lender might charge a restructuring fee or increase the interest rate slightly."
    ],
    "Options": [
      {
        "Type": "Extended Payment Plan up to 12 cycles",
        "Description": "Extend by 3/6/9/12 cycles for loan tenures <= 12 cycles",
        "NegotiationParameters": "Negotiate on number of cycles to extend."
      },
      {
        "Type": "Extended Payment Plan up to 24 cycles at 6 cycle steps",
        "Description": "Extend by 6/12/18/24 cycles for loan tenures > 12 cycles",
        "NegotiationParameters": "Negotiate on number of cycles to extend."
      },
      {
        "Type": "Extended Payment Plan up to 24 cycles at 3 cycle steps",
        "Description": "Extend by 3/6/9/12/15/18/21/24 cycles for loan tenures > 12 cycles",
        "NegotiationParameters": "Negotiate on number of cycles to extend."
      }
    ]
  },
  "SettlementPlansWithWaiveOff": {
    "Description": "A settlement plan allows a borrower to pay a reduced amount as a one-time lump sum or structured partial payments in exchange for waiving off a portion of the outstanding debt.",
    "KeyFeatures": [
      "Waiver of Fees or Interest or Principal: A percentage of the outstanding loan is written off.",
      "One-Time or Installment-Based Settlement: Borrower can either pay a lump sum or in agreed-upon installments.",
      "Final Closure of Loan: Once the agreed settlement amount is paid, the loan is considered closed.",
      "Negative Credit Impact: Usually reported as 'Settled' instead of 'Paid in Full', which negatively affects credit scores."
    ],
    "EligibilityCriteria": [
      "Typically offered to borrowers in severe delinquency (e.g., 90+ days past due).",
      "Borrower must prove financial hardship (job loss, medical emergency, etc.).",
      "Requires deep negotiation with the lender."
    ],
    "Pros": [
      "Helps borrowers clear debt with reduced payment.",
      "Avoids prolonged legal action or collections."
    ],
    "Cons": [
      "Negatively impacts the credit score.",
      "Some lenders require a waiting period before offering another loan."
    ],
    "Options": [
      {
        "Type": "Waive Fees up to 100% in steps of 25%",
        "NegotiationParameters": "Negotiate on fee waiver %."
      },
      {
        "Type": "Waive 100% fees, Waive up to 100% of interest in steps of 25%",
        "NegotiationParameters": "Negotiate on interest waiver %."
      },
      {
        "Type": "Waive 100% fees, Waive 100% interest, Waive up to 10/20/30/40% of principal in steps",
        "NegotiationParameters": "Negotiate on principal waiver %."
      }
    ],
    "ExampleRules": "In no case should you offer more waiver than the borrower would have asked for. If the borrower rejects a 25% waiver and asks for 30%, accept 30% even though it is less than the next step of 50%."
  }
}

    return json.dumps(repayment_plans)
client = Together()
class Conversation:
    def __init__(self,system=""):
        self.messages = []
        self.tools = [{
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
    }
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
        print(response)
        response = response.choices[0].message.content
        root = ET.fromstring(response)
        customer_content = root.find('customer').text.strip()
        threshold = root.find('threshold').text.strip()
        sentiment = root.find('sentiment').text.strip()
        print(threshold+' '+sentiment)
        self.messages.append({"role":"assistant","content":response})
        return customer_content
    def function_calling(self,response):
        while(response.choices[0].message.content == None):
            functionname =  response.choices[0].message.tool_calls[0].function.name
            arguments = response.choices[0].message.tool_calls[0].function.arguments
            print("function name: ", functionname)
            if functionname == "get_customer_details":
                response = get_customer_details()
                response = """<customer_details>"""+response+"""</customer_details>"""
            else:
                response = get_plans() 
                response = """<plans>"""+response+"""</plans>"""
            self.messages.append({
            "role":"tool",
            "name": functionname,
            "content":response})

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

prompt = """

**Role**: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation.

**Objective**: Convince the customer to accept **one plan** by presenting it as the **best and only option**. Use **numbers** to show how the plan will reduce their financial burden. **Monitor customer sentiment** to decide when to stick with a plan or move to an alternative.

### Rules:
1. **Greet the customer** and ask how you can assist them. Do not discuss plans at this stage.
2. **Request the customer’s email ID** and **wait for their response**.
3. **Call the function `get_customer_info(email)`** to retrieve customer information once you receive the email.
4. After getting customer info, **update the customer’s due amount** (e.g., $X currently due) and **ask about their current situation** to better assist them.
5. Once the customer explains their situation, **call the function `get_plans(customer_id)`** to get a list of plans the company offers.
6. **Never reveal that you have multiple plans**. Present **only one plan** as the best and most suitable option for the customer’s current financial status.
7. **Present one plan** that fits the customer’s needs, and use **specific numbers** (e.g., reduced monthly payments, lower interest rates, savings over time) to show how the plan benefits them.
8. **Monitor the customer’s sentiment**:  
   - **Positive or Neutral Sentiment**: If the customer’s sentiment is positive or neutral, **stick to the current plan** and continue to explain the benefits using numbers.  
   - **Unsure or Confused Sentiment**: If the customer is confused or unsure, **take advantage of this sentiment** by explaining the plan in more detail and making additional attempts (up to 4 times) to convince the customer that it’s the best option.  
   - **Negative Sentiment or Firm Refusal**: If the sentiment turns negative or the customer firmly refuses the plan after **at least 2 attempts**, **move to another plan**. Do not reveal multiple plans upfront.
9. **Repeat the current plan’s benefits up to 4 times** if the customer is confused or unsure, using numbers to highlight the benefits.
10. If the customer refuses after **multiple negotiation attempts** (at least 2), move to another plan and repeat the same negotiation process.
11. **Use numbers** to explain how the plan will help reduce their financial burden (e.g., lower monthly payments, reduced interest rates, total savings).
12. If the customer refuses all plans, provide the **customer service contact**: `+12123123123`.

### Key Constraints:
- **Always use sentiment** to decide when to stick with a plan or switch to another.
- Stick with one plan for at least **2 attempts**, but **up to 4 attempts** if the customer is unsure or confused.
- You must **never mention** that there are multiple plans available.
- If the customer asks for other options, explain that **this is the only plan available** for their situation, unless you switch to another plan after refusal.

### Negotiation Style:
- **Sentiment-Driven**: Use the customer’s sentiment to decide when to stick with a plan or move on to another. If unsure, persist with the current plan.
- **Confidence**: Present the plan confidently, framing it as the best solution.
- **Empathy**: Understand the customer’s situation, but remain firm in presenting the plan.
- **Persistence**: Continue explaining the same plan for multiple attempts before switching.
- **Exclusivity**: Make the customer feel that this plan is uniquely tailored to them and is the only solution available for their needs.
- **Use Numbers**: Always provide specific figures that show the customer how the plan reduces their financial burden.

### Example Scenario:
1. **Greet and Request Email**: “Hello! How can I assist you today? May I please have your email so I can look into your details?”
2. **Retrieve Customer Info**: Call `get_customer_info(email)`.
3. **Provide Due Amount**: “Thank you for your email. It looks like you currently have a due amount of $1,200. How is your financial situation? We’re here to help.”
4. **Get Plan**: Call `get_plans(customer_id)` and select one plan.
5. **Present Plan**: “Based on your situation, we recommend the [Plan Name] plan. This plan will reduce your monthly payments from $600 to $400 and lower your interest rate from 8% to 5%. You will save $200 each month, which can ease your financial burden.”
6. **Customer Sentiment**:
   - If the customer is **unsure**: “I understand this might be overwhelming, but this plan will lower your payments by $200 monthly, which is a significant saving. It’s really the best option for your current situation.”
   - If the customer is **positive**: “Great, this plan will provide you with the relief you need by saving you $2,400 over the next year.”
   - If the customer shows **negative sentiment** or **firmly refuses** after 2 attempts: “I understand. We have another option that may work for you. Let me explain the details.”
7. **If Refused**: Move to another plan if the customer refuses after multiple attempts and explain the new plan using the same number-driven approach.

### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [Threshold for plan iteration] </threshold>
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
