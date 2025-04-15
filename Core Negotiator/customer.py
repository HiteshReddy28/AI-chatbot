import json

def get_customer_details():
    
    customers = [
        {
            "customer_id": "CUST001",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
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
                "loan_amount": 10000,
                "loan_term": 60,
                "interest_rate": 0.05,
                "start_date": "2022-01-01",
                "end_date": "2027-01-01",
                "monthly_payment": 188.71,
                "remaining_balance": 7500,
                "payment_status": "Active",
                "late_payments": 0
            },
            "account_details": {
                "account_id": "ACC112233",
                "account_type": "Savings",
                "account_balance": 5000,
                "account_status": "Active",
                "opened_date": "2018-05-10"
            },
            "credit_score": 720,
            "customer_since": "2015-03-22",
            "last_payment_date": "2024-02-15",
            "next_payment_due": "2024-03-15",
            "payment_method": "Auto Debit"
        },
        {
            "customer_id": "CUST002",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "+1987654321",
            "date_of_birth": "1990-09-25",
            "ssn": "987-65-4321",
            "address": {
                "street": "456 Elm St",
                "city": "Springfield",
                "state": "TX",
                "zip": "67890",
                "country": "USA"
            },
            "employment_details": {
                "employer_name": "XYZ Inc",
                "job_title": "Marketing Manager",
                "annual_income": 95000,
                "employment_status": "Full-Time",
                "years_employed": 3
            },
            "loan_details": {
                "loan_id": "LN123789",
                "loan_type": "Car Loan",
                "loan_amount": 25000,
                "loan_term": 48,
                "interest_rate": 0.045,
                "start_date": "2023-03-01",
                "end_date": "2027-03-01",
                "monthly_payment": 566.14,
                "remaining_balance": 24000,
                "payment_status": "Active",
                "late_payments": 1
            },
            "account_details": {
                "account_id": "ACC445566",
                "account_type": "Checking",
                "account_balance": 3000,
                "account_status": "Active",
                "opened_date": "2017-09-15"
            },
            "credit_score": 710,
            "customer_since": "2016-08-10",
            "last_payment_date": "2024-02-20",
            "next_payment_due": "2024-03-20",
            "payment_method": "Manual Payment"
        },
        {
            "customer_id": "CUST003",
            "first_name": "Robert",
            "last_name": "Johnson",
            "email": "robert.johnson@example.com",
            "phone": "+1122334455",
            "date_of_birth": "1978-12-05",
            "ssn": "456-78-9012",
            "address": {
                "street": "789 Oak St",
                "city": "Metro City",
                "state": "NY",
                "zip": "54321",
                "country": "USA"
            },
            "employment_details": {
                "employer_name": "Tech Solutions",
                "job_title": "Data Scientist",
                "annual_income": 120000,
                "employment_status": "Full-Time",
                "years_employed": 8
            },
            "loan_details": {
                "loan_id": "LN456123",
                "loan_type": "Mortgage",
                "loan_amount": 300000,
                "loan_term": 360,
                "interest_rate": 0.04,
                "start_date": "2015-06-01",
                "end_date": "2045-06-01",
                "monthly_payment": 1432.25,
                "remaining_balance": 250000,
                "payment_status": "Active",
                "late_payments": 2
            },
            "account_details": {
                "account_id": "ACC778899",
                "account_type": "Joint",
                "account_balance": 15000,
                "account_status": "Active",
                "opened_date": "2010-01-25"
            },
            "credit_score": 740,
            "customer_since": "2009-12-01",
            "last_payment_date": "2024-02-10",
            "next_payment_due": "2024-03-10",
            "payment_method": "Auto Debit"
        },
        {
            "customer_id": "CUST004",
            "first_name": "Emily",
            "last_name": "Davis",
            "email": "emily.davis@example.com",
            "phone": "+1098765432",
            "date_of_birth": "1995-02-18",
            "ssn": "234-56-7890",
            "address": {
                "street": "321 Pine St",
                "city": "Lakeside",
                "state": "FL",
                "zip": "98765",
                "country": "USA"
            },
            "employment_details": {
                "employer_name": "HealthPlus",
                "job_title": "Nurse Practitioner",
                "annual_income": 75000,
                "employment_status": "Part-Time",
                "years_employed": 2
            },
            "loan_details": {
                "loan_id": "LN789012",
                "loan_type": "Student Loan",
                "loan_amount": 50000,
                "loan_term": 120,
                "interest_rate": 0.035,
                "start_date": "2020-09-01",
                "end_date": "2030-09-01",
                "monthly_payment": 495.40,
                "remaining_balance": 42000,
                "payment_status": "Active",
                "late_payments": 0
            },
            "account_details": {
                "account_id": "ACC990011",
                "account_type": "Savings",
                "account_balance": 8000,
                "account_status": "Active",
                "opened_date": "2021-02-18"
            },
            "credit_score": 690,
            "customer_since": "2020-01-10",
            "last_payment_date": "2024-02-25",
            "next_payment_due": "2024-03-25",
            "payment_method": "Auto Debit"
        }
    ]

    
    customer_id = input("Please enter the customer ID: ").strip()

    
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    
    return None
