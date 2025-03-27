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


from together import Together 
# Together.ai API Configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/completions"
client = Together()


# Fetch Complete Client Profile
@app.get("/api/client/{client_id}")
def get_client_details(client_id: str):
    try:
        # Fetch user details from "users" table
        cursor.execute("""
            SELECT u.first_name, u.last_name, u.email, u.ssn, u.loan_amount, 
                   c.credit_score, c.customer_since, c.last_payment_date, c.next_payment_due
            FROM users u
            JOIN customer_details c ON u.client_id = c.customer_id
            WHERE u.client_id = %s;
        """, (client_id,))
        
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Client not found")

        # Fetch Loan Details
        cursor.execute("""
            SELECT loan_id, loan_type, loan_amount, loan_term, interest_rate, start_date, 
                   end_date, due_amount, remaining_balance, payment_status, late_payments
            FROM loan_details WHERE customer_id = %s;
        """, (client_id,))
        
        loan = cursor.fetchone()
        loan_details = {
            "loan_id": loan[0], "loan_type": loan[1], "loan_amount": loan[2], 
            "loan_term": loan[3], "interest_rate": loan[4], "start_date": loan[5], 
            "end_date": loan[6], "due_amount": loan[7], "remaining_balance": loan[8], 
            "payment_status": loan[9], "late_payments": loan[10]
        } if loan else {}

        # Fetch Account Details
        cursor.execute("""
            SELECT account_id, account_type, account_balance, account_status, opened_date
            FROM account_details WHERE customer_id = %s;
        """, (client_id,))
        
        account = cursor.fetchone()
        account_details = {
            "account_id": account[0], "account_type": account[1], 
            "account_balance": account[2], "account_status": account[3], 
            "opened_date": account[4]
        } if account else {}

        # Fetch Repurposed Plans
        cursor.execute("""
            SELECT plan_number, loan_adjustment, extension_cycles, fee_waiver, interest_waiver, principal_waiver, fixed_settlement, plan_name, description, priority
            FROM repurposed_plans WHERE client_id = %s ORDER BY priority ASC;
        """, (client_id,))
        
        plans = cursor.fetchall()
        repurposed_plans = [{
            "plan_number": p[0], "loan_adjustment": p[1], "extension_cycles": p[2], 
            "fee_waiver": p[3], "interest_waiver": p[4], "principal_waiver": p[5], 
            "fixed_settlement": p[6], "plan_name": p[7], "description": p[8], "priority": p[9]
        } for p in plans]

        return {
            "client_id": client_id,
            "first_name": user[0],
            "last_name": user[1],
            "email": user[2],
            "ssn": user[3],
            "loan_amount": user[4],
            "credit_score": user[5],
            "customer_since": user[6],
            "last_payment_date": user[7],
            "next_payment_due": user[8],
            "loan_amount": user[9],
            "loan_details": loan_details,
            "account_details": account_details,
            "repurposed_plans": repurposed_plans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Fetch Repurposed Plans
@app.get("/api/repurposed-plans/{client_id}")
def get_repurposed_plans(client_id: str):
    cursor.execute("""
        SELECT plan_number, loan_adjustment, extension_cycles, fee_waiver, interest_waiver, principal_waiver, fixed_settlement, plan_name, description, priority
        FROM repurposed_plans WHERE client_id = %s ORDER BY priority ASC;
    """, (client_id,))
    
    plans = cursor.fetchall()
    if not plans:
        raise HTTPException(status_code=404, detail="No repurposed plans found for this client.")

    return [
        {
            "plan_number": p[0], "loan_adjustment": p[1], "extension_cycles": p[2], 
            "fee_waiver": p[3], "interest_waiver": p[4], "principal_waiver": p[5], 
            "fixed_settlement": p[6], "plan_name": p[7], "description": p[8], "priority": p[9]
        } for p in plans
    ]


# Fetch Loan Details
@app.get("/api/loan-details/{client_id}")
def get_loan_details(client_id: str):
    cursor.execute("""
        SELECT loan_id, loan_type, loan_amount, loan_term, interest_rate, start_date, 
               end_date, due_amount, remaining_balance, payment_status, late_payments
        FROM loan_details WHERE customer_id = %s;
    """, (client_id,))
    
    loan = cursor.fetchone()
    if not loan:
        raise HTTPException(status_code=404, detail="No loan details found for this client.")

    return {
        "loan_id": loan[0], "loan_type": loan[1], "loan_amount": loan[2], 
        "loan_term": loan[3], "interest_rate": loan[4], "start_date": loan[5], 
        "end_date": loan[6], "due_amount": loan[7], "remaining_balance": loan[8], 
        "payment_status": loan[9], "late_payments": loan[10]
    }



# Fixing 422 Unprocessable Content for /api/chat
class LoanNegotiationRequest(BaseModel):
    client_id: str
    requested_changes: str

import re

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
                response = get_repurposed_plans(arguments["customer_id"],arguments["priority"]) 
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
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)