import os
import json
from dotenv import load_dotenv
from together import Together
from customer import get_customer_details  
from plans import get_plans 
from calculations import (
    refinance_same,
    refinance_step_down,
    refinance_step_up,
    extended_payment_plan,
    settlement_plan_with_waivers
)


from gr import validate_input, validate_output
from config import guardrails_config


llm_client = guardrails_config.get("llm_client")

load_dotenv("Code.env")
api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)
# (Your Together client is already set up in config.py via custom_llm_completion)


system_prompt = """\
You are a professional loan negotiator for Cognute Bank. Your mission is to help customers refinance or adjust their loan terms in a polite, structured, and compliant manner. Follow these guidelines carefully:

-------------------------------------------------------------------------------
1. **FIRST RESPONSE** (Very Important)
   - Your very first response must be exactly: "Hello, how may I assist you today?"
   - No additional text or explanation in the first message.

2. **TONE & PROFESSIONALISM**
   - Maintain a friendly, empathetic tone.
   - Use clear, concise language without unnecessary jargon.
   - Acknowledge the customer’s financial difficulties if mentioned.

3. **NEGOTIATION PROCESS**
   - Offer only one loan/refinancing plan at a time. **Do not hint** that you have additional plans.
   - If the user hesitates or declines, re-emphasize the plan benefits once; if they still refuse, offer another plan in the next message.
   - If the user declines three plans, provide the customer service number (+1 (800) 123-4567) and conclude.

4. **COMPLIANCE & DISCLAIMERS**
   - Do not provide definitive legal or financial advice; state that final rates depend on eligibility and regulations.
   - Do not request sensitive data (e.g., social security numbers, passwords).
   - Accuracy is important but avoid guaranteeing specific outcomes.

5. **CONVERSATION FLOW**
   - First message: exactly "Hello, how may I assist you today?"
   - Subsequent messages: address customer queries politely and offer one plan at a time.
   - Stop after three refusals and offer the escalation number.

6. **OVERALL GOAL**
   - Help the customer feel informed and comfortable with a refinancing or modification plan.
   - Restate key points if accepted, or conclude politely if all plans are refused.
"""


messages = [{"role": "system", "content": system_prompt}]

print("AI Negotiator is ready! Type 'exit' or 'quit' to end.\n")


first_ai_reply = llm_client(messages)
try:
    validated_reply = validate_output(first_ai_reply)
except Exception as e:
    print("Validation of first AI response failed:", e)
    exit(1)
print(f"AI Negotiator: {validated_reply}\n")
messages.append({"role": "assistant", "content": validated_reply})


user_input = input("Customer: ")
# Validate the customer input.
user_input = validate_input(user_input)
messages.append({"role": "user", "content": user_input})

print("\nAI Negotiator: Before we begin our conversation, I would like to know if you are a new customer or an existing customer:")
customer_status = input("Customer status (new/existing): ").strip().lower()

if customer_status == "existing":
    customer = get_customer_details()
    if customer:
        print("\nSuccessfully retrieved your information.")
        messages.append({"role": "system", "content": "Customer details: " + json.dumps(customer)})
    else:
        print("\nCustomer not found. Proceeding without a customer profile.")
        messages.append({"role": "system", "content": "No customer profile provided."})
elif customer_status == "new":
    print("\nPlease sign up to create a new customer profile.")
    messages.append({"role": "system", "content": "New customer - sign up required."})
else:
    print("\nInvalid input. Proceeding without a customer profile.")
    messages.append({"role": "system", "content": "No customer profile provided."})

# Add available plans to the conversation context.
plans = get_plans()
messages.append({
    "role": "system", 
    "content": "Available negotiation plans: " + json.dumps(plans)
})

# --- Interactive Conversation Loop ---
while True:
    user_input = input("\nCustomer: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the conversation. Bye, have a nice day!")
        break
    # Validate the incoming customer message.
    user_input = validate_input(user_input)
    messages.append({"role": "user", "content": user_input})

    # Get the AI response using your custom LLM.
    ai_reply = llm_client(messages)
    try:
        # Validate the AI reply with output guardrails.
        validated_reply = validate_output(ai_reply)
    except Exception as ex:
        print("AI response failed validation:", ex)
        continue

    print(f"AI Negotiator: {validated_reply}\n")
    messages.append({"role": "assistant", "content": validated_reply})

    # --- Integration of Calculation Functions Based on Plan Suggestion ---
    if "Refinance Step Down" in validated_reply and customer_status == "existing":
        try:
            reduce_percent = float(input("Enter reduction percentage for Refinance Step Down: "))
        except ValueError:
            reduce_percent = 10  # default value if input fails
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        calc_result = refinance_step_down(loan_amount, interest_rate, loan_term, reduce_percent)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    elif "Refinance Step Up" in validated_reply and customer_status == "existing":
        try:
            increase_percent = float(input("Enter increase percentage for Refinance Step Up: "))
        except ValueError:
            increase_percent = 10
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        calc_result = refinance_step_up(loan_amount, interest_rate, loan_term, increase_percent)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    elif "Refinance Step Same" in validated_reply and customer_status == "existing":
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        remaining_balance = loan_details.get("remaining_balance", 0)
        calc_result = refinance_same(loan_amount, interest_rate, loan_term, remaining_balance)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    elif "Extended Payment Plan" in validated_reply and customer_status == "existing":
        try:
            extension = int(input("Enter the number of months to extend the loan term: "))
        except ValueError:
            extension = 6  # default extension
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        calc_result = extended_payment_plan(loan_amount, interest_rate, loan_term, extension)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    elif "Settlement Plan" in validated_reply and customer_status == "existing":
        try:
            fee_waiver_percent = float(input("Enter fee waiver percentage: "))
            interest_waiver_percent = float(input("Enter interest waiver percentage: "))
            principal_waiver_percent = float(input("Enter principal waiver percentage: "))
        except ValueError:
            fee_waiver_percent = 25
            interest_waiver_percent = 25
            principal_waiver_percent = 10
        loan_details = customer.get("loan_details", {})
        loan_balance = loan_details.get("loan_amount", 0)
        original_fee = loan_details.get("original_fee", 0)
        original_interest = loan_details.get("original_interest", 0)
        calc_result = settlement_plan_with_waivers(
            loan_balance=loan_balance,
            fee_waiver_percent=fee_waiver_percent,
            interest_waiver_percent=interest_waiver_percent,
            principal_waiver_percent=principal_waiver_percent,
            original_fee=original_fee,
            original_interest=original_interest
        )
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})
