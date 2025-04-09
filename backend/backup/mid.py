from decimal import Decimal
import os
import requests
import jwt
import psycopg2
import random
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from dotenv import load_dotenv
from jose import JWTError
from fastapi.middleware.cors import CORSMiddleware
import xml.etree.ElementTree as ET
import json
import re
from guardrails import enforce_input_guardrails, enforce_output_guardrails, is_rate_limited, log_flagged_input


from calculation import (
    refinance_same,
    refinance_step_down,
    refinance_step_up,
    extended_payment_plan,
    settlement_plan_with_waivers
)


# Load environment variables
load_dotenv()

# PostgreSQL Connection
DATABASE_URL = os.getenv("DATABASE_URL", "dbname=ainegotiator user=admin password=yourpassword host=localhost port=5432")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# JWT Secret Key
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Token Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

app = FastAPI()

# CORS Middleware (Allow frontend to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models (Schemas)
class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    ssn: str
    loan_amount: float

class TokenData(BaseModel):
    email: str

class ClientVerification(BaseModel):
    client_id: str
    passcode: str


# JWT Token Utility Functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def generate_repurposed_plans(client_id, loan_amount):
    plans = [
        {"plan_number": 1, "loan_adjustment": loan_amount * 0.1, "extension_cycles": 0, "fee_waiver": 0, "interest_waiver": 0, "principal_waiver": 0, "fixed_settlement": 0},
        {"plan_number": 2, "loan_adjustment": 0, "extension_cycles": 3, "fee_waiver": 0, "interest_waiver": 0, "principal_waiver": 0, "fixed_settlement": 0},
        {"plan_number": 3, "loan_adjustment": 0, "extension_cycles": 0, "fee_waiver": 25, "interest_waiver": 0, "principal_waiver": 0, "fixed_settlement": 0},
        {"plan_number": 4, "loan_adjustment": 0, "extension_cycles": 0, "fee_waiver": 100, "interest_waiver": 25, "principal_waiver": 0, "fixed_settlement": 0},
        {"plan_number": 5, "loan_adjustment": 0, "extension_cycles": 0, "fee_waiver": 100, "interest_waiver": 100, "principal_waiver": 5, "fixed_settlement": 1000}
    ]

    for plan in plans:
        query = """
        INSERT INTO repurposed_plans (client_id, plan_number, loan_adjustment, extension_cycles, fee_waiver, interest_waiver, principal_waiver, fixed_settlement)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (client_id, plan["plan_number"], plan["loan_adjustment"], plan["extension_cycles"], plan["fee_waiver"], plan["interest_waiver"], plan["principal_waiver"], plan["fixed_settlement"]))
    
    conn.commit()



# Signup Endpoint - Register a User
@app.post("/api/signup")
def signup(user: UserSignup):
    try:
        client_id = str(random.randint(10000, 99999))
        hashed_password = pwd_context.hash(user.password)

        query = """
        INSERT INTO users (first_name, last_name, email, password, client_id, ssn, loan_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING client_id;
        """
        cursor.execute(query, (user.first_name, user.last_name, user.email, hashed_password, client_id, user.ssn, user.loan_amount))
        conn.commit()

        # Generate all 5 repurposed plans
        generate_repurposed_plans(client_id, user.loan_amount)

        return {"message": "User registered successfully!", "client_id": client_id}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# Login Endpoint - Get JWT Token
@app.post("/api/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = "SELECT email, password FROM users WHERE email = %s;"
    cursor.execute(query, (form_data.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    stored_hashed_password = user[1]

    if not pwd_context.verify(form_data.password, stored_hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(data={"sub": user[0]})
    return {"access_token": access_token, "token_type": "bearer"}


# User Verification for Chatbot
@app.post("/api/verify")
def verify_user(request: ClientVerification):
    query = "SELECT client_id, password FROM users WHERE client_id = %s;"
    cursor.execute(query, (request.client_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid Client ID")

    stored_hashed_password = user[1]
    if not pwd_context.verify(request.passcode, stored_hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Passcode")

    return {"message": "Access Granted"}


#Protected Route Example (Only Accessible with JWT)
@app.get("/api/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        return {"message": "You have access!", "user_email": user_email}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
@app.get("/api/userinfo")
def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")

        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        query = "SELECT client_id FROM users WHERE email = %s;"
        cursor.execute(query, (user_email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"client_id": user[0]}  

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token format")


# Store Chat Message in Database
class ChatMessage(BaseModel):
    client_id: str
    sender: str
    message: str

@app.post("/api/chat")
def store_chat_message(chat: ChatMessage, token: str = Depends(oauth2_scheme)):
    if chat.sender not in ["user", "bot"]:
        raise HTTPException(status_code=400, detail="Invalid sender type")
    query = """
    INSERT INTO chat_history (client_id, sender, message) 
    VALUES (%s, %s, %s);
    """
    cursor.execute(query, (chat.client_id, chat.sender, chat.message))
    conn.commit()
    return {"message": "Chat message stored successfully"}

# Fixing 500 Internal Server Error for /api/negotiate
class LoanNegotiationRequest(BaseModel):
    client_id: str
    current_plan: str
    requested_changes: str
    prompt: str


# Retrieve Chat History for a Client
@app.get("/api/chat/{client_id}")
def get_chat_history(client_id: str, token: str = Depends(oauth2_scheme)):
    query = "SELECT sender, message, timestamp FROM chat_history WHERE client_id = %s ORDER BY timestamp ASC;"
    cursor.execute(query, (client_id,))
    chat_records = cursor.fetchall()

    if not chat_records:
        return {"chat_history": []}  # Return empty list if no history

    return {
        "chat_history": [
            {"sender": row[0], "message": row[1], "timestamp": row[2]} for row in chat_records
        ]
    }

# Delete Chat History
@app.delete("/api/chat/clear/{client_id}")
def clear_chat_history(client_id: str):
    try:
        cursor.execute("DELETE FROM chat_history WHERE client_id = %s", (client_id,))
        conn.commit()
        return {"message": "Chat history cleared successfully."}
    except Exception as e:
        print(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear chat history.")



#Root Route
@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI"}


# Fixing 422 Unprocessable Content for /api/chat
class LoanNegotiationRequest(BaseModel):
    client_id: str
    requested_changes: str

@app.get("/api/client/{client_id}")
def get_client_details():
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


@app.get("/api/repurposed_plans/{client_id}")
def get_plans(customer_id:str):
    repayment_plans = {
        "CUST654321":{
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
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 2,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Begin by offering the 10% decrease option as the best and only available solution. Emphasize its benefits using values from the function (e.g., reduced monthly payments and lower financial burden).",
    "2. Call the appropriate function to calculate and present the updated values that show how the 10% reduction benefits the customer.",
    "3. Stick to the 10% decrease option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further convince the customer (e.g., explaining how this reduction keeps payments affordable while easing their financial strain).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% reduction is the best and only available option** for now, explaining why it is ideal for their current financial situation using function-derived values.",
    "5. Only after three iterations of explaining the 10% reduction, if the customer still resists, introduce the next step (20%) while emphasizing why the 10% decrease was an essential first step.",
    "6. Ensure to go in order (10% → 20% → 30%...50%) and never skip steps. Reinforce the current option using calculated values from the function before moving forward to the next percentage."
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
  "priority": 3,
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
  "priority": 4,
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
  "priority": 5,
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
  "description": "Increase loan amount in steps of 10%, max up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Begin by offering the 10% increase option and presenting it as the only and best available solution. Emphasize its benefits using values from the function (e.g., how much cash they would get and how manageable the payments remain).",
    "2. Call the appropriate function to calculate and present updated values that showcase the benefits of the current option.",
    "3. Stick to the 10% increase option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further explain how this option improves the customer’s financial situation (e.g., lower payment impact, immediate cash benefits).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% increase is the best and only available option** at the moment. Explain why this step is optimal for their current needs and use calculated values from the function.",
    "5. Only after three iterations of explaining the 10% increase, if the customer continues to resist, introduce the next step (20%) while emphasizing why the previous step was ideal and necessary to build toward larger changes.",
    "6. Ensure to go in order, from 10% to 20%, never skipping steps, and continue to reinforce the current option using function-derived values before moving forward."
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
    "1. Begin by offering the 10% decrease option as the best and only available solution. Emphasize its benefits using values from the function (e.g., reduced monthly payments and lower financial burden).",
    "2. Call the appropriate function to calculate and present the updated values that show how the 10% reduction benefits the customer.",
    "3. Stick to the 10% decrease option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further convince the customer (e.g., explaining how this reduction keeps payments affordable while easing their financial strain).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% reduction is the best and only available option** for now, explaining why it is ideal for their current financial situation using function-derived values.",
    "5. Only after three iterations of explaining the 10% reduction, if the customer still resists, introduce the next step (20%) while emphasizing why the 10% decrease was an essential first step.",
    "6. Ensure to go in order (10% → 20% → 30%...50%) and never skip steps. Reinforce the current option using calculated values from the function before moving forward to the next percentage."
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
}
      ]},
    
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



from together import Together 
# Together.ai API Configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/completions"
client = Together()

#Helper function to safely convert Decimal to float
def safe_float(value):
    return float(value) if isinstance(value, Decimal) else value

#Request Model
class LoanNegotiationRequest(BaseModel):
    client_id: str
    requested_changes: str

class Conversation:
    def __init__(self,system=""):
        self.messages = []
        self.tools  = [{
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
                "required": ["loan_amount", "interest_rate", "loan_term","remaining_balance", "due"]
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
                    "reduce_percent": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                    
                },
                "required": ["loan_amount", "interest_rate", "loan_term", "reduce_percent","remaining_balance", "due"]
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
                "increase_percent": {"type": "number", "description": "Percentage to increase the loan amount by"},
                "remaining_balance": { "type": "number" },
                "due": {"type": "number"},
            },
            "required": ["loan_amount", "interest_rate", "loan_term", "increase_percent","remaining_balance", "due"]
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
        response = response.choices[0].message.content
        root = ET.fromstring(response)
        customer_content = root.find('customer').text.strip()
        threshold = root.find('threshold').text.strip()
        sentiment = root.find('sentiment').text.strip()
        print(threshold+' '+sentiment)
        self.messages.append({"role":"assistant","content":response})
        return customer_content
    
    def function_calling(self,response):
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
              result = get_client_details()
              tool_result = f"<customer_details>{(result)}</customer_details>"
          else:
              response = get_plans(arguments["customer_id"])
              tool_result = """<plans>"""+response+"""</plans>"""

          self.messages.append({
          "role":"tool",
          "name": functionname,
          "content":tool_result})

          response = client.chat.completions.create(
          model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
          messages= self.messages,
          max_tokens=300,
          tools=self.tools,
          tool_choice="auto",
          temperature=0.2,
          )
        return response

class PromptRequest(BaseModel):
    prompt: str

prompt = """
####Role:
You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.

###Objective:
Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan will reduce their financial burden. Monitor customer sentiment to decide when to stick with a plan or move to another.

###Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
2. Request the Client ID and wait for their response.**Call the function `get_client_details(client_id)`** to retrieve customer information ONLY once.
3. Once you have the customer info, provide the customer’s due amount and remaining_balance with th due date(e.g., $X due) and ask about their current financial situation to better assist them.
4. **Call get_plans(str(customer_id))** only once after the customer explains their situation to retrieve all available plans in priority starting from 1 for the customer. 
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
  **2 Neagitive: He want to move to the next plan and dont want to proceed with the current plan. Assign a value between 1 to 2 to threshold.
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
You must ALWAYS respond strictly in this XML format:

<response>
  <customer>[response here]</customer>
  <sentiment>[sentiment category]</sentiment>
  <threshold>[threshold integer]</threshold>
</response>

Do not return any extra text. Only return XML.

"""


message = {
    "role": "system",
    "content": prompt
}

messages = [message]

    
conv = Conversation(system=prompt)

class NegotiationRequest(BaseModel):
    client_id: str
    current_plan: str = None  # Optional if not always needed
    requested_changes: str
    prompt: str


#Negotiator
@app.post("/api/negotiate")
def negotiate_loan(request: NegotiationRequest):
    try:
        print("Received request:", request.dict())  # Debugging

        client_id = str(request.client_id).strip()
        if not client_id:
            raise HTTPException(status_code=400, detail="Client ID is required.")

        if not request.requested_changes or len(request.requested_changes.strip()) == 0:
            raise HTTPException(status_code=400, detail="Requested changes cannot be empty.")
        
        
    
        # Call AI negotiation
        ai_response = conv.generate(request.prompt)
        

        if not ai_response or not isinstance(ai_response, str):
            raise HTTPException(status_code=500, detail="AI response is empty or invalid.")



        # Extract the <response> XML block safely
        # match = re.search(r"<response>.*?</response>", ai_response, re.DOTALL)
        # if not match:
        #     print("Malformed AI response:", ai_response)
        #     raise HTTPException(status_code=500, detail="AI response did not contain valid <response> XML block.")

        # xml_response = match.group(0)

        # try:
        #     root = ET.fromstring(xml_response)
        # except ET.ParseError as e:
        #     print("XML parsing error:", str(e))
        #     raise HTTPException(status_code=500, detail="Failed to parse AI XML response.")

        # customer_node = root.find("customer")
        # if customer_node is None or customer_node.text is None:
        #     raise HTTPException(status_code=500, detail="Missing <customer> tag or text in AI response.")

        # customer_content = customer_node.text.strip()

        #Output Guardrails
        # if not enforce_output_guardrails(customer_content):
        #     raise HTTPException(status_code=500, detail="AI response failed content guardrails.")
        
        # Store chat history
        # cursor.execute(
        #     "INSERT INTO chat_history (client_id, sender, message) VALUES (%s, %s, %s)",
        #     (client_id, "bot", customer_content)
        # )
        # conn.commit()

        return {"negotiation_response": ai_response}

    except Exception as e:
        print(f"Error in /api/negotiate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    


@app.post("/api/chat")
async def chat_generation(request: PromptRequest):
    try:
        response = conv.generate(request.prompt)
        return {"message":response}
    except Exception as e:
        return {"error": str(e)}

#Run FastAPI App
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)