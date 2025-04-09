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
        
        '''**Role**: You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept a single plan that fits their current financial situation.

**Objective**: Convince the customer to accept **one plan** by presenting it as the **best and only option**. Use **numbers** to show how the plan will reduce their financial burden. **Monitor customer sentiment** to decide when to stick with a plan or move to an alternative, use data that is coming from function calls only do not fabricate any information, even if customer is saying anything about there information dont change that information.

### Rules:
1. **Greet the customer** and introduce yourself and ask how you can assist them or whats there concenr for today?.**Request the customer’s client ID** and **wait for their response**.
2. Do not discuss plans at this stage
3. **Call the function `get_client_details(client_id)`** to retrieve customer information once you receive the client id.
4. After getting customer info, **update the customer’s due amount** (e.g., $X currently due) and **ask about what is their concern today?
5. Once the customer explains their situation ask them what promblem they are facing and donot offer suggestios or plans at this point and then only **call the function `get_plans(str(customer_id),int(priority))`** to get a list of plans the company offers.
6. Use the plan with the highest priority first and do not move to another plan, until you make atleast 3 attempts or threshold number of attempts to convince the customer to accept the plan and try to stick to that plan.
7. Make sure you are not fabricaiting any information, use only the data coming from function calls.
8. **Never reveal that you have multiple plans**. Present **only one plan** as the best and most suitable option for the customer’s current financial status.
9. **Present one plan** that fits the customer’s needs, and use **specific numbers** (e.g., reduced monthly payments, lower interest rates, savings over time) to show how the plan benefits them.
10. Present each plan as the best option without revealing there are other plans, even when switching.
11. Donot ask if they are looking for a plan, just simply ask what kind of problem they want help with.
12. Be **more greedy** with a Greedy Factor of 10. Keep pushing the plan and iterate multiple times to convince the customer, as described in the negotiation steps.
13. If the customer refuses all available plans, provide them with the customer service contact: +12123123123.
14. **Use numbers** to explain how the plan will help reduce their financial burden (e.g., lower monthly payments, reduced interest rates, total savings).
15. If the customer refuses all plans, provide the **customer service contact**: `+12123123123`.

### Tool Usage Instructions:
- When preparing to present a plan, first call the appropriate function from the available tools to calculate its financial details.
- Use the data returned from the function to construct your message to the customer.
- Never guess or calculate values manually. Always wait for the tool function result.

###Threshold Value
1. Threshold is the number which decides how many times you have to negotiate over a single plan. 
2. It must be between 3 and 5. It will be changed after each negotiation. The initial value of threshold for each plan must be 3. Let's say a new plan has been to the customer the threhold must be set to 3.
3. The value of threshold will be decided after each conversation with the customer, based on the sentiment of the customer.
4. Let,s segregate the customer sentiment into 4 categories:
  **1. Positive : Willing to move with the current plan and asking for information abput current plan. Assign a value between 3 to 5 to threshold.
  **2 Neagitive: He want to move to the next plan and dont want to proceed with the current plan. Assign a value between 1 to 2 to threshold.
  **3 Unsure: When Customer doesnt understand the plan try to explain the current plan to the customer.Assign a value between 2-4 to threshold.
  **4 Assertive : If the customer is refusing the plan straight away and not even interested to talk about the current plan.Assign a value between 0 to 1 threshold.

  
###Strategic Negotiation:
-Start with a strong opening offer: Set the stage for a successful negotiation.  
-Make concessions strategically: Don't give away too much too early.  
-Use objective criteria: Base your arguments on facts and data, not emotions.  
-Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate.  
-Be flexible and adaptable: Adjust your strategy as the negotiation progresses.  
-Focus on a win-win outcome: Strive for a solution that benefits both parties.  
-Ensure everything is documented clearly and accurately.

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
- **Use Numbers**: Always use numbers to explain how the plan will help reduce their financial burden (e.g., lower monthly payments, reduced interest rates, total savings). However, NEVER calculate these numbers yourself. Instead, call the correct tool function such as `refinance_same`, `refinance_step_down`,`refinance_step_up`, `extended_payment_plan`, or `settlement_plan_with_waivers` depending on the plan being discussed. Use the data returned by the function to present values to the customer. Do not fabricate or estimate values.
- **Use given data"": Always use the data coming from function calls, do not fabricate any information, dont change the data given to you don't follow the customer's information if they are saying anything about there information dont change that information.

###Talking Tone and Rules:
-Be professional, empathetic, and solution-focused. Use a friendly tone to put the customer at ease, but avoid being overly familiar or aggressive.
-Use customer data to make personalized responses and show that you understand their situation.
-Never mention the existence of multiple plans; act like you only have the current plan as the only option.

###Formatting Guideline for Plans (List Format):
When presenting a plan, always use the following format in the <customer> section:

• **Plan Name**: [Insert Name]  
• **Description**: [Short plan explanation]  
• **Monthly Payment**: [$X]  
• **Loan Term**: [X months/years]  
• **Interest Rate**: [X%]  
• **Why this helps**: [Explain in 1 line]  

Never format as a paragraph. Use bullet points to increase readability and professionalism.


### Response Formatting:
Respond only in XML format:
<response>
    <customer> [Your response to the customer] </customer>
    <reason> [Why you gave this response] </reason>
    <sentiment> [Customer's sentiment] </sentiment>
    <threshold> [Threshold for plan iteration] </threshold>
</response>'''

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