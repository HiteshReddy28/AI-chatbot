from typing import Optional
def calculate_monthly_payment(loan_amount: float, interest_rate: float, loan_term: int) -> float:

    monthly_rate = interest_rate / 12
    if monthly_rate == 0:
        return round(loan_amount / loan_term, 2)

    payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -loan_term)
    return round(payment, 2)

# def refinance_same(Principal: float, interest_rate: float, loan_term: int, remaining_balance: float, due: float) -> dict:
#     loan_amount = Principal
#     monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
#     refunded_amount = round(loan_amount - remaining_balance- due, 2)
#     return {
#         "type": "Refinance Step Same",
#         "new_loan_amount": loan_amount,
#         "loan_term": loan_term,
#         "interest_rate": interest_rate,
#         "monthly_payment": monthly_payment,
#         "in_hand_cash": refunded_amount,
#         "description": "Same terms (interest rate, tenure etc...) and same loan amount. The difference between original loan amount and remaining balance is refunded to help the customer ."
#     }


def refinance_same(Principal, interest_rate, loan_term, remaining_balance, due) -> dict:
    loan_amount = float(Principal)
    interest_rate = float(interest_rate)
    loan_term = int(loan_term)
    remaining_balance = float(remaining_balance)
    due = float(due)
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    refunded_amount = round(loan_amount - remaining_balance- due, 2)
    return {
        "type": "Refinance Step Same",
        "new_loan_amount": loan_amount,
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": monthly_payment,
        "in_hand_cash": refunded_amount,
        "description": "Same terms (interest rate, tenure etc...) and same loan amount. The difference between original loan amount and remaining balance is refunded to help the customer ."
    }


def refinance_step_down(Principal, interest_rate, loan_term, reduce_percent,remaining_balance, due) -> dict:
    loan_amount = float(Principal)
    interest_rate = float(interest_rate)
    loan_term = int(loan_term)
    remaining_balance = float(remaining_balance)
    reduce_percent = float(reduce_percent)
    due = float(due)
    adjusted_loan = loan_amount * (1 - reduce_percent / 100)
    in_hand = adjusted_loan - remaining_balance - due
    new_monthly_payment = calculate_monthly_payment(adjusted_loan, interest_rate, loan_term)
    old_monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
    return {
        "type": f"Refinance Step Down ({reduce_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": new_monthly_payment,
        "in_hand_cash": in_hand,
        "Difference in monthly payments": old_monthly_payment - new_monthly_payment,
        "description": f"Loan reduced by {reduce_percent}%"
    }

# def refinance_step_down(Principal: float, interest_rate: float, loan_term: int, reduce_percent: float,remaining_balance: float, due: float) -> dict:
#     loan_amount = Principal
#     adjusted_loan = loan_amount * (1 - reduce_percent / 100)
#     in_hand = adjusted_loan - remaining_balance - due
#     new_monthly_payment = calculate_monthly_payment(adjusted_loan, interest_rate, loan_term)
#     old_monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)
#     return {
#         "type": f"Refinance Step Down ({reduce_percent}%)",
#         "new_loan_amount": round(adjusted_loan, 2),
#         "loan_term": loan_term,
#         "interest_rate": interest_rate,
#         "monthly_payment": new_monthly_payment,
#         "in_hand_cash": in_hand,
#         "Difference in monthly payments": old_monthly_payment - new_monthly_payment,
#         "description": f"Loan reduced by {reduce_percent}%"
#     }


def refinance_step_up(Principal, interest_rate, loan_term, increase_percent,remaining_balance, due) -> dict:

    loan_amount = float(Principal)
    interest_rate = float(interest_rate)
    loan_term = int(loan_term)
    remaining_balance = float(remaining_balance)
    due = float(due)
    increase_percent = float(increase_percent)
    adjusted_loan = loan_amount * (1 + increase_percent / 100)
    in_hand = adjusted_loan - remaining_balance - due
    return {
        "type": f"Refinance Step Up ({increase_percent}%)",
        "new_loan_amount": round(adjusted_loan, 2),
        "loan_term": loan_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
        "in_hand_cash": in_hand,
        "description": f"Loan increased by {increase_percent}%"
    }


# def refinance_step_up(Principal: float, interest_rate: float, loan_term: int, increase_percent: float,remaining_balance: float, due: float) -> dict:
#     loan_amount = Principal
#     adjusted_loan = loan_amount * (1 + increase_percent / 100)
#     in_hand = adjusted_loan - remaining_balance - due
#     return {
#         "type": f"Refinance Step Up ({increase_percent}%)",
#         "new_loan_amount": round(adjusted_loan, 2),
#         "loan_term": loan_term,
#         "interest_rate": interest_rate,
#         "monthly_payment": calculate_monthly_payment(adjusted_loan, interest_rate, loan_term),
#         "in_hand_cash": in_hand,
#         "description": f"Loan increased by {increase_percent}%"
#     }


def extended_payment_plan(Principal, interest_rate, original_term, extension_cycles) -> dict:
    loan_amount = float(Principal)
    interest_rate = float(interest_rate)
    original_term = int(original_term)
    extension_cycles = int(extension_cycles)

    new_term = original_term + extension_cycles
    return {
        "type": f"Extended Payment Plan (+{extension_cycles} months)",
        "new_loan_amount": loan_amount,
        "loan_term": new_term,
        "interest_rate": interest_rate,
        "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, new_term),
        "description": f"Extended by {extension_cycles} months"
    }


# def extended_payment_plan(Principal: float, interest_rate: float, original_term: int, extension_cycles: int) -> dict:
#     loan_amount = Principal
#     new_term = original_term + extension_cycles
#     return {
#         "type": f"Extended Payment Plan (+{extension_cycles} months)",
#         "new_loan_amount": loan_amount,
#         "loan_term": new_term,
#         "interest_rate": interest_rate,
#         "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, new_term),
#         "description": f"Extended by {extension_cycles} months"
#     }

def settlement_plan_with_waivers(
    loan_balance: float,
    fee_waiver_percent: float = 0,
    interest_waiver_percent: float = 0,
    principal_waiver_percent: float = 0,
    original_fee: Optional[float] = 0,
    original_interest: Optional[float] = 0
) -> dict:
    
    waived_fee = (original_fee or 0) * fee_waiver_percent / 100
    waived_interest = (original_interest or 0) * interest_waiver_percent / 100
    waived_principal = loan_balance * principal_waiver_percent / 100

    settlement_amount = (
        (original_fee or 0) - waived_fee +
        (original_interest or 0) - waived_interest +
        loan_balance - waived_principal
    )

    return {
        "type": "Settlement Plan with Waive-Off",
        "waived_fee": round(waived_fee, 2),
        "waived_interest": round(waived_interest, 2),
        "waived_principal": round(waived_principal, 2),
        "total_settlement": round(settlement_amount, 2),
        "description": "Calculated based on requested waiver percentages."
    }

