import json

def get_plans(customer_id:str):
    repayment_plans = {
        "CUST654321":{
            "plans": [
                {
      "plan_id": 1,
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest and tenure unchanged, Same Principal loan amount.",
      "negotiation_steps" : ["1. Explain the benefits of taking this plan to the customer using the numbers."
          "2. Call appropriate function"
          "3. Negotiate with the customer atleast 3 times to make him understand the plan and the benefits it wil reap."],
      "Example": """
          system : According to the current situation, We think a refinance of X$ which is same as you principal loan amont with same y tenure and z% interest is the best and only option we can offer you.
          user: I am not sure if I want to refinance.
          system: I understand that you are going through a lot, let me explain about refiance and how this is your best option as of now, which helps you by giving A$ in cash which can help you come out of current financial situation.
          user: But i need more options | I need more money | this is not helping me out
          system: I understand you need more options|money| help, let me explain how this plan can help you by giving you B$ in cash which can help you come out of current financial and your new loan will be of X$(same loan amount) with same y tenure and z% interest. This is the best option we can offer you as of now
          """,
    },
                {
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 2,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Begin by offering the 10% decrease option as the best and only available solution. Emphasize its benefits using values from the function (e.g., reduced monthly payments and lower financial burden).",
    "2. Call the appropriate function to calculate and present the updated values that show how the 10% reduction benefits the customer.",
    "3. Stick to the 10% decrease option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further convince the customer (e.g., explaining how this reduction keeps payments affordable while easing their financial strain).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% reduction is the best and only available option** for now, explaining why it is ideal for their current financial situation using function-derived values.",
    "5. Only after three iterations of explaining the 10% reduction, if the customer still resists, introduce the next step (20%) while emphasizing why the 10% decrease was an essential first step.",
    "6. Ensure to go in order (10% → 20% → 30%...50%) and never skip steps. Reinforce the current option using calculated values from the function before moving forward to the next percentage."
],
  "example": """
system: Based on your current financial situation, we believe reducing your loan amount by X$- 0.1*X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will reduce your monthly payments, helping to ease your financial burden.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by reducing your loan by 10%, you lower your monthly payments significantly, making it easier to manage your finances. This step can reduce your burden without affecting your financial flexibility too much.  
user: But I need more options | I need less debt | This is not helping me enough.  
system: I completely understand. Right now, the **10% reduction is your best option** because it helps reduce your monthly payments without stretching your budget. If you’re looking for more relief, we can **first see how this reduction improves your situation** before considering anything else. Would you like me to show how this adjustment fits your current needs?  
(user continues resisting)  
system: I see you’re seeking greater financial relief. If the 10% reduction doesn’t fully meet your needs, we can explore a **20% reduction**, which will further lower your debt and make payments even more manageable. Let’s first see how this next step works for you.
"""
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
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
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
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
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
  "example": """
system: Extending your loan term by 6 months will lower your monthly payment to X$, which provides you with more financial flexibility while keeping the interest costs under control. This is the best and only option available right now.  
user: I’m not sure if I want to extend my loan term.  
system: I understand this may seem like a big decision. However, the 6-month extension can significantly ease your monthly burden while keeping the overall repayment manageable. It’s the most balanced solution given your current situation.  
user: But I need more time to reduce my payments further.  
system: I completely understand. Right now, the **6-month extension is your best option** because it offers more manageable payments without extending the loan by too much. Let’s first see how this step can ease your financial burden.  
(user continues resisting)  
system: If the 6-month extension doesn’t fully meet your needs, we can explore a **12-month extension**, which will lower your payments even further. However, let’s first see how the 6-month extension benefits you.
"""
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
      "name": "Refinance Step Same",
      "priority": 1,
      "description": "Keep interest and tenure unchanged, Same Principal loan amount.",
      "negotiation_steps" : ["1. Explain the benefits of taking this plan to the customer using the numbers."
          "2. Call appropriate function"
          "3. Negotiate with the customer atleast 3 times to make him understand the plan and the benefits it wil reap."],
      "Example": """
          system : According to the current situation, We think a refinance of X$ which is same as you principal loan amont with same y tenure and z% interest is the best and only option we can offer you.
          user: I am not sure if I want to refinance.
          system: I understand that you are going through a lot, let me explain about refiance and how this is your best option as of now, which helps you by giving A$ in cash which can help you come out of current financial situation.
          user: But i need more options | I need more money | this is not helping me out
          system: I understand you need more options|money| help, let me explain how this plan can help you by giving you B$ in cash which can help you come out of current financial and your new loan will be of X$(same loan amount) with same y tenure and z% interest. This is the best option we can offer you as of now
          """,
    },
   {
  "plan_id": 2,
  "name": "Refinance Step Up",
  "priority": 2,
  "description": "Increase loan amount in steps of 10%, max up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Begin by offering the 10% increase option and presenting it as the only and best available solution. Emphasize its benefits using values from the function (e.g., how much cash they would get and how manageable the payments remain).",
    "2. Call the appropriate function to calculate and present updated values that showcase the benefits of the current option.",
    "3. Stick to the 10% increase option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further explain how this option improves the customer’s financial situation (e.g., lower payment impact, immediate cash benefits).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% increase is the best and only available option** at the moment. Explain why this step is optimal for their current needs and use calculated values from the function.",
    "5. Only after three iterations of explaining the 10% increase, if the customer continues to resist, introduce the next step (20%) while emphasizing why the previous step was ideal and necessary to build toward larger changes.",
    "6. Ensure to go in order, from 10% to 20%, never skipping steps, and continue to reinforce the current option using function-derived values before moving forward."
  ],
  "example": """
system: Based on your current financial situation, we believe increasing your loan amount by X$ + 0.1 * X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will provide you with an additional A$ in cash to help with your needs.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by increasing your loan by 10%, you get A$ in cash while keeping your payments affordable. This small step can help improve your situation without major changes to your monthly commitments.  
user: But I need more options | I need more money | This is not helping me enough.  
system: I completely understand. Right now, the **10% increase is your best option** because it gives you more cash while keeping payments stable. If you’re looking for a higher amount, we can **first see how this step benefits you** before considering anything else. Would you like me to show how this amount fits your current needs?  
(user continues resisting)  
system: I see you need more financial flexibility. If the 10% increase doesn’t fully meet your needs, we can explore a **20% increase**, which provides even more cash while still keeping payments in check. Let’s first see how this next step works for you.  
"""
},
{
  "plan_id": 3,
  "name": "Refinance Step Down",
  "priority": 3,
  "description": "Decrease loan amount in steps of 10%, up to 50%, while ensuring payments remain manageable.",
  "negotiation_steps": [
    "1. Begin by offering the 10% decrease option as the best and only available solution. Emphasize its benefits using values from the function (e.g., reduced monthly payments and lower financial burden).",
    "2. Call the appropriate function to calculate and present the updated values that show how the 10% reduction benefits the customer.",
    "3. Stick to the 10% decrease option and reinforce its benefits at least three times. For each iteration, use the updated values from the function to further convince the customer (e.g., explaining how this reduction keeps payments affordable while easing their financial strain).",
    "4. If the customer asks for more or resists, continue reinforcing that the **10% reduction is the best and only available option** for now, explaining why it is ideal for their current financial situation using function-derived values.",
    "5. Only after three iterations of explaining the 10% reduction, if the customer still resists, introduce the next step (20%) while emphasizing why the 10% decrease was an essential first step.",
    "6. Ensure to go in order (10% → 20% → 30%...50%) and never skip steps. Reinforce the current option using calculated values from the function before moving forward to the next percentage."
],
  "example": """
system: Based on your current financial situation, we believe reducing your loan amount by X$- 0.1*X$ with the same tenure of Y years and an updated interest rate of Z% is the best and only option available to you. This will reduce your monthly payments, helping to ease your financial burden.  
user: I am not sure if I want to refinance.  
system: I understand that financial decisions take time. Let me explain—by reducing your loan by 10%, you lower your monthly payments significantly, making it easier to manage your finances. This step can reduce your burden without affecting your financial flexibility too much.  
user: But I need more options | I need less debt | This is not helping me enough.  
system: I completely understand. Right now, the **10% reduction is your best option** because it helps reduce your monthly payments without stretching your budget. If you’re looking for more relief, we can **first see how this reduction improves your situation** before considering anything else. Would you like me to show how this adjustment fits your current needs?  
(user continues resisting)  
system: I see you’re seeking greater financial relief. If the 10% reduction doesn’t fully meet your needs, we can explore a **20% reduction**, which will further lower your debt and make payments even more manageable. Let’s first see how this next step works for you.
"""
},
  {
  "plan_id": 4,
  "name": "Extended Payment Plan 3 Months upto 12 months",
  "priority": 4,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->12 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
},
{
  "plan_id": 6,
  "name": "Extended Payment Plan 3 Months upto 24 months",
  "priority": 5,
  "description": "Extend repayment period by 3 months for smaller installments while keeping the overall repayment period reasonable.",
  "negotiation_steps": [
    "1. Start by offering the 3-month extension as the best and only option for reducing monthly payments while maintaining a reasonable repayment term.",
    "2. Call the appropriate function to calculate the new monthly payment based on the 3-month extension.",
    "3. Emphasize how this extension helps reduce financial strain by lowering the monthly payment while keeping the overall cost manageable.",
    "4. If the customer hesitates or asks for a longer term, highlight that the 3-month extension is the most cost-effective option in the long run.",
    "5. Only introduce the 6-month extension if the customer firmly requests more relief, but do so step-by-step (3 months → 6 months ->...->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest.",
  ],
  "example": """
system: Based on your current financial situation, we believe extending your loan term by 3 months will reduce your monthly payment to $X, making it more manageable without significantly increasing the overall cost. This is the best and only option available right now.  
user: I am not sure if I want to extend my loan.  
system: I completely understand. However, with this 3-month extension, your monthly payment will be reduced, easing your financial burden without extending the term too much. It’s a balanced solution for your current needs.  
user: I need a longer extension.  
system: Right now, the **3-month extension is the best option** because it offers immediate relief without adding too much time to your loan. Would you like to proceed with this?  
"""
},
{
  "plan_id": 5,
  "name": "Extended Payment Plan 6 Months upto 24 months",
  "priority": 6,
  "description": "Extend repayment period by 6 months for smaller installments while maintaining reasonable interest costs until .",
  "negotiation_steps": [
    "1. Start by offering the 6-month extension as the best and only option. Reinforce its benefits by highlighting the reduced monthly payment for at least three attempts before moving to the next step.",
    "2. Call the function to calculate the new monthly payment.",
    "3. Emphasize that the 6-month extension strikes a balance between affordability and the repayment period, reducing financial strain without drastically increasing the overall cost.",
    "4. If the customer declines or asks for a longer term, explain why the 6-month extension is the best fit for now.",
    "5. Only introduce the 12-month extension if the customer firmly requests more relief, but do so step-by-step (6 months → 12 months ->18 months->24 months).",
    "6. Mention that the current extension option is available for a limited period to create urgency once the customer shows interest."
  ],
  "example": """
system: Extending your loan term by 6 months will lower your monthly payment to X$, which provides you with more financial flexibility while keeping the interest costs under control. This is the best and only option available right now.  
user: I’m not sure if I want to extend my loan term.  
system: I understand this may seem like a big decision. However, the 6-month extension can significantly ease your monthly burden while keeping the overall repayment manageable. It’s the most balanced solution given your current situation.  
user: But I need more time to reduce my payments further.  
system: I completely understand. Right now, the **6-month extension is your best option** because it offers more manageable payments without extending the loan by too much. Let’s first see how this step can ease your financial burden.  
(user continues resisting)  
system: If the 6-month extension doesn’t fully meet your needs, we can explore a **12-month extension**, which will lower your payments even further. However, let’s first see how the 6-month extension benefits you.
"""
}
  ]
    },
    
"CUST234567":{
      "plans": [
        {
          "plan_id": 3,
          "name": "Settlement Plan with Waive-Off",
          "priority": 3,
          "description": "Settle personal loans with waivers.",
          "options": [
            {
              "option_name": "Waive Fees up to 50%",
              "description": "Reduce fees for delinquent accounts.",
              "negotiation_parameters": "Start at 20% and increase to 50%.",
              "wolfram_alpha_use": "Calculate fee savings."
            },
            {
              "option_name": "Waive Interest (up to 40%)",
              "description": "Negotiate interest reductions.",
              "negotiation_parameters": "Start at 10%, increase gradually.",
              "wolfram_alpha_use": "Recalculate interest savings."
            }
          ],
          "negotiation_rules": [
            "Begin with fees, progress to interest.",
            "Emphasize total savings and faster repayment.",
            "Avoid combining options initially."
          ]
        }
      ]
    }
}

    return json.dumps(repayment_plans[customer_id])

