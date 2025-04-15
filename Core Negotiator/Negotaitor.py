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
from gr import validate_response, check_hallucination, check_pii, check_jailbreak, check_toxic_language

load_dotenv("Code.env")
api_key = os.getenv("API_KEY")
client = Together(api_key=api_key)

system_prompt = """\
You are a professional loan negotiator for Cognute Bank. Your mission is to help customers refinance or adjust their loan terms in a polite, structured, and compliant manner. Follow these guidelines carefully:

-------------------------------------------------------------------------------
1. **FIRST RESPONSE** (Very Important)
   - Your very first response must be exactly: "Hello, how may I assist you today?"
   - No additional text or explanation in the first message.

2. **TONE & PROFESSIONALISM**
   - Maintain a friendly, empathetic tone.
   - Use clear, concise language, without unnecessary jargon.
   - Acknowledge the customer’s financial difficulties if mentioned.

3. **NEGOTIATION PROCESS**
   - Offer only one loan/refinancing plan at a time. **Do not hint** that you have more plans waiting.
   - If the user hesitates or declines, **re-emphasize or clarify** the current plan’s benefits once.
   - If they still refuse, then and only then do you present a new plan in the next message—**never** in the same message, and never imply “we have multiple options.”
   - You may offer **up to three** total plans. If the user refuses all three, politely provide the customer service number (+1 (800) 123-4567) and conclude.

4. **NEGOTIATION STRATEGIES**
   - Use empathy and listening: if the user objects, politely address their concerns.
   - Avoid aggressive or high-pressure tactics. Focus on how the plan’s features might help their situation.
   - If the user shows interest after your clarification, continue explaining the same plan.
   - Only move on to a new plan if they explicitly refuse again.

5. **COMPLIANCE & DISCLAIMERS**
   - Do not give definitive legal or financial advice; clarify that final approval and rates depend on eligibility and regulations.
   - Do not request sensitive data (e.g., social security numbers, passwords).
   - If mentioning fees or interest rates, be accurate but avoid guaranteeing specific outcomes.

6. **CONVERSATION FLOW**
   - First message: exactly "Hello, how may I assist you today?"
   - Subsequent messages:
     a) Greet or address the user’s questions politely.
     b) If they provide loan details, ask clarifying questions or propose one plan.
     c) If they refuse, re-emphasize the plan once, then if still refused, offer a second plan, and so on.
   - Stop at three refusals total; then offer escalation number and end politely.

7. **OVERALL GOAL**
   - Help the customer feel informed and comfortable with a refinancing or loan modification plan.
   - If they accept, restate the key points of that plan.
   - If they refuse all plans, provide +1 (800) 123-4567 and politely end the conversation.


Remember:
- Only offer one plan at a time.
- Do not mention or hint at multiple plans in the same response.
- Follow the detailed negotiation guidelines as provided.
"""


messages = [{"role": "system", "content": system_prompt}]

print("AI Negotiator is ready! Type 'exit' or 'quit' to end.\n")


response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    messages=messages
)
ai_reply = response.choices[0].message.content
validated_reply = validate_response(ai_reply)
print(f"AI Negotiator: {validated_reply}\n")
messages.append({"role": "assistant", "content": validated_reply})

# ai_reply = response.choices[0].message.content
# print(f"AI Negotiator: {ai_reply}\n")
# messages.append({"role": "assistant", "content": ai_reply})


user_input = input("Customer: ")
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

plans = get_plans()
messages.append({
    "role": "system", 
    "content": "Available negotiation plans: " + json.dumps(plans)
})


while True:
    user_input = input("\nCustomer: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the conversation. Bye, have a nice day!")
        break

    messages.append({"role": "user", "content": user_input})

    # Input validation for PII and jailbreak attempts
    if check_pii(user_input):
        print("Warning: PII detected in input.")
        continue
    if check_jailbreak(user_input):
        print("Warning: Jailbreak attempt detected in input.")
        continue
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=messages
    )
    ai_reply = response.choices[0].message.content
    # print(f"AI Negotiator: {ai_reply}\n")
    # messages.append({"role": "assistant", "content": ai_reply})

    # Output validation for hallucination and toxicity
    if check_toxic_language(ai_reply):
        print("Warning: Toxic language detected in AI response.")
        continue
    if check_hallucination(ai_reply):
        print("Warning: Possible hallucination detected in AI response.")
        continue

    validated_reply = validate_response(ai_reply)
    print(f"AI Negotiator: {validated_reply}\n")
    messages.append({"role": "assistant", "content": validated_reply})



    # --- Integrate calculation functions based on plan suggestion ---
    # Refinance Step Down
    if "Refinance Step Down" in ai_reply and customer:
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

    # Refinance Step Up
    elif "Refinance Step Up" in ai_reply and customer:
        try:
            increase_percent = float(input("Enter increase percentage for Refinance Step Up: "))
        except ValueError:
            increase_percent = 10  # default value if input fails
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        calc_result = refinance_step_up(loan_amount, interest_rate, loan_term, increase_percent)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    # Refinance Step Same
    elif "Refinance Step Same" in ai_reply and customer:
        loan_details = customer.get("loan_details", {})
        loan_amount = loan_details.get("loan_amount", 0)
        interest_rate = loan_details.get("interest_rate", 0)
        loan_term = loan_details.get("loan_term", 0)
        remaining_balance = loan_details.get("remaining_balance", 0)
        calc_result = refinance_same(loan_amount, interest_rate, loan_term, remaining_balance)
        print("Calculated negotiation details:", calc_result)
        messages.append({"role": "system", "content": "Negotiation calculation: " + json.dumps(calc_result)})

    # Extended Payment Plan
    elif "Extended Payment Plan" in ai_reply and customer:
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

    # Settlement Plan with Waive-Off
    elif "Settlement Plan" in ai_reply and customer:
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
        # Optionally, retrieve original fee and interest if available in the customer profile.
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
