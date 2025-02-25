import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock borrower financial data 
BORROWER_DATA = {
    "loan_amount": 5000,
    "overdue_amount": 252.60,
    "overdue_days": 2,
    "payment_history": "Good",
    "past_delinquencies": 1
}

# Borrower Request Model
class BorrowerRequest(BaseModel):
    message: str
    history: list = []  # Track conversation history

# Function to detect user intent and emotional state
def detect_intent(user_message):
    """Detects the intent and urgency in a user's message."""
    user_message = user_message.lower()

    # Emotion detection: Identify frustration, confusion, or urgency
    if "can't pay" in user_message or "struggling" in user_message:
        emotion = "frustration"
    elif "help" in user_message or "urgent" in user_message:
        emotion = "urgent"
    else:
        emotion = "neutral"

    # Detect if user is asking about payment, overdue, loan settlement, etc.
    if "overdue" in user_message or "owe" in user_message:
        intent = "overdue_amount"
    elif "payment plan" in user_message or "how to pay" in user_message:
        intent = "payment_plan"
    elif "fees" in user_message or "waiver" in user_message:
        intent = "fee_waiver"
    elif "settle loan" in user_message or "lower loan" in user_message:
        intent = "loan_settlement"
    else:
        intent = "general_query"

    return emotion, intent

# Function to generate repayment plan example
def generate_repayment_plan():
    """Generates a sample repayment plan with dynamic values."""
    loan_amount = BORROWER_DATA["loan_amount"]
    overdue_amount = BORROWER_DATA["overdue_amount"]
    
    # Example repayment options
    repayment_plan_example = {
        "Refinance": f"Refinance your loan. The new loan amount would be: ${loan_amount * 1.1}.",
        "Extended Payment Plan": f"Extend your loan payment period by 3 cycles. New monthly payments will be adjusted.",
        "Waive Partial Fees": f"We can waive 25% of your overdue fees. Total fees will be reduced by ${overdue_amount * 0.25}.",
        "Loan Settlement": f"You can settle your loan for a reduced amount between $1000 and $200. A suggested settlement is $2500."
    }
    
    return repayment_plan_example

# Function to generate dynamic, human-like responses based on user input
def generate_dynamic_response(emotion, intent, user_message):
    """Generates dynamic responses based on user message and intent."""
    
    if emotion == "frustration":
        return "I understand it can be tough. Let’s look at some options to help ease the payment process."
    
    if emotion == "urgent":
        return "This seems urgent. Let's quickly go through your best options to manage this debt."

    if intent == "overdue_amount":
        return f"Your overdue amount is ${BORROWER_DATA['overdue_amount']}. I can help you explore options for managing this amount."

    if intent == "payment_plan":
        return "We offer flexible payment plans that can extend the term of your loan. Would you like me to provide more details?"

    if intent == "fee_waiver":
        return "We can waive a portion of your fees depending on your payment history. Let me check if you qualify."

    if intent == "loan_settlement":
        return "We can offer a settlement amount for your loan, which could be as low as $1000 depending on your situation."

    if intent == "general_query":
        return "Could you clarify your question? I’m here to assist with your loan and any related issues."

    return "Could you please clarify your concern? I’m here to assist with your loan."

@app.post("/chat")
async def chatbot(request: BorrowerRequest):
    """Handles borrower queries and provides dynamic, personalized responses based on intent."""
    
    user_message = request.message
    # Detect emotion and intent dynamically
    emotion, intent = detect_intent(user_message)
    
    # Generate the appropriate dynamic response
    response = generate_dynamic_response(emotion, intent, user_message)
    
    return {"response": response}

@app.get("/")
async def home():
    return {"message": "FastAPI backend for AI Negotiator is running!"}
