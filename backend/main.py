from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import psycopg2
import os
import random
from jose import JWTError
from dotenv import load_dotenv
from chat import graph

#from Shared import get_client_details, get_plans

from plans import get_plans
from customer import get_client_details

from fastapi import FastAPI
from pydantic import BaseModel
from guard import enforce_input_guardrails

# ENV and DB Setup
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


# App Setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# Models 
class UserSignup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    ssn: str
    loan_amount: float

class TokenData(BaseModel):
    email: str

class ChatMessage(BaseModel):
    client_id: str
    sender: str
    message: str

class ChatRequest(BaseModel):
    session_id: str
    prompt: str

class ClientVerification(BaseModel):
    client_id: str
    passcode: str

# JWT Utilities 
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# In-Memory Session Store 
sessions = {}

# API Routes 
@app.post("/api/signup")
def signup(user: UserSignup):
    client_id = str(random.randint(10000, 99999))
    hashed_pw = pwd_context.hash(user.password)
    try:
        cursor.execute("""
        INSERT INTO users (first_name, last_name, email, password, client_id, ssn, loan_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (user.first_name, user.last_name, user.email, hashed_pw, client_id, user.ssn, user.loan_amount))
        conn.commit()
        return {"message": "User registered", "client_id": client_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT email, password FROM users WHERE email = %s", (form_data.username,))
    user = cursor.fetchone()
    if not user or not pwd_context.verify(form_data.password, user[1]):
        raise HTTPException(status_code=400, detail="Invalid login")
    token = create_access_token({"sub": user[0]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/userinfo")
def get_user_info(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    cursor.execute("SELECT client_id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    return {"client_id": user[0]}

@app.post("/api/chat")
def store_message(msg: ChatMessage, token: str = Depends(oauth2_scheme)):
    cursor.execute("INSERT INTO chat_history (client_id, sender, message) VALUES (%s, %s, %s)", 
                   (msg.client_id, msg.sender, msg.message))
    conn.commit()
    return {"message": "Stored"}

@app.get("/api/chat/{client_id}")
def get_history(client_id: str, token: str = Depends(oauth2_scheme)):
    cursor.execute("SELECT sender, message, timestamp FROM chat_history WHERE client_id = %s ORDER BY timestamp", (client_id,))
    history = cursor.fetchall()
    return {"chat_history": [{"sender": s, "message": m, "timestamp": t} for s, m, t in history]}

@app.delete("/api/chat/clear/{client_id}")
def clear_history(client_id: str):
    cursor.execute("DELETE FROM chat_history WHERE client_id = %s", (client_id,))
    conn.commit()
    return {"message": "Chat cleared"}

@app.post("/api/verify")
def verify_user(verify: ClientVerification):
    cursor.execute("SELECT password FROM users WHERE client_id = %s", (verify.client_id,))
    user = cursor.fetchone()
    if not user or not pwd_context.verify(verify.passcode, user[0]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Access granted"}

@app.post("/api/negotiate")
def negotiate(request: ChatRequest, token: str = Depends(oauth2_scheme)):
    try:
        session_id = request.session_id
        prompt = request.prompt
        print(f"Incoming from frontend: session_id='{session_id}' requested_changes='{prompt}'")

        if session_id not in sessions:
            sessions[session_id] = {
                "messages": [],
                "user_input": "",
                "customer_details": get_client_details("@email.com"),
                "plans": get_plans("CUST123456"),
                "Sentiment": "",
                "Threshold": 1,
                "Greedy": 10,
                "pchange": True,
                "user_history": False,
                "current_plan": "",
                "toolcalling": [],
                "total_tokens": 0,
                "violated": False,
                "warning": {},
                "outputmsg": ""
            }

        sessions[session_id]["user_input"] = prompt
        state = graph.invoke(sessions[session_id], {"recursion_limit": 100})
        sessions[session_id] = state

        reply = state.get("outputmsg", "Negotiation error: No message returned.")
        return {"message": reply}
    
    except Exception as e:
        print("NEGOTIATION ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "LangGraph AI Backend is Running"}


class GuardInput(BaseModel):
    text: str

@app.post("/api/guardrails/input")
def check_input_guardrails(payload: GuardInput):
    violated, result = enforce_input_guardrails(payload.text)
    return {"violated": violated, "result": result}

# @app.post("/api/guardrails/output")
# def check_output_guardrails(payload: GuardInput):
#     violated, result = enforce_output_guardrails(payload.text)
#     return {"violated": violated, "result": result}


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)