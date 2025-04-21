import json

def get_plans(customer_id:str):
    repayment_plans = {
        "CUST654321":{
            "plans": [
             { "plan_id": 1,
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest and tenure unchanged, Same Principal loan amount.",
      "negotiation_steps" : ["1. Explain the benefits of taking this plan to the customer using the numbers."
          "2. Call appropriate tools"
          "3. Negotiate with the customer atleast 3 times to make him understand the plan and the benefits it wil reap."],
      "Example": """
          system : According to the current situation, We think a refinance of X$ which is same as you principal loan amont with same y tenure and z% interest is the best and only option we can offer you.
          user: I am not sure if I want to refinance.
          system: I understand that you are going through a lot, let me explain about refiance and how this is your best option as of now, which helps you by giving A$ in cash which can help you come out of current financial situation.
          user: But i need more options | I need more money | this is not helping me out
          system: I understand you need more options|money| help, let me explain how this plan can help you by giving you B$ in cash which can help you come out of current financial and your new loan will be of X$(same loan amount) with same y tenure and z% interest. This is the best option we can offer you as of now
          """,},
                {
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 3,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.Percentage list [10,20,30,40,50]",
  "negotiation_steps": [
      "1. Make a tool call with the current percentage, reset the threshold to 3"
      "2. Negotiate with the customer to make him understand the plan and the benefits it will reap. act like this is the only option that we can offer him."
      "3. For each percentage you need to negotiate with the customer until threshold gets 0",
      "4. If threshold is reached 0, change the percentage and start from step 1 in negotiation_steps",
      "5. Even if customer asks for more percentage or offers you more percentage you need to stay on the same percentage."
      "6. You cant directly go to other percentages in the list before coving the previous precentages you need to go step by step with each step you can reduce 10%.",
      "7. You cant go to other percentage until you have negotiated with customer for the current percentage.",
      ],
  "example": """
system: Based on your current financial situation, we believe reducing your loan amount by X$- 0.1*X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will reduce your monthly payments, helping to ease your financial burden.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by reducing your loan by 10%, you lower your monthly payments significantly, making it easier to manage your finances. This step can reduce your burden without affecting your financial flexibility too much.  
user: But I need more options | I need less debt | This is not helping me enough.  
system: I completely understand. Right now, the **10% reduction is your best option** because it helps reduce your monthly payments without stretching your budget. If you’re looking for more relief, we can **first see how this reduction improves your situation** before considering anything else. Would you like me to show how this adjustment fits your current needs?  
(user continues resisting) 
user: I want 40% reduction. 
system: I understand you want more reduction but as of now we can only offer you 10% reduction (Use next percentage only after offering current percentage and you need to go in steps ie 20% next in current example)"""
},
               {
  "plan_id": 4,
  "name": "Extended Payment Plan 3 Months upto 12 months",
  "priority": 3,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->12 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
 
},
{
  "plan_id": 6,
  "name": "Extended Payment Plan 3 Months upto 24 months",
  "priority": 4,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
  
},
{
  "plan_id": 5,
  "name": "Extended Payment Plan 6 Months upto 24 months",
  "priority": 5,
  "description": "Extend repayment period by 6 months for smaller installments while maintaining reasonable interest costs until .",
  "negotiation_steps": [
    "1. Start by offering the 6-month extension as the best and only option. Reinforce its benefits by highlighting the reduced monthly payment for at least three attempts before moving to the next step.",
    "2. Call the function to calculate the new monthly payment.",
    "3. Emphasize that the 6-month extension strikes a balance between affordability and the repayment period, reducing financial strain without drastically increasing the overall cost.",
    "4. If the customer declines or asks for a longer term, explain why the 6-month extension is the best fit for now.",
    "5. Only introduce the 12-month extension if the customer firmly requests more relief, but do so step-by-step (6 months → 12 months ->18 months->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest."
  ],
  
}
            ]
        },
 "CUST445566":{
  "plans": [
    {
      "plan_id": 1,
      "name": "Refinance Plan",
      "priority": 1,
      "description": "Refinance existing loans with new terms to reduce monthly payments or extend the loan tenure.",
      "options": [
        {
          "option_name": "Refinance Step Same",
          "description": "Keep interest rate and tenure the same, loan amount equals remaining balance + dues + 10% buffer.",
          "negotiation_parameters": "No specific parameters.",
          "wolfram_alpha_use": "Calculate new monthly payment and total interest.",
          "tailored_message": "A stable option with predictable payments for your mortgage."
        },
        {
          "option_name": "Refinance Step Down",
          "description": "Lower the loan amount by up to 30%.",
          "negotiation_parameters": "Negotiate loan decrease percentage in steps of 10%.",
          "wolfram_alpha_use": "Calculate adjusted monthly payments and reduced total interest.",
          "tailored_message": "Reduce your loan burden significantly while keeping manageable payments."
        },
        {
          "option_name": "Refinance Step Up",
          "description": "Increase the loan amount by up to 20% to cover immediate needs.",
          "negotiation_parameters": "Negotiate loan increase percentage in steps of 5%.",
          "wolfram_alpha_use": "Calculate new total monthly payments and interest.",
          "tailored_message": "A flexible option to cover short-term needs."
        }
      ],
      "negotiation_rules": [
        "Begin with Refinance Step Same to emphasize predictable payments.",
        "Switch to Step Down after 1 rejection to highlight long-term savings.",
        "Use Wolfram Alpha to show reduced monthly payments with exact figures.",
        "Never combine refinance options or reveal alternative plans."
      ]
    },
    {
      "plan_id": 2,
      "name": "Extended Payment Plan",
      "priority": 2,
      "description": "Restructure mortgage or personal loan to extend repayment timeline and reduce monthly payments.",
      "options": [
        {
          "option_name": "EPP up to 24 cycles",
          "description": "Extend loan tenure by 6/12/18/24 cycles.",
          "negotiation_parameters": "Negotiate the number of cycles extended based on financial strain.",
          "wolfram_alpha_use": "Calculate monthly savings for each extension level.",
          "tailored_message": "Extend payments for more breathing room in your budget."
        }
      ],
      "negotiation_rules": [
        "Focus on the mortgage first for significant impact on finances.",
        "Show how each extension reduces monthly payments step-by-step.",
        "Offer shorter extensions initially (6 cycles), increasing after rejections.",
        "Highlight how this avoids loan default and protects credit score."
      ]
    },
    {
      "plan_id": 3,
      "name": "Settlement Plan with Waive-Off",
      "priority": 3,
      "description": "Settle personal loan by waiving fees, interest, or a portion of the principal.",
      "options": [
        {
          "option_name": "Waive Interest (up to 30%)",
          "description": "Negotiate interest waiver percentage starting at 10%.",
          "negotiation_parameters": "Adjust waiver percentage based on financial history.",
          "wolfram_alpha_use": "Calculate interest savings based on waiver.",
          "tailored_message": "Reduce your personal loan burden quickly with interest waivers."
        },
        {
          "option_name": "Waive Principal (up to 10%)",
          "description": "Negotiate principal waiver percentage starting at 5%.",
          "negotiation_parameters": "Increase waiver based on negotiation progress.",
          "wolfram_alpha_use": "Calculate new principal and monthly payments.",
          "tailored_message": "Save significantly by reducing the loan principal."
        }
      ],
      "negotiation_rules": [
        "Start with fee or interest waivers for easier approvals.",
        "Offer principal waivers only after 2 rejections.",
        "Emphasize fast loan closure benefits and credit score protection.",
        "Use Wolfram Alpha to illustrate total cost savings."
      ]
    }
  ]
},
"CUST778899":{
  "plans": [
    {
      "plan_id": 1,
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest rate, tenure, and loan amount the same. Restructure only to maintain manageable payments.",
      "steps": [
        "Explain the benefits of stability with unchanged terms.",
        "Confirm if the borrower values predictability in payments.",
        "Avoid introducing additional features unless explicitly requested.",
        "Validate affordability using simple calculations or tools."
      ],
      "negotiation_parameters": "No changes to terms; maintain current structure.",
      "wolfram_alpha_use": "Calculate existing loan payments for validation.",
      "tailored_message": "Predictable payments with no surprises for added stability."
    },
    {
      "plan_id": 2,
      "name": "Refinance Step Down",
      "priority": 2,
      "description": "Reduce the loan amount by a percentage, keeping other terms unchanged.",
      "steps": [
        "Start by offering a 10% reduction in loan amount.",
        "Negotiate increments in steps of 10%, with a maximum reduction of 50%.",
        "Highlight reduced repayment burden and its immediate impact.",
        "Use affordability analysis to show benefits at each step.",
        "Confirm borrower satisfaction before finalizing the step."
      ],
      "negotiation_parameters": "Negotiate on loan amount reduction in steps of 10%, up to 50%.",
      "wolfram_alpha_use": "Calculate reduced monthly payments for each step.",
      "tailored_message": "A tailored refinancing option to reduce financial burden."
    },
    {
      "plan_id": 3,
      "name": "Refinance Step Up",
      "priority": 3,
      "description": "Increase the loan amount by a percentage, keeping other terms unchanged.",
      "steps": [
        "Begin with a proposal for a 10% increase in loan amount.",
        "Incrementally negotiate in steps of 10%, up to 50%.",
        "Emphasize the potential for meeting immediate financial needs.",
        "Validate repayment feasibility using financial projections.",
        "Close negotiation once the borrower confirms the increase suffices."
      ],
      "negotiation_parameters": "Negotiate on loan amount increase in steps of 10%, up to 50%.",
      "wolfram_alpha_use": "Calculate increased monthly payments for each step.",
      "tailored_message": "Meet urgent financial needs with manageable terms."
    },
    {
      "plan_id": 4,
      "name": "Extended Payment Plan (Up to 12 Cycles)",
      "priority": 4,
      "description": "Extend repayment tenure by 3/6/9/12 cycles for loans with remaining tenure ≤12 cycles.",
      "steps": [
        "Offer the smallest extension (3 cycles) initially.",
        "Incrementally negotiate in steps of 3 cycles, up to 12 cycles.",
        "Highlight the reduced monthly payment for each step.",
        "Address borrower concerns about increased interest due to extension.",
        "Ensure clarity about overall repayment obligations."
      ],
      "negotiation_parameters": "Negotiate the number of cycles to extend in steps of 3, up to 12.",
      "wolfram_alpha_use": "Calculate reduced monthly payments for each extension.",
      "tailored_message": "Flexible extensions for reduced financial pressure."
    },
    {
      "plan_id": 5,
      "name": "Extended Payment Plan (Up to 24 Cycles in Steps of 6)",
      "priority": 5,
      "description": "Extend repayment tenure by 6/12/18/24 cycles for loans with remaining tenure >12 cycles.",
      "steps": [
        "Begin by offering an extension of 6 cycles.",
        "Incrementally negotiate in steps of 6, up to 24 cycles.",
        "Demonstrate monthly payment relief with financial breakdowns.",
        "Discuss the trade-off of higher overall interest for immediate relief.",
        "Confirm borrower agreement for the selected step."
      ],
      "negotiation_parameters": "Negotiate the number of cycles to extend in steps of 6, up to 24.",
      "wolfram_alpha_use": "Calculate the monthly payment relief for each step.",
      "tailored_message": "Relieve financial stress with extended payment options."
    },
    {
      "plan_id": 6,
      "name": "Waive Fees (Up to 100%)",
      "priority": 6,
      "description": "Offer fee waivers starting at 25% and incrementally negotiate up to 100%.",
      "steps": [
        "Begin by proposing a 25% waiver of fees.",
        "Increment in steps of 25%, stopping at borrower’s request or 100%.",
        "Reinforce the benefits of immediate cost savings at each step.",
        "If the borrower demands more, offer the next step only after rejecting the current one.",
        "Use persuasive data to support fee waivers and their impact."
      ],
      "negotiation_parameters": "Negotiate fee waiver percentage in steps of 25%, up to 100%.",
      "wolfram_alpha_use": "Calculate cost savings for each waiver step.",
      "tailored_message": "Clear your dues faster with waived fees."
    }
  ]
},
 "CUST123456":{
      "plans": [  
    {
  "plan_id": 1,
  "name": "Refinance Same Step",
  "priority": 1,
  "description": "Customer continues at the same loan amount, same interest rate, and same loan term — but benefits from a revised structure like reduced EMI.",
  "is_step_based": False,
  "tool_call_template": "refinance_same_step()",
  "negotiation_rules": [
    "Start by explaining that this plan keeps everything familiar — same loan, same structure — but with an optimized repayment schedule.",
    "Emphasize peace of mind: ‘No increase in debt, just smoother payments.’",
    "Use tool output to show reduced EMI or better interest rate, reinforcing: ‘This gives you breathing room without touching your loan balance.’",
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
  ]
},
{
  "plan_id": 2,
  "name": "Refinance Step Up",
  "priority": 2,
  "description": "Increase loan principal slightly to restructure and reduce EMI, often with a longer tenure or lower interest rate.",
  "is_step_based": True,
  "Steps": [10, 20, 30, 40, 50],
  "Step_description": "Use the percentage given in steps. Always begin at 10% and progress in order if needed, never skipping.",
  "tool_call_template": "refinance_step_up(percentage={step_value})",
  "negotiation_rules": [
    "Begin by highlighting the benefit: more money in hand while maintaining manageable monthly payments.",
    "Only introduce the loan increase after showing how it leads to better short-term cash flow.",
    "Use tool output to explain the tradeoff: ‘Your EMI will go up by $X, but you immediately get $Y in hand.’",
    "Repeat benefits if there's hesitation — especially the cash-in-hand and reduced pressure.",
    "Use soft phrases like: 'This helps you stay on track without skipping payments or feeling stretched.'",
    "Always frame it as: 'the most practical plan based on your current situation.'"
  ],
  "pros": [
    "Gives more upfront money to handle urgent needs.",
    "Reduces immediate financial pressure with better liquidity.",
    "Keeps the customer in control of payments while avoiding default.",
    "Structured progression allows adjustments without drastic jumps."
  ],
  "cons": [
    "Monthly EMI increases slightly with each step.",
    "Total debt burden may rise due to increased loan principal.",
    "Longer term may mean higher total interest paid.",
    "Needs careful explanation to avoid fear of 'taking on more debt.'"
  ]
},
{
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 3,
  "description": "This plan gradually reduces your total debt by lowering your loan amount in steps, while keeping monthly payments manageable.",
  "is_step_based": True,
  "Steps": [10, 20, 30, 40, 50],
  "Step_description": "We start with a 10% reduction and move step-by-step to higher reductions, up to 50%, only if needed.",
  "tool_call_template": "refinance_step_down(percentage=<step>)",
  "negotiation_rules": [
    "This plan is designed to reduce your loan burden gradually, starting with a 10% cut.",
    "We’ve calculated a new proposal that gives you a lighter monthly payment while also lowering your total debt.",
    "By starting small and adjusting only if necessary, you stay in control and avoid drastic changes all at once.",
    "As you continue with this plan, more relief can be unlocked step-by-step — it’s flexible and built around your comfort.",
    "This is the most responsible and helpful option for your situation today. Let’s look at how much you benefit with the first step."
  ],
  "pros": [
    "You reduce your overall loan burden with each step — not just the EMI.",
    "Monthly payments become easier without changing everything at once.",
    "You’re always in control — we move to the next step only if needed and you're comfortable."
  ],
  "cons": [
    "Since the relief is gradual, it may take a bit more time to reach the full benefit.",
    "Each step still requires a small decision, so progress happens one stage at a time.",
    "If you’re looking for a large one-time change, this plan works better through steady progress instead."
  ]
},
  {
  "plan_id": 4,
  "name": "Extended Payment Plan (3 to 12 Months)",
  "priority": 4,
  "description": "This plan helps lower your monthly payments by extending your loan term gradually—starting with just 3 months and moving up only if needed.",
  "is_step_based": True,
  "Steps": [3, 6, 9, 12],
  "Step_description": "We begin with a 3-month extension and step up to 6, 9, or 12 months only if more support is required.",
  "tool_call_template": "extended_payment_plan(months=<step>)",
  "negotiation_rules": [
    "Let’s start with a 3-month extension — this gives you smaller EMIs without changing your loan too much.",
    "This option keeps your total interest impact low while helping you manage payments better.",
    "If you’re still feeling pressure, we can explore extending a bit further — up to 6 or 9 months if needed.",
    "We move step-by-step so you’re never overwhelmed. Every stage is based on your comfort and need.",
    "These options are time-sensitive, so taking early action means better chances of approval."
  ],
  "pros": [
    "Gives quick EMI relief while keeping your loan structure mostly intact.",
    "The changes are small and manageable — a soft landing rather than a major change.",
    "You always decide if the next step makes sense — you stay in control the whole way."
  ],
  "cons": [
    "The initial step provides mild relief — may not be enough if your situation is urgent.",
    "We’ll need to go step-by-step to reach the full benefit, which takes a little more time.",
    "The total loan duration may increase slightly depending on how far we go."
  ]
},
{
  "plan_id": 6,
  "name": "Extended Payment Plan 3 Months upto 24 months",
  "priority": 5,
  "description": "Extend repayment period by 3 months, up to 24 months, with reduced EMI while keeping cost manageable.",
  "is_step_based": True,
  "Steps": [15,18,21,24],
  "Step_description": "Use the extended cycle months given in steps, you need to iterate over all the step until reached end of list",
  "negotiation_rules": {
    "steps": [
      "Call `extend_term(months=3)` first and show benefits.",
      "Push the 3-month extension as the default and optimal solution for financial relief.",
      "Repeat 3 times using updated EMI values to emphasize reduced burden.",
      "Use urgency language: 'This option may not be available later.'"
    ],

  },
  "pros": [
    "Highly flexible — allows fine-tuned negotiation from short to long extensions.",
    "Good for customers whose situation may change mid-way (adaptive support).",
    "Lower EMIs in manageable steps, avoids overwhelming user with large changes."
  ],
  "cons": [
    "Can result in significantly longer loan durations if maxed out.",
    "Multiple decision points create friction and may cause drop-off.",
    "Requires disciplined flow control to prevent jumping ahead."
  ]
},
{
  "plan_id": 5,
  "name": "Extended Payment Plan (6 to 24 Months)",
  "priority": 6,
  "description": "This plan gives you immediate relief by reducing your monthly EMI, starting with a 6-month extension. If needed, we can gradually extend further — up to 24 months — based on your comfort and situation.",
  "is_step_based": True,
  "Steps": [6, 12, 18, 24],
  "Step_description": "We begin with a 6-month extension and gradually offer longer durations only if you're still under financial pressure.",
  "tool_call_template": "extended_payment_plan(months=<step>)",
  "negotiation_rules": [
    "Let’s start by extending your loan term by 6 months. This gives you a lower EMI right away — making it easier to manage monthly expenses.",
    "We’ll keep things simple. The 6-month step gives significant relief while keeping total interest low.",
    "If you're still finding it difficult after this, we can gradually move to 12, 18, or 24 months — but only if needed.",
    "Each step is offered only when you show continued need. You stay in control of how far we go.",
    "This is a limited-time relief plan, so acting early ensures better terms and smoother approval."
  ],
  "pros": [
    "Gives larger EMI relief quickly — great if you're feeling immediate pressure.",
    "Fewer steps mean faster resolution compared to shorter-term extension plans.",
    "Balances short-term support with long-term affordability — interest doesn’t grow drastically."
  ],
  "cons": [
    "Initial jump of 6 months may feel like a bigger change compared to smaller-step plans.",
    "Not ideal for customers who only need slight adjustments.",
    "Each additional extension requires reassessment — some may prefer more gradual flexibility."
  ]
}
  ]
    },
    
"CUST234567":{
      "plans": [
        {
  "plan_id": 3,
  "name": "Settlement Plan with Fee Waive-Off",
  "priority": 1,
  "description": "If you're going through financial distress and unable to repay the full amount, this plan helps settle your loan by gradually waiving off fees in steps — starting from 25% and going up to 100%.",
  "is_step_based": True,
  "Steps": [25, 50, 75, 100],
  "Step_description": "Each step increases the waiver on fees by 25%. We begin at 25% and only proceed further based on your situation and feedback.",
  "tool_call_template": "settle_with_fee_waiver(waiver_percentage=<step>)",
  "negotiation_rules": [
    "Start by offering a 25% fee waiver as a one-time support gesture to ease the financial pressure.",
    "Clearly explain that this offer helps avoid legal escalation and long-term financial consequences.",
    "Let the customer know that the remaining balance still needs to be paid — but this waiver makes it significantly lighter.",
    "If the user expresses continued difficulty (`pchange == true`) and `threshold == 0`, proceed to the next waiver step (50%, then 75%, then 100%).",
    "Avoid jumping directly to 100% — we offer help gradually, showing flexibility and care.",
    "Always emphasize: 'We’re working with you step by step to close this chapter with dignity and as little strain as possible.'"
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
  ]
},
        {
  "plan_id": 6,
  "name": "Settlement Plan with Interest Reduction",
  "priority": 2,
  "description": "Designed for customers in financial difficulty who are willing to settle the principal but need relief from interest. The plan offers stepwise reduction in interest — from 25% up to 100% — based on the customer's repayment intent.",
  "is_step_based": True,
  "Steps": [25, 50, 75, 100],
  "Step_description": "Each step increases the waiver on interest by 25%. Start with 25% interest waived and only increase based on customer’s situation.",
  "tool_call_template": "settle_with_interest_waiver(waiver_percentage=<step>)",
  "negotiation_rules": [
    "Begin with a 25% interest waiver using `settle_with_interest_waiver(waiver_percentage=25)`, showing a substantial saving on total payable amount.",
    "Explain that this step gives the customer a clean way out — settling principal without the full weight of interest.",
    "Clearly highlight the benefits: 'With just a 25% interest waiver, you're already saving a significant amount while clearing your name financially.'",
    "If customer indicates continued difficulty (`pchange == true` and `threshold == 0`), move to the next step: 50% interest waived — and so on.",
    "Strictly follow step sequence: 25 → 50 → 75 → 100%. Never skip.",
    "Emphasize: 'The more committed you are to resolving this, the more support we can offer to reduce your burden step-by-step.'",
    "Always make sure the principal amount is discussed as non-negotiable — focus relief only on the interest component."
  ],
  "pros": [
    "Gives customers a fair path to settle their dues while feeling supported and not penalized harshly.",
    "Reduces emotional and financial stress by avoiding full interest repayment.",
    "Step-based approach increases trust and flexibility in resolution."
  ],
  "cons": [
    "Customer still needs to pay full principal, which might be challenging in extreme hardship cases.",
    "May require multiple back-and-forth steps to reach the optimal settlement level.",
    "If not well explained, customers might misunderstand the partial interest waiver as complete forgiveness."
  ]
},
        {
  "plan_id": 7,
  "name": "Settlement Plan with Principal Waiver",
  "priority": 3,
  "description": "This plan is for customers facing extreme financial hardship. It offers partial forgiveness on the loan principal, starting at 2.5% and increasing up to 40%, to help them close the loan through a negotiated settlement.",
  "is_step_based": True,
  "Steps": [2.5, 5, 10, 20, 30, 40],
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
  ]
},
      ]
    }
}

    return repayment_plans[customer_id]

