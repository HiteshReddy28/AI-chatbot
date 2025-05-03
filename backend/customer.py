import json
def get_client_details(id:int):
    customer_details = [
    {
  "customer_id": "CUST123456",
  "first_name": "John",
  "last_name": "Doe",
  "email": "ac244@njit.edu",
  "phone": "+1234567890",
  "date_of_birth": "1985-06-15",
  "ssn": "123-45-6789",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip": "12345",
    "country": "USA"
  },
  "employment_details": {
    "employer_name": "ABC Corp",
    "job_title": "Software Engineer",
    "annual_income": 85000,
    "employment_status": "Full-Time",
    "years_employed": 5
  },
  "loan_details": {
    "loan_id": "LN987654",
    "loan_type": "Personal Loan",
    "loan_purpose": "Medical Expenses",
    "principal": 10000.0,
    "remaining_balance": 7500.0,
    "interest_rate": 0.05,
    "loan_term_months": 60,
    "start_date": "2022-01-01",
    "end_date": "2027-01-01",
    "monthly_payment": 188.71,
    "dues": 188.71,
    "late_payments": 0,
    "late_fee_per_payment": 0.0,
    "total_late_fees": 0.0,
    "prepayment_penalty": True,
    "collateral_required": False,
    "payment_status": "Active",
    "last_payment_date": "2025-04-15",
    "next_payment_due": "2025-05-15",
    "payment_method": "Auto Debit",
    "payment_history": [
      {"date": "2024-01-15", "amount": 188.71, "status": "Paid"},
      {"date": "2023-12-15", "amount": 188.71, "status": "Paid"},
      {"date": "2023-11-15", "amount": 188.71, "status": "Paid"}
    ],
    "next_steps": "Customer is enrolled in auto-debit. Monitor next payment on due date.",
    "account_flag": "Good Standing"
  },
  "account_details": {
    "account_id": "ACC112233",
    "account_type": "Savings",
    "account_balance": 5000.0,
    "account_status": "Active",
    "opened_date": "2018-05-10"
  },
  "credit_score": 720,
  "customer_since": "2015-03-22"
},
    {
    "customer_id": "CUST234567",
    "first_name": "Johnny",
    "last_name": "Cins",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1985-06-15",
    "ssn": "123-45-6789",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zip": "12345",
        "country": "USA"
    },
    "employment_details": {
        "employer_name": "Unemployed",
        "job_title": "N/A",
        "annual_income": 0,
        "employment_status": "Unemployed",
        "years_employed": 0
    },
    "loan_details": [
        {
  "loan_id": "LN987654",
  "loan_type": "Personal Loan",
  "Principal": 10000,
  "loan_term": 60,
  "interest_rate": 0.05,
  "start_date": "2022-01-01",
  "end_date": "2027-01-01",
  "monthly_payment": 188.71,
  "remaining_balance": 9500,
  "dues": 1709.68,
  "dues_breakdown": {
    "unpaid_installments": 1509.68,
    "late_fees": 200.00
  },
  "payment_status": "Delinquent",
  "late_payments": 8,
  "late_fee_per_payment": 25,
  "missed_payment_dates": [
    "2023-07-01",
    "2023-08-01",
    "2023-09-01",
    "2023-10-01",
    "2023-11-01",
    "2023-12-01",
    "2024-01-01",
    "2024-02-01"
  ],
  "next_payment_due": "2024-03-01",
  "loan_purpose": "Medical Expenses",
  "prepayment_penalty": True,
  "collateral_required": False
}

    ],
    "account_details": {
        "account_id": "ACC112233",
        "account_type": "Savings",
        "account_balance": 2,
        "account_status": "Dormant",
        "opened_date": "2018-05-10"
    },
    "credit_score": 410,
    "customer_since": "2015-03-22",
    "last_payment_date": "2023-11-01",
    "next_payment_due": "2023-12-01",
    "payment_method": "None"
},
]
    return customer_details[id]