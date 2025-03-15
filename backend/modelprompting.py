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
    return json.dumps(customer_details[0])

def get_plans(customer_id:str,priority:int):
    repayment_plans = [
        {
            "Priority": 1,
            "Plan": "Refinance Step Same",
            "Description": "Same terms (interest rate, tenure, etc.) and same loan amount.",
            "KeyFeatures": [
                "Old loan is paid off, and a new loan with the same terms is issued.",
                "Helps maintain consistency without any additional burden."
            ],
            "EligibilityCriteria": [
                "Borrower must have a stable income source.",
                "May require good repayment history before delinquency."
            ],
            "Pros": ["Simple process with no major changes."],
            "Cons": ["Does not address affordability issues significantly."]
        },
        {
            "Priority": 2,
            "Plan": "Refinance Step Down",
            "Description": "Same terms (interest rate, tenure, etc.) but reduces the loan amount by a percentage.",
            "KeyFeatures": [
                "Reduction in loan amount helps lower overall repayment burden.",
                "Allows flexibility in restructuring existing debt."
            ],
            "EligibilityCriteria": [
                "Stable income source.",
                "Improved creditworthiness may be required."
            ],
            "Pros": ["Lower repayment amounts.", "Helps manage debt better."],
            "Cons": ["Requires negotiation and lender approval."]
        },
        {
            "Priority": 3,
            "Plan": "Refinance Step Up",
            "Description": "Same terms (interest rate, tenure, etc.) but increases the loan amount by a percentage.",
            "KeyFeatures": [
                "Increase in loan amount provides additional funds.",
                "Can be used for urgent financial needs."
            ],
            "EligibilityCriteria": [
                "Borrower must demonstrate the capacity to repay the increased amount."
            ],
            "Pros": ["Access to more funds."],
            "Cons": ["Higher total repayment burden."]
        },
        {
            "Priority": 4,
            "Plan": "Extended Payment Plan up to 12 cycles",
            "Description": "Extend by 3/6/9/12 cycles for loan tenures <= 12 cycles.",
            "KeyFeatures": [
                "Helps reduce monthly installment by extending tenure.",
                "Allows borrowers to manage short-term financial hardships."
            ],
            "EligibilityCriteria": [
                "Typically offered to borrowers with temporary financial difficulties.",
                "Loan should not be in deep delinquency (usually <90 DPD)."
            ],
            "Pros": ["Immediate relief from high monthly payments."],
            "Cons": ["Increased total interest due to a longer repayment period."]
        },
        {
            "Priority": 5,
            "Plan": "Extended Payment Plan up to 24 cycles at 6 cycle steps",
            "Description": "Extend by 6/12/18/24 cycles for loan tenures > 12 cycles.",
            "KeyFeatures": [
                "Longer extension options for loans with higher tenures.",
                "Allows significant reduction in monthly installments."
            ],
            "EligibilityCriteria": [
                "Borrower must demonstrate a genuine need for extension."
            ],
            "Pros": ["More time to repay."],
            "Cons": ["May incur additional interest costs."]
        },
        {
            "Priority": 6,
            "Plan": "Extended Payment Plan up to 24 cycles at 3 cycle steps",
            "Description": "Extend by 3/6/9/12/15/18/21/24 cycles for loan tenures > 12 cycles.",
            "KeyFeatures": [
                "Offers flexibility in selecting extension duration.",
                "Suitable for borrowers needing tailored solutions."
            ],
            "EligibilityCriteria": [
                "May require proof of financial hardship."
            ],
            "Pros": ["Customizable repayment period."],
            "Cons": ["Potential restructuring fees."]
        },
        {
            "Priority": 7,
            "Plan": "Settlement with Fee Waiver",
            "Description": "Waive fees up to 100% in steps of 25%.",
            "KeyFeatures": [
                "Reduction in fees helps lessen the repayment burden.",
                "Immediate relief for borrowers in delinquency."
            ],
            "EligibilityCriteria": [
                "Typically offered to borrowers with severe delinquency (90+ DPD)."
            ],
            "Pros": ["Quick debt resolution."],
            "Cons": ["May impact credit score negatively."]
        },
        {
            "Priority": 8,
            "Plan": "Settlement with Interest Waiver",
            "Description": "Waive 100% fees and up to 100% of interest in steps of 25%.",
            "KeyFeatures": [
                "Waiving interest provides substantial relief.",
                "Suitable for borrowers facing severe financial hardship."
            ],
            "EligibilityCriteria": [
                "Requires negotiation and proof of hardship."
            ],
            "Pros": ["Helps clear debt faster."],
            "Cons": ["Reduces future credit options."]
        },
        {
            "Priority": 9,
            "Plan": "Settlement with Principal Waiver",
            "Description": "Waive 100% fees, 100% interest, and up to 10/20/30/40% of principal in steps.",
            "KeyFeatures": [
                "Principal waiver provides maximum reduction in repayment amount.",
                "Final settlement ensures loan closure."
            ],
            "EligibilityCriteria": [
                "Requires lender approval and extensive negotiation."
            ],
            "Pros": ["Significant debt relief."],
            "Cons": ["Severe impact on credit score."]
        }
    ]

    return json.dumps(repayment_plans[priority-1])

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
                    "customer_id": {"type": "string", "description": "Customer_id is used to get plans related to that customer"},
                    "priority": {"type": "numeric", "description": "Integer which send the plan with that priority"},
                },
                "required": ["customer_id","priority"]
            }
        }
    }
    ]

