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

class State(TypedDict):
    messages: list
    customer_details: dict
    plans: dict
    Sentiment: str
    Threshold: int
    Greedy: int
    pchange: bool
    user_history : bool




llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key)

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

def sentiment_node(state: State) ->State:
    sentiment_prompt = f"""
    Use the following sentiment label
    previous interaction & last message: {state["messages"]}
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
    response = llm.invoke(sentiment_prompt)
    response = response.content.lower()
    # print(response)
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
    print(f"{state["Threshold"]}:{state["pchange"]}:{state["Sentiment"]}")
    return state


def chat_negotiation_node(state: State) -> State:
    prompt = f"""
##Avaliable tool_calls: refinance_same,refinance_step_down,refinance_step_up,extended_payment_plan
###Role:You are a Customer Service Representative for Cognute Bank, responsible for selecting a plan based on the customer's financial situation.
####Instruction: You need to change the plan or percentage only if pchange is True, or else you need to stay with the same plan or percentage
###Objective: Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan reduces their financial burden.Use pchange to change plan or percentage 

pchange: {state["pchange"]}
####Rules:
1. Share the customer’s due amount, remaining balance, and due date (e.g., “$X due by [date]”). Ask about their financial situation.
2. Select the plan based on the priority and greedy factor, make necessary tool call before presenting the plan to the customer.
3. Never reveal the information about plans or percentages and do not accept the percentages or plans given by the customer.
4. You must state on the same plan until pchange is true
     - Present the plan to the customer, explaining how it will help them. Use numbers to show how the plan reduces their financial burden.
     - Never reveal the information about other plans or percentages and do not accept the percentages or plans given by the customer.
5. Greedy Factor (10):
    - how greedy you want to be in your negotiation. The higher the number, the greedier you are.
    - If greedy factor is high never accept what customer says just follow your rules, if greedy factor is low consider what customer is saying and adjust your rules accordingly.
6. Never reveal multiple plans exist, even if asked. Always say, “This is the only viable option based on your data.”
7. If all plans are rejected, provide the service contact: +12123123123.

Output: Your response must be short, covering all the necessary information, you will iterate over the same plan for few time so dont give out all the information at once.
"""
    system_prompt = {"role": "system", "content": prompt + f"""Customer Details: {state['customer_details']}\nPlans: {state["plans"]}\n"""}
    full_messages = [system_prompt] + state["messages"] 
    # print(full_messages)
    response = llm_with_tools.invoke(full_messages)

    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })
    return state
# def plan_selector(state:State)->State:
#     prompt = ""
#     return state

def tool_call_decider(state: State) -> str:
    last_msg = state["messages"][-1]
    if "tool_calls" in last_msg["additional_kwargs"]:
        return "tool_call"
    else:
        return "output" 

def tool_call_node(state: State) -> State:
    last_msg = state["messages"][-1]
    state["messages"].pop()
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
            state["pchange"] = False
            state["messages"].append({
                "role": "tool",
                "name": tool,
                "content": f"{tool_result}",
                "tool_call_id": tool_calls[0]["id"]
            })
        
    else:
        state["messages"].append({
                "role": "tool",
                "name": tool,
                "content": f"[Tool Not Found] {tool}"
            })
    return state

MAX_HISTORY = 6
MAX_SUMMARY_THRESHOLD = 6

def summarize_node(state: State) -> State:
    if len(state["messages"]) < MAX_SUMMARY_THRESHOLD:
        # print(len(state["messages"]))
        return state

    print("Summarizing conversation to reduce token usage...")
    
    summary_text = state["messages"]
    
    summary_prompt =  f"""

###Role: You are a summarization assistant for Cognute Bank’s Recovery Solutions Team. Based on the provided conversation history, create a structured summary that includes:

###MUST INCLUDE
High-Level Overview – Briefly explain the overall state and goal of the conversation.
Chronological Summary – List the key exchanges between assistant, user, and tool in order.
Tool Calls – Mention if any tools were used and what was retrieved.
Plan Negotiation – Mention if there was any negotiation or discussion about a resolution plan.
Current State – Clearly indicate what stage the conversation is at and what the next agent should do.

###Instructions:
- Use only the information in the conversation.
- Do NOT add or assume any information.
- Do NOT include references to internal tools, functions, or system behavior .
- Be clear, concise, and factual.
\n
Current Coversation:{summary_text}
"""
    summary = llm.invoke([{"role": "system", "content": summary_prompt}]).content

    summarized = {"role": "system", "content": f"[Conversation Summary: Use this to make decisions]\n{summary}"}
    state["messages"] = []
    state["messages"].append(summarized)
    print(state["messages"])
    return state


def output_node(state: State) -> State:
    last_msg = state["messages"][-1]
    last_response = last_msg["content"]
    print(f"LLM with tools: {last_response}")
    if not last_response:
        print(" Assistant response was empty. Skipping rewrite.")
        return state

    prompt = f"""
    Response: {last_response}
###Role: You are a assistant representing Cognute Bank’s Team. You must negotiate a resolution plan with the user. Please provide a clear and concise plan that addresses the user’s concerns and meets the bank’s requirements.
###Content: You are given with the plan details and some additional information. Please use this to negotiation techniques to convience the plan with the user.
### Instructions:
- Use only the information given 
- Do NOT add or assume any information
- Be clear, concise, and factual.
- Talk like you are a human assistant
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
    improved = llm.invoke(prompt).content
    print(f"Assistant: {improved}")
    return state


# --- Build Graph ---
builder = StateGraph(State)

builder.add_node("input", input_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)
builder.add_node("sentiment",sentiment_node)
# builder.add_node("plan_sector",plan_selector)
builder.set_entry_point("input")
builder.add_edge("input", "sentiment")
builder.add_edge("sentiment", "chat_negotiation")

builder.add_conditional_edges(
    "chat_negotiation",
    tool_call_decider,
    {
        "tool_call": "tool_call",
        "output": "output"
    }
)

builder.add_edge("tool_call", "chat_negotiation")
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
    "Greedy": 0,
    "pchange": False,
    "user_history": False,
}

print("Assistant: Welcome to the chat. How can I assist you today?")
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