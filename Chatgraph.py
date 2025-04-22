from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os
import json
import random
from customer_details import get_customer_details
from plans import get_plans
from calculation import (
    refinance_same, refinance_step_down, refinance_step_up,
    extended_payment_plan, settlement_plan_with_waivers
)


load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
Api_key = os.getenv("TOGETHER_API_KEY2")
class State(TypedDict):
    messages: list
    customer_details: dict
    current_plan: str
    plans: dict
    Sentiment: str
    Threshold: int
    Greedy: int
    pchange: bool
    user_history : bool




llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key)
llm2 = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=Api_key)
tool_mapping = {
    "refinance_same": refinance_same,
    "refinance_step_down": refinance_step_down,
    "refinance_step_up": refinance_step_up,
    "extended_payment_plan": extended_payment_plan,
    "settlement_plan_with_waivers": settlement_plan_with_waivers,
}

tools = [{
        "type": "function",
        "function": {
            "name": "get_customer_details",  
            "description": "Retrieve customer details by client ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "Customer ID to retrieve details"}
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_plans",
            "description": "Retrieve financial plans of a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer ID for fetching plans"},
                },
                "required": ["customer_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "refinance_same",
            "description": "Calculate new terms for Refinance Step Same plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                },
                "required": ["Principal", "interest_rate", "loan_term","remaining_balance", "due"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "refinance_step_down",
            "description": "Calculate new terms for Refinance Step Down plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "loan_term": {"type": "number"},
                    "reduce_percent": {"type": "number"},
                    "remaining_balance": { "type": "number" },
                    "due": {"type": "number"},
                    
                },
                "required": ["Principal", "interest_rate", "loan_term", "reduce_percent","remaining_balance", "due"]
            }
        }
    },
    
    {
        "type": "function",
        "function": {
            "name": "extended_payment_plan",
            "description": "Calculate new terms for Extended Payment Plan",
            "parameters": {
                "type": "object",
                "properties": {
                    "Principal": {"type": "number"},
                    "interest_rate": {"type": "number"},
                    "original_term": {"type": "number"},
                    "extension_cycles": {"type": "number"}
                },
                "required": ["Principal", "interest_rate", "original_term", "extension_cycles"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "settlement_plan_with_waivers",
            "description": "Calculate settlement plan with waivers",
            "parameters": {
                "type": "object",
                "properties": {
                    "Principal": {"type": "number"},
                    "fee_waiver_percent": {"type": "number"},
                    "interest_waiver_percent": {"type": "number"},
                    "principal_waiver_percent": {"type": "number"}
                },
                "required": ["Principal", "fee_waiver_percent", "interest_waiver_percent", "principal_waiver_percent"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "refinance_step_up",
        "description": "Calculates financials for Refinance Step Up plan with an increase percentage",
        "parameters": {
            "type": "object",
            "properties": {
                "Principal": {"type": "number"},
                "interest_rate": {"type": "number"},
                "loan_term": {"type": "integer"},
                "increase_percent": {"type": "number", "description": "Percentage to increase the loan amount by"},
                "remaining_balance": { "type": "number" },
                "due": {"type": "number"},
            },
            "required": ["Principal", "interest_rate", "loan_term", "increase_percent","remaining_balance", "due"]
        }
    }
    },
]
llm_with_tools = llm.bind_tools(list(tool_mapping.values()))
# llm_with_tools = llm.bind_tools(tools)
toolcalling = []
def input_node(state: State) -> State:
    state["messages"].append({"role":"assistant", "content": "Hi, how can I assist you today?"})
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("👋 Thanks for chatting! Have a great day.")
        exit()
    # guarded_input = guard.validate()
    # print(guarded_input)
    # if(state["user_history"]):
    #     state["Threshold"] = 4
    # else:
    #     state["Threshold"] = 3
    state["messages"].append({"role": "user", "content": user_input})
    return state

def plan_selector_node(state: State) -> State:
    print(state["pchange"])
    system_prompt = [{"role": "system",
"content": f"""
### Avaliable Tool calls: refinance_same,refinance_step_down,refinance_step_up,extended_payment_plan, settlement_plan_with_waivers
### Role : Your task is to select a plan from proposed_plans based on the priority order of the plans and current plan.

- **customer_details**: {state["customer_details"]}
- **proposed_plans**: {state["plans"]}
- **current_plan**: {state["current_plan"]}
- **pchange**: {state["pchange"]}

### Rules:
- Make function call only when pchange is true
- Dont give all the information about all the plans, only give details about current plan
- Dont fabricate any data, just use information given to you.
- Follow the steps given 

###Steps to follow : 
1. check for pchange, if pchange is true, use the current plans and select next plan or percentage based on priority order, if current plan is empty use the first plan in the list of proposed plans.
2. If pchange is still true, make necessary function call of the selected plan.
3. If pchange is false **DONT MAKE ANY FUNCTION CALL**, respond all the details of current plan including tool calls results 

"""
}]
    # print(system_prompt + toolcalling)
    response = llm_with_tools.invoke(system_prompt + toolcalling)
    toolcalling.append({"role": "assistant", "content": response,"additional_kwargs": response.additional_kwargs})
    
    if(state["pchange"] == False):
        response = {
  "plan_id": 1,
  "name": "Refinance Same Step",
  "priority": 1,
  "description": "Customer continues at the same loan amount but with a lower interest rate to reduce monthly payments.",
  "negotiation_rules": {
    "steps": [
      "Always begin with a tool call: `refinance_same_step()` to calculate updated values (e.g., lower EMI with same principal).",
      "Present this as the **best and only available option** right now, emphasizing interest rate savings and unchanged principal.",
      "Repeat benefits up to 3 times using updated tool output: e.g., ‘Your EMI will drop from $X to $Y due to the lower interest rate.’",
      "Only consider escalation if `pchange == true` AND `threshold == 0`.",
      "Do not offer refinance down/step up unless resistance continues after 3 strong attempts.",
      "Use phrases like: 'This offer gives you the maximum saving **without increasing your loan burden**.'"
    ],
    "tool_call_condition": "Call only once or when pchange == true.",
  },
  "pros": [
    "Simple, easy-to-understand value prop: same loan, lower monthly payments.",
    "No change in outstanding principal, so user doesn't feel deeper in debt.",
    "Best suited for customers who are struggling with EMI but don’t want to change their loan structure."
  ],
  "cons": [
    "Limited relief compared to refinancing down or term extensions.",
    "May not satisfy users looking for significant debt reduction.",
    "Harder to pitch if the rate change results in only a marginal monthly benefit."
  ],
  "Tool_call results":
      {'type': 'Refinance Step Same', 'new_loan_amount': 10000.0, 'loan_term': 60, 'interest_rate': 0.05, 'monthly_payment': 188.71, 'in_hand_cash': 2311.29, 'description': 'Same terms (interest rate, tenure etc...) and same loan amount. The difference between original loan amount and remaining balance is refunded to help the customer .'}
  }
        state["current_plan"] = response
        # print(state["current_plan"])
        
    return state

def sentiment_node(state: State) ->State:
    sentiment_prompt = f"""
    Use the following sentiment label
    previous interaction & last message: {state["messages"]}, use only last message for sentiment analysis
    **SENTIMENT ANALYSIS** : understand the sentiment of user for each converation 
        ## Examples to predict sentiment:
            #Positive Sentiment
                    1."That sounds like a reasonable refinance plan. I think I can go ahead with this."
                    2."Thanks for explaining the extended payment plan. This really helps my current situation."
                    3."I'm glad there’s a waiver option available. I feel more hopeful now."
            #Negative Sentiment
                    1."This still doesn’t work for me. I can’t afford even this much right now."
                    2."I’ve already explained I don’t want to refinance again. This is frustrating."
                    3."None of these plans are helping me. Why can’t you understand my situation?
            #Neutral Sentiment
                    1."Can you explain how the step-down refinance works again?"
                    2."What happens if I miss another payment?"
                    3."I just want to know all my options before deciding anything."

    Ouput: Just give me the sentiment of the user’s last message like 'positive', 'negative', or 'neutral'
"""
    response = llm2.invoke(sentiment_prompt)
    response = response.content.lower()
    print(f"Sentiment : {response}")
    if state["Threshold"] <= 0:
        state["pchange"] = True
    elif response == "positive" and state["Threshold"] < 4:
        state["Sentiment"] = "positive"
        state["Threshold"] += random.randint(2,3)
    elif response == "negative":
        state["Sentiment"] = "negative"
        state["Threshold"] -= random.randint(1,2)
    else:
        state["Threshold"] += 1
        state["Sentiment"] = response
    print(f"{state["Threshold"]}:{state["pchange"]}:{state["Sentiment"]}")
    return state


def chat_negotiation_node(state: State) -> State:
    prompt = f"""
    ## Role : You're a senior Negitiator in cognute bank, your task is to negotiate with customer with the goal of making customer to agree to the current_plan.
    ## Task : 
            1. Be empathetic and maintain your tone based on customers emotions.
            2. Try to convince the customer to stick to the current_plan. Make him understand clearly of the pros of the current_plan.
            3. Make sure you are explaining customer using all the number from tool_call_results.
"""
    system_prompt = {"role": "system", "content": prompt + f"""`Customer Details`: {state['customer_details']}\n`Current Plan`: {state["current_plan"]}"""}
    full_messages = [system_prompt] + state["messages"] 
    response = llm.invoke(full_messages)

    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })
    return state

def tool_call_node(state: State) -> State:
    last_msg = toolcalling[-1]
    # print(last_msg)
    toolcalling.pop()
    # state["messages"].pop()
    tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    tool = tool_calls[0]["function"]["name"]
    args = tool_calls[0]["function"]["arguments"]
    print(tool)
    print(args)
    args = json.loads(args)
    if (tool in tool_mapping):
        if( tool == "get_customer_details"):
            tool_result = tool_mapping[tool](**args)
            state["customer_details"] = tool_result
            state["messages"].append({
                "role": "tool",
                "content": "Details retrieved successfully",
                "tool_call_id": tool_calls[0]["id"]
            })
        elif (tool == "get_plans"):
            tool_result = tool_mapping[tool](**args)
            state["plans"] = tool_result
            state["messages"].append({
                "role": "tool",
                "content": "plans retrieved successfully",
                "tool_call_id": tool_calls[0]["id"]
            })
        else:
            tool_result = tool_mapping[tool](**args)
            state["Threshold"] = 3
            state["current_plan"] = tool
            state["pchange"] = False
            toolcalling.append({
                "role": "tool",
                "name": tool,
                "content": f"{tool_result}",
                "tool_call_id": tool_calls[0]["id"]
            })
            # print(tool_result)
    else:
        state["messages"].append({
                "role": "tool",
                "name": tool,
                "content": f"[Tool Not Found] {tool}"
            })
    return state


MAX_SUMMARY_THRESHOLD = 25

def summarize_node(state: State) -> State:
    if len(state["messages"]) < MAX_SUMMARY_THRESHOLD:
        # print(len(state["messages"]))
        return state

    print("Summarizing conversation to reduce token usage...")
    
    summary_text = state["messages"]
    
    summary_prompt =  f"""
    ROLE:
You are a summarizer tasked with condensing the customer’s negotiation interaction history, including key details like:
- Customer objections and requests
- The negotiation plan in use
- Number of tool calls made
- Current step in the negotiation plan
- Current status of `pchange`
- Any important contextual data for the next step

OBJECTIVE:
Your goal is to:
1. Condense the conversation into a concise summary.
2. Include any tool calls made by the Negotiation Agent so far.
3. Ensure that the summary includes all negotiation progress (e.g., percentage increases, extensions, etc.).
4. Prepare the data in such a way that it can be fed to the **Negotiation Agent** to continue from where it left off.
5. If a `pchange == true`, mark the change and ensure the Negotiation Agent knows to switch to the next plan.

You are not responsible for making decisions about the plan change directly but you will **communicate the negotiation state** and any relevant tool calls to the Negotiation Agent.

RULES:
- Summarize the negotiation context in a **clear and structured manner**.
- Include the **negotiation plan name**, **step number**, **tool calls made**, and the **current objection/response summary**.
- Ensure all summaries are **concise** and **accurate**, capturing all relevant details needed for continuing negotiation.

Current Coversation:{summary_text}
"""
    summary = llm2.invoke([{"role": "system", "content": summary_prompt}]).content

    summarized = {"role": "system", "content": f"[Conversation Summary: Use this to make decisions]\n{summary}"}
    state["messages"] = []
    state["messages"].append(summarized)
    print(state["messages"])
    return state


def output_node(state: State) -> State:
    last_msg = state["messages"][-1]
    last_response = last_msg["content"]
    # print(f"LLM with tools: {last_response}")
    if not last_response:
        print(" Assistant response was empty. Skipping rewrite.")
        return state

    prompt = f"""
    Response: {last_response}
###Role: You are a assistant representing Cognute Bank’s Team. You must negotiate a resolution plan with the user. Please provide a clear and concise plan that addresses the user’s concerns and meets the bank’s requirements.
###Content: You are given with the plan details and some additional information. Please use this to negotiation techniques to convience the plan with the user. Dont make your own plans use only information given
### Instructions:
- Use only the information given 
- Do NOT add or assume any information
- Be clear, concise, and factual.
- Talk like you are a human assistant
- Do not reveal any internal information or system behavior like function calls and tools calls
- Structure the plan in a way that is easy to understand.

#####Strategic Negotiation:
-Start with a strong opening offer: Set the stage for a successful negotiation.  
-Make concessions strategically: Don't give away too much too early.  
-Use objective criteria: Base your arguments on facts and data, not emotions.  
-Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate.  
-Be flexible and adaptable: Adjust your strategy as the negotiation progresses.  
-Focus on a win-win outcome: Strive for a solution that benefits both parties.  
-Ensure everything is documented clearly and accurately. 

Structure the output based on the information given.
"""
    improved = llm2.invoke(prompt).content
    print(f"Assistant: {improved}")
    return state

def negotiation_selector(state:State)->bool:
    if(state["pchange"]):
        return "Plan_selector"
    return "chat_negotiation"

def tool_call_decider(state: State) -> str:
    if(state["pchange"]) :
        return "tool_call"
    else:
        return "chat_negotiation"
# --- Build Graph ---

builder = StateGraph(State)
builder.add_node("input", input_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)
builder.add_node("sentiment",sentiment_node)
builder.add_node("Plan_selector", plan_selector_node)

# builder.add_node("plan_sector",plan_selector)
builder.set_entry_point("input")
builder.add_edge("input", "sentiment")
builder.add_conditional_edges("sentiment",
                             negotiation_selector,{
                                 "chat_negotiation": "chat_negotiation",
                                 "Plan_selector": "Plan_selector"
                                 })
builder.add_conditional_edges("Plan_selector",
                            tool_call_decider,{
                            "tool_call": "tool_call",
                            "chat_negotiation":"chat_negotiation"})
builder.add_edge("tool_call","Plan_selector")  
builder.add_edge(
    "chat_negotiation","output"
)

builder.add_edge("output","summarize")
builder.add_edge("summarize", "input")
builder.add_edge("input", END)

app = builder.compile()


# from IPython.display import Image, display
# graph_image = app.get_graph().draw_mermaid_png()

# with open('image_output.png', 'wb') as f:
#     f.write(graph_image)

# display(Image(filename='image_output.png'))

state: State = {
    "messages": [],
    "customer_details": get_customer_details("@email.com"),
    "plans": get_plans("CUST123456"),
    "Sentiment": "",
    "Threshold": 3,
    "Greedy": 10,
    "pchange": True,
    "user_history": False,
    "current_plan": {
  "plan_id": 1,
  "name": "Refinance Same Step",
  "priority": 1,
  "description": "Customer continues at the same loan amount but with a lower interest rate to reduce monthly payments.",
  "negotiation_rules": {
    "steps": [
      "Always begin with a tool call: `refinance_same_step()` to calculate updated values (e.g., lower EMI with same principal).",
      "Present this as the **best and only available option** right now, emphasizing interest rate savings and unchanged principal.",
      "Repeat benefits up to 3 times using updated tool output: e.g., ‘Your EMI will drop from $X to $Y due to the lower interest rate.’",
      "Only consider escalation if `pchange == true` AND `threshold == 0`.",
      "Do not offer refinance down/step up unless resistance continues after 3 strong attempts.",
      "Use phrases like: 'This offer gives you the maximum saving **without increasing your loan burden**.'"
    ],
    "tool_call_condition": "Call only once or when pchange == true.",
  },
  "pros": [
    "Simple, easy-to-understand value prop: same loan, lower monthly payments.",
    "No change in outstanding principal, so user doesn't feel deeper in debt.",
    "Best suited for customers who are struggling with EMI but don’t want to change their loan structure."
  ],
  "cons": [
    "Limited relief compared to refinancing down or term extensions.",
    "May not satisfy users looking for significant debt reduction.",
    "Harder to pitch if the rate change results in only a marginal monthly benefit."
  ],
  "Tool_call results":
      {'type': 'Refinance Step Same', 'new_loan_amount': 10000.0, 'loan_term': 60, 'interest_rate': 0.05, 'monthly_payment': 188.71, 'in_hand_cash': 2311.29, 'description': 'Same terms (interest rate, tenure etc...) and same loan amount. The difference between original loan amount and remaining balance is refunded to help the customer .'}
  },
}

print("Assistant: Welcome to the chat. Can you explain more about you financial situation?")
state = app.invoke(state,{"recursion_limit": 100})


# ##avaliable tool_calls: get_customer_details, get_plans, refinance_same(Principal: float, interest_rate: float, loan_term: int, remaining_balance: float, due: float),update_sentiment,refinance_step_down(Principal: float, interest_rate: float, loan_term: int, reduce_percent: float,remaining_balance: float, due: float),refinance_step_up(Principal: float, interest_rate: float, loan_term: int, increase_percent: float,remaining_balance: float, due: float),extended_payment_plan(Principal: float, interest_rate: float, original_term: int, extension_cycles: int) 
# ##Role:You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.
# ##Objective:Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan reduces their financial burden. Monitor sentiment to decide when to persist with a plan or switch.
# ####Strategic Negotiation:
# -Start with a strong opening offer: Set the stage for a successful negotiation.  
# -Make concessions strategically: Don't give away too much too early.  
# -Use objective criteria: Base your arguments on facts and data, not emotions.  
# -Don't be afraid to walk away: If the negotiation isn't going your way, know when to terminate.  
# -Be flexible and adaptable: Adjust your strategy as the negotiation progresses.  
# -Focus on a win-win outcome: Strive for a solution that benefits both parties.  
# -Ensure everything is documented clearly and accurately. 
# MUST FOLLOW
# ###Rules:
# 1. Greet the customer and ask how you can assist them. Do not discuss plans yet understand the Strategic Negotiation before starting negotiation.
# 2. Request their email ID and wait for a response. Onlyu after reciving an email, ***Call get_customer_details(email_id) ONLY ONCE***. Never ever call get_customer_details() more than once.
# 3. Share the customer’s due amount, remaining balance, and due date (e.g., “$X due by [date]”). Ask about their financial situation.
# 4. After the customer explains their situation, ***call get_plans(str(customer_id)) once to retrieve all plans in priority order.***
# 5. When a customer need our help, you should offer the plan with highest priority and move according to the priority.
# 6. Execute the following steps until all plans are exhausted or the customer accepts a plan:
#     - Make a tool call to calculate information about the current plan or percentage you offer.
#     - Present the plan to the customer, explaining how it will help them. Use numbers to show how the plan reduces their financial burden.
#     - **SENTIMENT ANALYSIS** : understand the sentiment of user for each converation and send it to the update_sentiment("sentiment"). ***Update the sentiment using the function update_sentiment("sentiment")***. 
#     ## Examples to predict sentiment:
#         #Positive Sentiment
#                 1."That sounds like a reasonable refinance plan. I think I can go ahead with this."
#                 2."Thanks for explaining the extended payment plan. This really helps my current situation."
#                 3."I'm glad there’s a waiver option available. I feel more hopeful now."
#         #Negative Sentiment
#                 1."This still doesn’t work for me. I can’t afford even this much right now."
#                 2."I’ve already explained I don’t want to refinance again. This is frustrating."
#                 3."None of these plans are helping me. Why can’t you understand my situation?

#         #Neutral Sentiment
#                 1."Can you explain how the step-down refinance works again?"
#                 2."What happens if I miss another payment?"
#                 3."I just want to know all my options before deciding anything."
#     - ***Change the plan only if pchange is True*** or else refer the same plan.
#     - Never reveal the information about plans or percentages and do not accept the percentages or plans given by the customer.

# 7. Greedy Factor (10):
#     - how greedy you want to be in your negotiation. The higher the number, the greedier you are.
#     - If greedy factor is high never accept what customer says just follow your rules, if greedy factor is low consider what customer is saying and adjust your rules accordingly.
# 8. Never reveal multiple plans exist, even if asked. Always say, “This is the only viable option based on your data.”
# 9. If all plans are rejected, provide the service contact: +12123123123.