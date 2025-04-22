def get_customer_details(email_id = None):
    customer_details = [
    {
        "customer_id": "CUST123456",
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
        "loan_details": [
            {
                "loan_id": "LN987654",
                "loan_type": "Personal Loan",
                "Principle": 10000,
                "loan_term": 60,
                "interest_rate": 0.05,
                "start_date": "2022-01-01",
                "end_date": "2027-01-01",
                "monthly_payment": 188.71,
                "remaining_balance": 7500,
                "dues": 188.71,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Medical Expenses",
                "prepayment_penalty": True,
                "collateral_required": False
            }
        ],
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
  "customer_id": "CUST234567",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "phone": "+1987654321",
  "date_of_birth": "1990-07-20",
  "ssn": "234-56-7890",
  "address": {
    "street": "456 Elm Street",
    "city": "Metropolis",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  },
  "employment_details": {
    "employer_name": "XYZ Inc",
    "job_title": "Financial Analyst",
    "annual_income": 70000,
    "employment_status": "Full-Time",
    "years_employed": 3
  },
  "loan_details": [
    {
      "loan_id": "LN123456",
      "loan_type": "Personal Loan",
      "Principle": 15000,
      "loan_term": 48,
      "interest_rate": 0.07,
      "start_date": "2021-06-01",
      "end_date": "2025-06-01",
      "monthly_payment": 358.24,
      "remaining_balance": 9200,
      "dues": 358.24,
      "payment_status": "Active",
      "late_payments": 2,
      "loan_purpose": "Home Renovation",
      "prepayment_penalty": False,
      "collateral_required": False
    }
  ],
  "account_details": {
    "account_id": "ACC445566",
    "account_type": "Checking",
    "account_balance": 3200,
    "account_status": "Active",
    "opened_date": "2019-09-15"
  },
  "credit_score": 690,
  "customer_since": "2017-08-30",
  "last_payment_date": "2025-03-01",
  "next_payment_due": "2025-04-01",
  "payment_method": "Manual Payment"
},
    {
        "customer_id": "CUST654321",
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
        "loan_details": [
            {
                "loan_id": "LN123789",
                "loan_type": "Car Loan",
                "Principle": 25000,
                "loan_term": 48,
                "interest_rate": 0.045,
                "start_date": "2023-03-01",
                "end_date": "2027-03-01",
                "monthly_payment": 566.14,
                "remaining_balance": 24000,
                "dues": 666.14,
                "payment_status": "Active",
                "late_payments": 1,
                "loan_purpose": "Vehicle Purchase",
                "prepayment_penalty": False,
                "collateral_required": True
            },
            {
                "loan_id": "LN876543",
                "loan_type": "Credit Card Debt",
                "Principle": 5000,
                "loan_term": 24,
                "interest_rate": 0.15,
                "start_date": "2022-06-01",
                "end_date": "2024-06-01",
                "monthly_payment": 250,
                "remaining_balance": 2000,
                "dues": 300,
                "payment_status": "Delinquent",
                "late_payments": 3,
                "loan_purpose": "Retail Purchases",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
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
        "customer_id": "CUST112233",
        "first_name": "Alice",
        "last_name": "Brown",
        "email": "alice.brown@example.com",
        "phone": "+1122334455",
        "date_of_birth": "1992-03-12",
        "ssn": "555-66-7788",
        "address": {
            "street": "789 Maple St",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "ACME Co",
            "job_title": "Data Analyst",
            "annual_income": 70000,
            "employment_status": "Part-Time",
            "years_employed": 2
        },
        "loan_details": [
            {
                "loan_id": "LN332211",
                "loan_type": "Student Loan",
                "Principle": 15000,
                "loan_term": 120,
                "interest_rate": 0.035,
                "start_date": "2020-09-01",
                "end_date": "2030-09-01",
                "monthly_payment": 147.89,
                "remaining_balance": 12500,
                "dues": 147.89,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Higher Education",
                "prepayment_penalty": True,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC998877",
            "account_type": "Savings",
            "account_balance": 1500,
            "account_status": "Active",
            "opened_date": "2019-02-01"
        },
        "credit_score": 680,
        "customer_since": "2018-06-15",
        "last_payment_date": "2024-02-10",
        "next_payment_due": "2024-03-10",
        "payment_method": "Auto Debit"
    },
     {
        "customer_id": "CUST445566",
        "first_name": "Robert",
        "last_name": "Johnson",
        "email": "robert.johnson@example.com",
        "phone": "+1445566778",
        "date_of_birth": "1980-11-02",
        "ssn": "444-55-6666",
        "address": {
            "street": "234 Oak Lane",
            "city": "Chicago",
            "state": "IL",
            "zip": "60601",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "Global Solutions",
            "job_title": "Project Manager",
            "annual_income": 105000,
            "employment_status": "Full-Time",
            "years_employed": 7
        },
        "loan_details": [
            {
                "loan_id": "LN556677",
                "loan_type": "Mortgage",
                "Principle": 300000,
                "loan_term": 360,
                "interest_rate": 0.03,
                "start_date": "2015-07-01",
                "end_date": "2045-07-01",
                "monthly_payment": 1264.14,
                "remaining_balance": 250000,
                "dues": 1264.14,
                "payment_status": "Active",
                "late_payments": 2,
                "loan_purpose": "Home Purchase",
                "prepayment_penalty": True,
                "collateral_required": True
            },
            {
                "loan_id": "LN667788",
                "loan_type": "Personal Loan",
                "Principle": 20000,
                "loan_term": 60,
                "interest_rate": 0.07,
                "start_date": "2020-10-01",
                "end_date": "2025-10-01",
                "monthly_payment": 396.02,
                "remaining_balance": 8000,
                "dues": 396.02,
                "payment_status": "Active",
                "late_payments": 0,
                "loan_purpose": "Debt Consolidation",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC223344",
            "account_type": "Savings",
            "account_balance": 15000,
            "account_status": "Active",
            "opened_date": "2010-04-15"
        },
        "credit_score": 750,
        "customer_since": "2009-08-01",
        "last_payment_date": "2024-03-01",
        "next_payment_due": "2024-04-01",
        "payment_method": "Auto Debit"
    },
    {
        "customer_id": "CUST778899",
        "first_name": "Emily",
        "last_name": "Davis",
        "email": "emily.davis@example.com",
        "phone": "+1778899000",
        "date_of_birth": "1995-02-14",
        "ssn": "777-88-9999",
        "address": {
            "street": "567 Pine St",
            "city": "Seattle",
            "state": "WA",
            "zip": "98101",
            "country": "USA"
        },
        "employment_details": {
            "employer_name": "Tech Innovators",
            "job_title": "UX Designer",
            "annual_income": 85000,
            "employment_status": "Full-Time",
            "years_employed": 2
        },
        "loan_details": [
            {
                "loan_id": "LN778899",
                "loan_type": "Student Loan",
                "Principle": 50000,
                "loan_term": 120,
                "interest_rate": 0.04,
                "start_date": "2018-09-01",
                "end_date": "2028-09-01",
                "monthly_payment": 506.23,
                "remaining_balance": 30000,
                "dues": 506.23,
                "payment_status": "Active",
                "late_payments": 1,
                "loan_purpose": "Higher Education",
                "prepayment_penalty": False,
                "collateral_required": False
            },
            {
                "loan_id": "LN889900",
                "loan_type": "Credit Card Debt",
                "Principle": 8000,
                "loan_term": 24,
                "interest_rate": 0.18,
                "start_date": "2022-01-01",
                "end_date": "2024-01-01",
                "monthly_payment": 400,
                "remaining_balance": 2000,
                "dues": 600,
                "payment_status": "Delinquent",
                "late_payments": 3,
                "loan_purpose": "Retail Purchases",
                "prepayment_penalty": False,
                "collateral_required": False
            }
        ],
        "account_details": {
            "account_id": "ACC334455",
            "account_type": "Checking",
            "account_balance": 2500,
            "account_status": "Active",
            "opened_date": "2017-06-20"
        },
        "credit_score": 690,
        "customer_since": "2016-11-12",
        "last_payment_date": "2024-02-25",
        "next_payment_due": "2024-03-25",
        "payment_method": "Manual Payment"
    }
]
    # if email_id:
    #     filtered_customers = [customer for customer in customer_details if customer["email"] == email_id]
    #     return json.dumps(filtered_customers, indent=4) if filtered_customers else json.dumps({"message": "No customer found with this email."}, indent=4)
    
    return customer_details[0]
