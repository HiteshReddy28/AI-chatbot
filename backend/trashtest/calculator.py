# Repurposed Plan Calculator Tool Functions

def calculate_refinance_step_same(loan_amount, interest_rate, term):
    return {
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "term": term,
        "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, term)
    }

def calculate_refinance_step_down(loan_amount, interest_rate, term, reduction_percent):
    reduced_amount = loan_amount * (1 - reduction_percent / 100)
    return {
        "loan_amount": reduced_amount,
        "interest_rate": interest_rate,
        "term": term,
        "monthly_payment": calculate_monthly_payment(reduced_amount, interest_rate, term)
    }

def calculate_refinance_step_up(loan_amount, interest_rate, term, increase_percent):
    increased_amount = loan_amount * (1 + increase_percent / 100)
    return {
        "loan_amount": increased_amount,
        "interest_rate": interest_rate,
        "term": term,
        "monthly_payment": calculate_monthly_payment(increased_amount, interest_rate, term)
    }

def calculate_extended_payment_plan(loan_amount, interest_rate, new_term):
    return {
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "term": new_term,
        "monthly_payment": calculate_monthly_payment(loan_amount, interest_rate, new_term)
    }

def calculate_settlement_plan(loan_amount, fee_waiver=0, interest_waiver=0, principal_waiver=0):
    waived_fees = loan_amount * (fee_waiver / 100)
    waived_interest = loan_amount * (interest_waiver / 100)
    waived_principal = loan_amount * (principal_waiver / 100)
    final_amount = loan_amount - (waived_fees + waived_interest + waived_principal)
    return {
        "original_loan": loan_amount,
        "fee_waived": waived_fees,
        "interest_waived": waived_interest,
        "principal_waived": waived_principal,
        "settlement_amount": max(final_amount, 0)
    }

def calculate_monthly_payment(loan_amount, annual_rate, term_months):
    if annual_rate == 0 or term_months == 0:
        return loan_amount / term_months if term_months != 0 else 0
    monthly_rate = annual_rate / 12
    numerator = monthly_rate * (1 + monthly_rate)**term_months
    denominator = (1 + monthly_rate)**term_months - 1
    return round(loan_amount * numerator / denominator, 2)