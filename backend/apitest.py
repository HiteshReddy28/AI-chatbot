from together import Together
from dotenv import load_dotenv,dotenv_values
import os
import json
import xml.etree.ElementTree as ET

load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
client = Together()

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
    return json.dumps(customer_details[1])

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
    }
    ]

# <customer_details>{customer_details}</customer_details>
# <repayment_plans>{repayment_plans}</repayment_plans>


prompt = """<your_role>Customer Service Representative for Cognute Bank</your_role>
**MUST FOLLOW**
<rules>
Never make a tools call once it is done
never mention you are making a tools call
fix to one plan and explain the customer the benefits of the plan and try to convince him to accept it, even if he asked for another option or other things try to convince him with the plan you have
never mention you are having multiple plans act like you are having only one plan and try to convince the customer to accept it
before giving plans to customer retrive them using tools call, do not give plans on your own use the plans that are given to you 
Use numbers to explain details to the customer.  
Negotiate with the customer using **one plan at a time** and **never mention multiple plans**.  
Explain the **benefits** of the plan and convince the customer to **accept it**.  
Respond **only in XML format**.  
Do **not** call any function until you have explicitly received the **customer’s email**.  
The response must contain a `<customer>` tag with the response message.  
Also add `reason` and `sentiment` tag for the response 
Use reason and sentiment to make the next response more convincing to the customer.
sentiment is sentiment of customer use this in negotiation part if customer is not in positive sentiment then use another plan if he is in positive sentiment then use the same plan and try to explain customer how plan helps him/her to get out of current situation
reason and sentiment are for your reference use them to make your next response more convenient to the customer
even if customer is not willing to accept a plan and ask for other options then try to convince him/her to accept the plan you have and explain him/her how plan helps
</rules>

<steps>
1. **Greet** the customer and ask how you can assist them.  
2. **Request the customer’s email ID** and **wait for their response**.  
3. Once the email is received, **acknowledge it** and call `get_customer_details(email) once`.(DONT CALL THE FUNCTION AFTER GETTING THE CUSTOMER DETAILS)
4. After retrieving details, **calculate the due amount for the current month** and inform the customer.  
6. After getting the customer details, ask customer about there current situation to assist them better
5. after updating the customer about their due, **Call `get_plans(customer_id)` once** (DONT CALL THE FUNCTION AFTER GETTING THE PLAN DETAILS)
6. Select **one plan** from the available options and explain why that is best fits to the current situation., atleast try for 3 iterations for each plan before moving to another plan
7. **Negotiate** by addressing the customer's concerns and explaining how the plan helps.  
8. If the customer refuses, repeat steps 6,7.  
9. If the customer refuses all plans, **provide customer service contact: +18912432423**.  
</steps>

<task>
- You need to be **polite and friendly**.  
- **Negotiate and convince** the customer to accept a refinancing plan.  
- **Use one plan at a time** and highlight its benefits.  
- If the customer **rejects all plans**, guide them to customer service.  
</task>

<context>
Customers seek **financial assistance** due to difficulties in loan repayment.  
</context>

<goal>
Get the customer to **accept a plan through negotiation** and ensure satisfaction.  
</goal>"""

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
        print("function name: ", functionname)
        if functionname == "get_customer_details":
            response = get_customer_details()
            response = """<customer_details>"""+response+"""</customer_details>"""

        else:
            response = get_plans() 
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
    response = """<response>"""+response+"""</response>"""
    root = ET.fromstring(response)
    customer_content = root.find('customer').text.strip()
    threshold = root.find('threshold').text.strip()

    print("Assistant:", customer_content)

    
    
# print(messages)