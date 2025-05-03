import json
'''


'''
def get_plans(customer_id:str):
    repayment_plans = {
          
 "CUST123456":{
      "plans": [  
          {
          "plan_id": 1,
          "name": "Refinance Step Same",
          "priority": 1,
          "description": "Customer continues at the same loan amount, same interest rate, and same loan term — but benefits from a revised structure with cash in hand to get back on track with payments",
          "is_step_based": False,
          "tool_call_template": "refinance_same_step()",
          "negotiation_rules": [
            "Start by explaining that this plan keeps everything familiar — same loan, same structure — but with an optimized repayment schedule.",
            "Emphasize peace of mind: ‘No increase in debt, just smoother payments.’",
            "Use tool output to show: ‘This gives you breathing room without touching your loan balance.’",
            "Position it as the most stable option available today, ideal for maintaining control during uncertain times.",
            "Use positive framing like: ‘This is a no-change solution that helps you stay on track — no surprises, just relief.’"
          ],
          "pros": [
            "Simple, easy-to-understand structure with less emotional or financial friction.",
            "No change in principal — psychologically easier to accept.",
            "Best suited for customers who prefer stability and do not want to restructure their loan."
          ],
          "cons": [
            "Provides minimal relief compared to step-up or term extension plans.",
            "Not ideal for customers who need significant cash or debt reduction."
          ],
          "Tool_results": {
              "type": "Refinance Step Same",
              "new_loan_amount": 10000.0,
              "loan_term": 60,
              "interest_rate": "5%",
              "monthly_payment": 188.71,
              "in_hand_cash": 2311.29,},
      },
      
                 {
  "plan_id": 2,
  "name": "Extended Payment Plan",
  "priority": 2,
  "description": "This plan helps lower your monthly payments by extending your loan term gradually—starting with just 3 months and moving up only if needed.",
  "is_step_based": True,
#   "Steps": [3, 6],
#   "Step_description": "We begin with a 3-month extension and step up to 6, 9, or 12 months only if more support is required.",
  "tool_call_template": "extended_payment_plan(months=<step>)",
  "negotiation_rules": [
    "Let’s start with a 3-month extension — this gives you less monthly payment without changing your loan too much.",
    "This option keeps your total interest impact low while helping you manage payments better.",
    # "If you’re still feeling pressure, we can explore extending a bit further — up to 6 or 9 months if needed.",
    "We move step-by-step so you’re never overwhelmed. Every stage is based on your comfort and need.",
    "These options are time-sensitive, so taking early action means better chances of approval."
  ],
  "pros": [
    "Gives quick monthly payment relief while keeping your loan structure mostly intact.",
    "Reduce customers monthly payments",
    "The changes are small and manageable — a soft landing rather than a major change.",
    "You always decide if the next step makes sense — you stay in control the whole way.",
  ],
  "cons": [
    "The initial step provides mild relief — may not be enough if your situation is urgent.",
    "We’ll need to go step-by-step to reach the full benefit, which takes a little more time.",
    "The total loan duration may increase slightly depending on how far we go.",
  ],
  "Tool_results":{"3_months_extension":{"Monthly Payment": 180.8,"loan_amount": 10000.0,
              "loan_term": 63,
              "interest_rate": "5%","Extended months": 3,"monthly_saving": 8}}
},
 {
  "plan_id": 3,
  "name": "Extended Payment Plan",
  "priority": 3,
  "description": "This plan helps lower your monthly payments by extending your loan term gradually—starting with just 3 months and moving up only if needed.",
  "is_step_based": True,
#   "Steps": [3, 6],
#   "Step_description": "We begin with a 3-month extension and step up to 6, 9, or 12 months only if more support is required.",
  "tool_call_template": "extended_payment_plan(months=<step>)",
  "negotiation_rules": [
    "Let’s start with a 3-month extension — this gives you less monthly payment without changing your loan too much.",
    "This option keeps your total interest impact low while helping you manage payments better.",
    # "If you’re still feeling pressure, we can explore extending a bit further — up to 6 or 9 months if needed.",
    "We move step-by-step so you’re never overwhelmed. Every stage is based on your comfort and need.",
    "These options are time-sensitive, so taking early action means better chances of approval."
  ],
  "pros": [
    "Gives quick monthly payment relief while keeping your loan structure mostly intact.",
    "Reduce customers monthly payments",
    "The changes are small and manageable — a soft landing rather than a major change.",
    "You always decide if the next step makes sense — you stay in control the whole way.",
  ],
  "cons": [
    "The initial step provides mild relief — may not be enough if your situation is urgent.",
    "We’ll need to go step-by-step to reach the full benefit, which takes a little more time.",
    "The total loan duration may increase slightly depending on how far we go.",
  ],
  "Tool_results":{
              "6_months_extension":{"Monthly Payment": 173.62,"loan_amount": 10000.0,
              "loan_term": 66,
              "interest_rate": 0.05,"Extended months": 6,"Monthly_saving": 15}}
},
{
  "plan_id": 4,
  "name": "Settlement Plan with Fee Waive-Off",
  "priority": 4,
  "description": "If you're going through financial distress and unable to repay the full amount, this plan helps settle your loan by gradually waiving off fees",
  "is_step_based": True,
#   "Steps": [25, 50],
#   "Step_description": "Each step increases the waiver on fees by 25%. We begin at 25% and only proceed further based on your situation and feedback.",
  "tool_call_template": "settle_with_fee_waiver(waiver_percentage=<steps>)",
  "negotiation_rules": [
      
  ],
  "pros": [
    "Allows customers to settle their loan quickly with less burden from penalties or overdue charges.",
    "Prevents further credit damage and legal risk by offering a clean exit path.",
    "Flexible — starts small and increases only if the customer truly needs more help."
  ],
  "cons": [
    "Still requires lump-sum payment or settlement of remaining balance, which might be tough in very critical cases.",
    "Fee waivers are conditional — may not suit customers expecting full forgiveness instantly.",
    "Might not be perceived positively if not explained with empathy and clarity."
  ],
  "Tool_Results": {
      "Fee_waiver_25%":{"Plan Name": "Settlement Plan with Fee Waive-Off(25%)",
"Loan Amount": 10000,
"Settlement Amount": 7641.53,
"Interest Rate": "5%",
"Term": 60,
"Monthly Payment": 188.71,
"Dues": 141.53,
"Waived fee": 47.18},
"Fee_waiver_50%":{"Plan_name":"Settlement Plan with Fee Waive-Off(50%)",
"Loan Amount": 10000,
"Settlement Amount": 7594.36,
"Interest Rate": "5%",
"Term": 60,
"Monthly Payment": 188.71,
"Dues": 94.36,
"Waived fee": 94.36,},
  }
},     
  ]
    },
    
"CUST234567":{
      "plans": [
        {
  "plan_id": 1,
  "name": "Settlement Plan with Fee Waive-Off",
  "priority": 1,
  "description": "If you're going through financial distress and unable to repay the full amount, this plan helps settle your loan by gradually waiving off fees in steps — starting from 25% and going up to 100%.",
  "is_step_based": True,
  "Steps": [50, 100],
  "Step_description": "Each step increases the waiver on fees by 25%. We begin at 25% and only proceed further based on your situation and feedback.",
  "tool_call_template": "settle_with_fee_waiver(waiver_percentage=<step>)",
  "negotiation_rules": [
    
    ],
  "pros": [
    "Allows customers to settle their loan quickly with less burden from penalties or overdue charges.",
    "Prevents further credit damage and legal risk by offering a clean exit path.",
    "Flexible — starts small and increases only if the customer truly needs more help."
  ],
  "cons": [
    "Still requires lump-sum payment or settlement of remaining balance, which might be tough in very critical cases.",
    "Fee waivers are conditional — may not suit customers expecting full forgiveness instantly.",
    "Might not be perceived positively if not explained with empathy and clarity."
  ],
  "tool_results":{"Fee_waiver_50%":{'type': 'Settlement Plan with Waive-Off', 'total_settlement': 9783.11, 'Loan_amount': 10000, 'Interest_rate': 0.05, 'Term': 60, 'waived_fee': 283.06, 'Updated dues': 283.06, 'monthly_balance': 188.71, 'description': 'Calculated based on requested waiver percentages.'},
                  "Fee_waiver_100%":{'type': 'Settlement Plan with Waive-Off', 'total_settlement': 9500.05, 'Loan_amount': 10000, 'Interest_rate': 0.05, 'Term': 60, 'waived_fee': 566.13, 'Updated dues': 0.0, 'monthly_balance': 188.71, 'description': 'Calculated based on requested waiver percentages.'}}

},
        {
  "plan_id": 2,
  "name": "Settlement Plan with Principal Waiver",
  "priority": 2,
  "description": "This plan is for customers facing extreme financial hardship. It offers partial forgiveness on the loan principal, starting at 2.5% and increasing up to 40%, to help them close the loan through a negotiated settlement.",
  "is_step_based": True,
  "Steps": [5,10],
  "Step_description": "The waiver on principal starts at 2.5%. Increase only if the customer is unable to pay, based on clear hardship signals (pchange, threshold). Do not skip steps.",
  "tool_call_template": "settle_with_principal_waiver(waiver_percentage=<step>)",
  "negotiation_rules": [
    "Start by offering a 2.5% waiver on principal using `settle_with_principal_waiver(waiver_percentage=2.5)`.",
    "Highlight that this is a rare opportunity to reduce the debt **at the principal level**, which is usually non-negotiable.",
    "Explain: 'Even a 2.5% reduction gives you relief without hurting your future borrowing potential.'",
    "Only advance to next step if customer is still unable to commit AND (`pchange == true` and `threshold == 0`).",
    "Sequence must be followed strictly: 2.5 → 5 → 10 → 20 → 30 → 40%.",
    "Avoid framing this as debt forgiveness — instead present it as a **settlement benefit** for timely closure.",
    "Always reinforce urgency: 'This support may not be available if delayed. The earlier you act, the more we can support you.'"
  ],
  "pros": [
    "Directly reduces the core debt — not just fees or interest — which makes the offer very powerful.",
    "Makes settlement affordable for users who have limited financial recovery options.",
    "Allows stepwise trust-building and flexibility for extreme hardship cases."
  ],
  "cons": [
    "Customer may expect larger waivers prematurely — needs careful framing to avoid entitlement.",
    "More steps in smaller percentages may increase negotiation time.",
    "May create expectations among customers that principal is always negotiable (should be discouraged in general lending behavior)."
  ],
  "tool_results":{"Principal_waiver_5%":{'type': 'Settlement Plan with Waive-Off', 'total_settlement': 9025.05, 'Loan_amount': 10000, 'Interest_rate': 0.05, 'Term': 60, 'waived_fee': 1041.13, 'Updated dues': 0.0, 'monthly_balance': 188.71, 'description': 'Calculated based on requested waiver percentages.'},
                  "Pricipal_waiver_10%":{'type': 'Settlement Plan with Waive-Off', 'total_settlement': 8550.05, 'Loan_amount': 10000, 'Interest_rate': 0.05, 'Term': 60, 'waived_fee': 1516.13, 'Updated dues': 0.0, 'monthly_balance': 188.71, 'description': 'Calculated based on requested waiver percentages.'}}
},
      ]
    }
}

    return repayment_plans[customer_id]