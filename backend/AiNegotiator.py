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
import re

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


# Client Profile
@app.get("/api/client/{client_id}")
def get_client_profile(client_id: str, token: str = Depends(oauth2_scheme)):
    query = "SELECT first_name, last_name, email, ssn, loan_amount FROM users WHERE client_id = %s;"
    cursor.execute(query, (client_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="Client not found")

    query = "SELECT plan_number, loan_adjustment, extension_cycles, fee_waiver, interest_waiver, principal_waiver, fixed_settlement FROM repurposed_plans WHERE client_id = %s;"
    cursor.execute(query, (client_id,))
    plans = cursor.fetchall()

    return {
        "client_id": client_id,
        "first_name": user[0],
        "last_name": user[1],
        "email": user[2],
        "ssn": user[3],
        "loan_amount": user[4],
        "repurposed_plans": [
            {"plan_number": p[0], "loan_adjustment": p[1], "extension_cycles": p[2], "fee_waiver": p[3], "interest_waiver": p[4], "principal_waiver": p[5], "fixed_settlement": p[6]} for p in plans
        ]
    }



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

# Together.ai API Configuration
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/completions"


# Fetch Client Details
@app.get("/api/client/{client_id}")
def get_client_details(client_id: str):
    cursor.execute("SELECT first_name, last_name, email, loan_amount FROM users WHERE client_id = %s", (client_id,))
    user_data = cursor.fetchone()
    if not user_data:
        raise HTTPException(status_code=404, detail="Client not found")
    return {
        "client_id": client_id,
        "first_name": user_data[0],
        "last_name": user_data[1],
        "email": user_data[2],
        "loan_amount": user_data[3]
    }

# Fetch Repurposed Plans
@app.get("/api/repurposed-plans/{client_id}")
def get_repurposed_plans(client_id: str):
    cursor.execute(
        "SELECT plan_number, loan_adjustment, extension_cycles, fee_waiver, interest_waiver, principal_waiver, fixed_settlement FROM repurposed_plans WHERE client_id = %s ORDER BY plan_number",
        (client_id,)
    )
    plans = cursor.fetchall()
    if not plans:
        raise HTTPException(status_code=404, detail="No repurposed plans found for this client.")
    return [
        {
            "plan_number": p[0],
            "loan_adjustment": p[1],
            "extension_cycles": p[2],
            "fee_waiver": p[3],
            "interest_waiver": p[4],
            "principal_waiver": p[5],
            "fixed_settlement": p[6]
        } for p in plans
    ]

# Fixing 422 Unprocessable Content for /api/chat
class LoanNegotiationRequest(BaseModel):
    client_id: str
    requested_changes: str

import re

# AI Model Call
def call_llama3(prompt: str):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "prompt": prompt,
        "max_tokens": 400,  
        "temperature": 0.6  
    }

    try:
        response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
        print("Llama API Response:", response.status_code, response.text)

        if response.status_code == 200:
            ai_response = response.json().get("choices")[0].get("text").strip()
            return ai_response
        else:
            raise HTTPException(status_code=500, detail=f"Llama API error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"Error calling Llama API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Llama API call failed: {str(e)}")


@app.post("/api/negotiate")
def negotiate_loan(request: LoanNegotiationRequest):
    try:
        # Fetch client details
        client_data = get_client_details(request.client_id)
        loan_amount = client_data["loan_amount"]

        # Fetch available repurposed plans
        repurposed_plans = get_repurposed_plans(request.client_id)
        if not repurposed_plans:
            raise HTTPException(status_code=404, detail="No available plans for this client.")

        # Select the first plan for negotiation
        selected_plan = repurposed_plans[0]


        # Identify user intent
        #user_message = request.requested_changes.strip().lower()
        #keywords_refinance = ["refinance", "loan modification", "change loan terms"]
        #keywords_payment_help = ["help paying", "lower payment", "reduce payment", "can't pay"]
        #keywords_info = ["balance", "how much", "loan amount"]

        #XML-based AI negotiation prompt
        negotiation_prompt = f"""
<negotiation>
    <loan_officer>
        <role>You are a professional loan officer at a top financial institution in the USA.</role>
        <instructions>
            - Start with a **greeting** and confirm the client's request.
            - **DO NOT offer another plan unless the client explicitly rejects the current one.**
            - If the client **confirms a plan**, acknowledge it and **finalize the negotiation**.
            - The **final response** should be enclosed in `<message_to_client></message_to_client>`.
        </instructions>
    </loan_officer>

    <client>
        <id>{request.client_id}</id>
        <loan_amount>${loan_amount:.2f}</loan_amount>
        <request>{request.requested_changes}</request>
    </client>

    <conversation>
        <greeting>Hello {client_data["first_name"]}, I’m happy to assist you today. How can I help with your loan of ${loan_amount:.2f}?</greeting>
        <negotiation_step>Let's discuss your situation. Can you tell me what challenges you're facing with your loan?</negotiation_step>
    </conversation>

    <recommended_plan>
        <plan_number>{selected_plan["plan_number"]}</plan_number>
        <loan_adjustment>${selected_plan["loan_adjustment"]}</loan_adjustment>
        <extension_cycles>{selected_plan["extension_cycles"]}</extension_cycles>
        <fee_waiver>{selected_plan["fee_waiver"]}%</fee_waiver>
        <interest_waiver>{selected_plan["interest_waiver"]}%</interest_waiver>
        <principal_waiver>{selected_plan["principal_waiver"]}%</principal_waiver>
        <fixed_settlement>${selected_plan["fixed_settlement"]}</fixed_settlement>
    </recommended_plan>

    <client_confirmation>
        - If the client **accepts** the plan, respond with:  
          **"Thank you for confirming. We will now proceed with finalizing your agreement."**
        - If the client **rejects**, DO NOT suggest a new plan unless they explicitly request another option.
    </client_confirmation>

    <message_to_client>
        AI-GENERATED RESPONSE HERE
    </message_to_client>
</negotiation>
"""

        # Get AI-generated response
        ai_response = call_llama3(negotiation_prompt)

        # Extract only the message from AI response
        final_response = extract_final_response(ai_response)

        if not final_response or final_response.strip() == "":
            final_response = "I'm sorry, but I couldn't process your request. Can you clarify?"

        # Store the chat history in DB
        cursor.execute(
            "INSERT INTO chat_history (client_id, sender, message) VALUES (%s, %s, %s)",
            (request.client_id, "bot", final_response)
        )
        conn.commit()

        return {"negotiation_response": final_response}

    except Exception as e:
        print(f"Error in /api/negotiate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Extract AI Response
def extract_final_response(ai_response):
    """
    Extracts only the <message_to_client> section from the AI response.
    If no specific message is found, returns a default response.
    """
    try:
        # Ensure response is in string format
        if not isinstance(ai_response, str):
            raise ValueError("AI response is not a string.")

        # Extract the message inside <message_to_client> tags
        match = re.search(r'<message_to_client>(.*?)</message_to_client>', ai_response, re.DOTALL)

        if match:
            return match.group(1).strip()

        return "I'm sorry, but I couldn't process your request. Can you clarify?"
    
    except Exception as e:
        print(f"Error extracting message: {str(e)}")
        return "I'm sorry, but there was an error processing your request."


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)