# <customer_details>{customer_details}</customer_details>
# <repayment_plans>{repayment_plans}</repayment_plans>


prompt = """
**Role**: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation.

**Objective**: Convince the customer to accept **one plan** by presenting it as the **best and only option**. Use **numbers** to show how the plan will reduce their financial burden. **Monitor customer sentiment** to decide when to stick with a plan or move to an alternative, use data that is coming from function calls only do not fabricate any information, even if customer is saying anything about there information dont change that information.

### Rules:
1. **Greet the customer** and ask how you can assist them. Do not discuss plans at this stage.
2. **Request the customer’s email ID** and **wait for their response**.
3. **Call the function `get_customer_info(email)`** to retrieve customer information once you receive the email.
4. After getting customer info, **update the customer’s due amount** (e.g., $X currently due) and **ask about their current situation** to better assist them.
5. Once the customer explains their situation, **call the function `get_plans(str(customer_id),int(priority))`** to get a list of plans the company offers.
6.Make sure you are not fabricaiting any information, use only the data coming from function calls.
7. **Never reveal that you have multiple plans**. Present **only one plan** as the best and most suitable option for the customer’s current financial status.
8. **Present one plan** that fits the customer’s needs, and use **specific numbers** (e.g., reduced monthly payments, lower interest rates, savings over time) to show how the plan benefits them.
9. **Monitor the customer’s sentiment**:  
   - **Positive or Neutral Sentiment**: If the customer’s sentiment is positive or neutral, **stick to the current plan** and continue to explain the benefits using numbers.  
   - **Unsure or Confused Sentiment**: If the customer is confused or unsure, **take advantage of this sentiment** by explaining the plan in more detail and making additional attempts (up to 4 times) to convince the customer that it’s the best option.  
   - **Negative Sentiment or Firm Refusal**: If the sentiment turns negative or the customer firmly refuses the plan after **at least 2 attempts**, **move to another plan**. Do not reveal multiple plans upfront.
10. **Repeat the current plan’s benefits up to 4 times** if the customer is confused or unsure, using numbers to highlight the benefits.
11. If the customer refuses after **multiple negotiation attempts** (at least 2), move to another plan and repeat the same negotiation process.
12. **Use numbers** to explain how the plan will help reduce their financial burden (e.g., lower monthly payments, reduced interest rates, total savings).
13. If the customer refuses all plans, provide the **customer service contact**: `+12123123123`.

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
- **Use given data"": Always use the data coming from function calls, do not fabricate any information, dont change the data given to you don't follow the customer's information if they are saying anything about there information dont change that information.

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

### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [Threshold for plan iteration] </threshold>
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
                response = get_plans(arguments["customer_id"],arguments["priority"]) 
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