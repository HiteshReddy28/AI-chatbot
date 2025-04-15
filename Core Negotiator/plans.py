def get_plans():
    repayment_plans = {
        "Plan 1 - Refinance": {
            "Description": (
                "Refinancing involves replacing an existing loan with a new one, often with better "
                "terms for the borrower. It helps reduce monthly payments, extend tenure, or lower "
                "interest rates, making repayment easier."
            ),
            "KeyFeatures": [
                "New Loan Issued: The old loan is paid off, and a new loan is created with different terms.",
                "Lower Interest Rate: If the borrower qualifies, the interest rate may be reduced.",
                "Extended Tenure: The loan term may be increased to lower EMI payments.",
                "Better Affordability: Helps delinquent borrowers by restructuring their debt into manageable payments."
            ],
            "EligibilityCriteria": [
                "Borrower must have a stable income source.",
                "Improved creditworthiness may be required.",
                "May require a good repayment history before delinquency."
            ],
            "Pros": [
                "Lower monthly payments, making repayment easier.",
                "Helps maintain a positive credit score if payments are made on time."
            ],
            "Cons": [
                "May result in a higher total interest paid due to extended tenure.",
                "Some lenders charge refinancing fees or prepayment penalties."
            ],
            "Options": {
                "Option 1": {
                    "Type": "Refinance Step Same",
                    "Description": "Same terms (interest rate, tenure, etc.) and same loan amount.",
                    "NegotiationParameters": "No Negotiation Parameters."
                },
                "Option 2": {
                    "Type": "Refinance Step Down",
                    "Description": "Same terms (interest rate, tenure, etc.) and decrease loan amount by percentage.",
                    "NegotiationParameters": "Negotiate on loan amount decrease % up to 50% in steps of 10%."
                },
                "Option 3": {
                    "Type": "Refinance Step Up",
                    "Description": "Same terms (interest rate, tenure, etc.) and increase loan amount by percentage.",
                    "NegotiationParameters": "Negotiate on loan amount increase % up to 50% in steps of 10%."
                }
            }
        },
        "Plan 2 - Extended Payment Plan (EPP)": {
            "Description": (
                "An Extended Payment Plan (EPP) allows borrowers to restructure their existing loan by "
                "extending the repayment timeline, reducing the monthly installment without issuing a new loan."
            ),
            "KeyFeatures": [
                "Existing Loan Restructured: No new loan is created, but repayment terms are adjusted.",
                "Reduced Monthly Payment: Spread over a longer period.",
                "No Additional Interest Rate Change: The existing rate may remain the same, or a small restructuring fee might apply.",
                "More Time to Repay: Helps borrowers avoid default and negative credit reporting."
            ],
            "EligibilityCriteria": [
                "Typically offered to borrowers who are late on payments but not severely delinquent.",
                "Borrowers with temporary financial hardships (e.g., job loss, medical emergency).",
                "Loan should not be in deep delinquency (usually <90 DPD).",
                "Lender may require proof of income reduction or financial hardship.",
                "Some lenders may charge a restructuring fee (1-3% of outstanding balance).",
                "Some lenders require a minimum number of on-time payments before allowing an EPP."
            ],
            "Pros": [
                "Immediate relief from high monthly payments.",
                "No need to take a new loan or affect the credit score negatively.",
                "Helps avoid loan default and collections."
            ],
            "Cons": [
                "Total interest outflow increases due to the longer repayment period.",
                "Lender might charge a restructuring fee or increase the interest rate slightly."
            ],
            "Options": {
                "Option 1": {
                    "Type": "Extended Payment Plan up to 12 cycles",
                    "Description": "Extend by 3/6/9/12 cycles for loan tenures <= 12 cycles.",
                    "NegotiationParameters": "Negotiate on number of cycles to extend."
                },
                "Option 2": {
                    "Type": "Extended Payment Plan up to 24 cycles at 6 cycle steps",
                    "Description": "Extend by 6/12/18/24 cycles for loan tenures > 12 cycles.",
                    "NegotiationParameters": "Negotiate on number of cycles to extend."
                },
                "Option 3": {
                    "Type": "Extended Payment Plan up to 24 cycles at 3 cycle steps",
                    "Description": "Extend by 3/6/9/12/15/18/21/24 cycles for loan tenures > 12 cycles.",
                    "NegotiationParameters": "Negotiate on number of cycles to extend."
                }
            }
        },
        "Plan 3 - Settlement Plans with Waive-off": {
            "Description": (
                "A Settlement Plan with Waive-off allows a borrower to pay a reduced amount as a one-time lump sum "
                "or structured partial payments in exchange for waiving off a portion of the outstanding debt."
            ),
            "KeyFeatures": [
                "Waiver of Fees or Interest or Principal: A percentage of the outstanding loan is written off.",
                "One-Time or Installment-Based Settlement: Borrower can either pay a lump sum or in agreed-upon installments.",
                "Final Closure of Loan: Once the agreed settlement amount is paid, the loan is considered closed.",
                "Negative Credit Impact: Usually reported as 'Settled' instead of 'Paid in Full', which negatively affects credit scores."
            ],
            "EligibilityCriteria": [
                "Typically offered to borrowers in severe delinquency (e.g., 90+ days past due).",
                "Borrower must prove financial hardship (job loss, medical emergency, etc.).",
                "Requires deep negotiation with the lender."
            ],
            "Pros": [
                "Helps borrowers clear debt with reduced payment.",
                "Avoids prolonged legal action or collections."
            ],
            "Cons": [
                "Negatively impacts the credit score.",
                "Some lenders require a waiting period before offering another loan."
            ],
            "Options": {
                "Option 1": {
                    "Type": "Waive Fees up to 100% in steps of 25%",
                    "NegotiationParameters": "Negotiate on fee waiver %."
                },
                "Option 2": {
                    "Type": "Waive 100% fees, Waive up to 100% of interest in steps of 25%",
                    "NegotiationParameters": "Negotiate on interest waiver %."
                },
                "Option 3": {
                    "Type": "Waive 100% fees, Waive 100% interest, Waive up to 10/20/30/40% of principal in steps",
                    "NegotiationParameters": "Negotiate on principal waiver %."
                }
            },
            "ExampleRules": (
                "In no case should you offer more waiver than the borrower would have asked for. "
                "For example, if the borrower rejects a 25% fee waiver and asks for 30%, accept 30% even though it is "
                "less than the next step of 50%. If the borrower asks for any other offers after rejecting the 25% waiver, "
                "then offer 50% which is the next step."
            )
        }
    }
    return repayment_plans