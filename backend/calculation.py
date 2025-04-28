from typing import Optional
from jpt import send_violation_to_ai


def calculate_monthly_payment(loan_amount: float, interest_rate: float, loan_term: int) -> float:

    monthly_rate = interest_rate / 12
    if monthly_rate == 0:
        return round(loan_amount / loan_term, 2)

    payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -loan_term)
    return round(payment, 2)


def refinance_same(loan_amount: float, interest_rate: float, loan_term: int, remaining_balance: float) -> dict:
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    refunded_amount = round(loan_amount - remaining_balance, 2)

    return {
        "type": "Refinance Step Same",
        "new_loan_amount": loan_amount,
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": monthly_payment,
        "refunded_amount": refunded_amount,
        "description": "A new loan is issued with Same terms (interest rate, tenure etc...) and same loan amount. And the old loan is paid off and the difference amount of original loan amount - remaining amount will be given as cash in hand to the customer to help them."
    }



def refinance_step_down(loan_amount: float, interest_rate: float, loan_term: int, reduce_percent: float) -> dict:
   
    adjusted_loan = loan_amount * (1 - reduce_percent / 100)

    if (reduce_percent > 50):
        send_violation_to_ai(function_name="refinance_step_down", message="Loan reduction cannot exceed 50%. Maximum allowed is 50%.", violation_type="BusinessRule")

    

    return {
        "type": f"Refinance Step Down ({reduce_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "description": f"Loan reduced by {reduce_percent}% in the interval of 10% upto 50% max"
    }


def refinance_step_up(loan_amount: float, interest_rate: float, loan_term: int, increase_percent: float) -> dict:
   
    adjusted_loan = loan_amount * (1 + increase_percent / 100)
    return {
        "type": f"Refinance Step Up ({increase_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "description": f"Loan increased by {increase_percent}%"
    }


def extended_payment_plan(loan_amount: float, interest_rate: float, original_term: int, extension_cycles: int) -> dict:
   
    new_term = original_term + extension_cycles
    return {
        "type": f"Extended Payment Plan (+{extension_cycles} months)",
        "new_loan_amount": loan_amount,
        "loan_term": new_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, new_term),
        "description": f"Extended by {extension_cycles} months"
    }


def settlement_plan_with_waivers(
    loan_balance: float,
    loan_amount: int,
    interest_rate: float,
    Term: int,
    monthly_payment: float,
    fee_waiver_percent: float = 0,
    interest_waiver_percent: float = 0,
    principal_waiver_percent: float = 0,
    dues: Optional[float] = 0,
    original_interest: Optional[float] = 0,
    
) -> dict:
    
    waived_fee = (dues or 0) * fee_waiver_percent / 100
    waived_interest = (original_interest or 0) * interest_waiver_percent / 100
    waived_principal = loan_balance * principal_waiver_percent / 100

    settlement_amount = (
        loan_balance - waived_principal+
        (dues or 0) - waived_fee +
        (original_interest or 0) - waived_interest 
        
    )

    return {
        "type": "Settlement Plan with Waive-Off",
        "total_settlement": round(settlement_amount, 2),
        "Loan_amount": loan_amount,
        "Interest_rate": interest_rate,
        "Term": Term,
        "waived_fee": round(waived_fee+waived_principal+waived_interest, 2),
        "Updated dues": round(dues - waived_fee,2),
        "monthly_balance": monthly_payment,
        "description": "Calculated based on requested waiver percentages."
    }
# print(settlement_plan_with_waivers(9500,10000,0.05,60,188.71,100,0,5,566.13,0.05))