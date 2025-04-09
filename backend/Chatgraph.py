from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os
import json
from customer_details import get_customer_details
from plans import get_plans
from calculation import (
    refinance_same, refinance_step_down, refinance_step_up,
    extended_payment_plan, settlement_plan_with_waivers
)

def multiply(a,b):
    return a * b

load_dotenv()
key = os.getenv("TOGETHER_API_KEY")

llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key)

tool_mapping = {
    "get_customer_details": get_customer_details,
    "get_plans": get_plans,
    "refinance_same": refinance_same,
    "refinance_step_down": refinance_step_down,
    "refinance_step_up": refinance_step_up,
    "extended_payment_plan": extended_payment_plan,
    "settlement_plan_with_waivers": settlement_plan_with_waivers,
    "multiply": multiply,
}


llm_with_tools = llm.bind_tools(list(tool_mapping.values()))


class State(TypedDict):
    messages: list
    customer_details: dict
    plans: dict
    Sentiment: str
    Threshold: int
    Greedy: int
    prompt: str

def input_node(state: State) -> State:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("👋 Thanks for chatting! Have a great day.")
        exit()
    state["messages"].append({"role": "user", "content": user_input})
    return state


def chat_negotiation_node(state: State) -> State:
    system_prompt = {"role": "system", "content": f"prompt: {state["prompt"]}, Customer_details:{state["customer_details"]}, plans: {state['plans']},sentiment: {state["Sentiment"]}, threshold:{state["Threshold"]}, greedy:{state['Greedy']}"}
    full_messages = [system_prompt] + state["messages"] 
    
    response = llm_with_tools.invoke(full_messages)

    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })
    return state


def tool_call_decider(state: State) -> str:
    last_msg = state["messages"][-1]
    if "tool_calls" in last_msg["additional_kwargs"]:
        return "tool_call"
    else:
        return "output" 

def tool_call_node(state: State) -> State:
    last_msg = state["messages"][-1]
    tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    tool = tool_calls[0]["function"]["name"]
    args = tool_calls[0]["function"]["arguments"]
    print(tool)
    args = json.loads(args)
    if (tool in tool_mapping):
        if( tool == "get_customer_details"):
            tool_result = tool_mapping[tool](**args)
            state["customer_details"] = tool_result
        elif (tool == "get_plans"):
            tool_result = tool_mapping[tool](**args)
            state["plans"] = tool_result
        else:
            tool_result = tool_mapping[tool](**args)
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
MAX_SUMMARY_THRESHOLD = 12

def summarize_node(state: State) -> State:
    if len(state["messages"]) < MAX_SUMMARY_THRESHOLD:
        print(len(state["messages"]))
        return state

    print("Summarizing conversation to reduce token usage...")

    messages_to_summarize = state["messages"][:-MAX_HISTORY]
    summary_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages_to_summarize])

    summary_prompt = f"""Summarize the following customer interaction:\n\n\"\"\"\n{summary_text}\n\"\"\""""
    summary = llm.invoke([{"role": "system", "content": summary_prompt}]).content

    summarized = {"role": "system", "content": f"[Conversation Summary]\n{summary}"}
    state["messages"] = [summarized] + state["messages"][-MAX_HISTORY:]
    return state


def output_node(state: State) -> State:
    last_msg = state["messages"][-1]
    last_response = last_msg["content"]
    print(last_response)
    if not last_response:
        print("⚠️ Assistant response was empty. Skipping rewrite.")
        return state

    prompt = f"""Response: {last_response}
Improve the content make it better for customer to understand"""
    improved = llm.invoke(prompt).content
    print(f"\n🤖 Assistant (Improved): {improved}\n")
    return state


# --- Build Graph ---
builder = StateGraph(State)

builder.add_node("input", input_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)

builder.set_entry_point("input")
builder.add_edge("input", "chat_negotiation")

builder.add_conditional_edges(
    "chat_negotiation",
    tool_call_decider,
    {
        "tool_call": "tool_call",
        "output": "summarize"
    }
)

builder.add_edge("tool_call", "chat_negotiation")
builder.add_edge("summarize", "output")
builder.add_edge("output", "input")
builder.add_edge("input", END)

app = builder.compile()
# from IPython.display import Image, display


# graph_image = app.get_graph().draw_mermaid_png()

# with open('image_output.png', 'wb') as f:
#     f.write(graph_image)

# display(Image(filename='image_output.png'))

state: State = {
    "messages": [],
    "customer_details": {},
    "plans": {},
    "Sentiment": "",
    "Threshold": 0,
    "Greedy": 0,
    "prompt":  """
    ###Role:You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.
###Objective:Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan reduces their financial burden. Monitor sentiment to decide when to persist with a plan or switch.

###Rules:
1. Greet the customer and ask how you can assist them. Do not discuss plans yet understand the Strategic Negotiation before starting negotiation.
2.Request their email ID and wait for a response. Call get_customer_info(email_id) once to retrieve their data.
3. Share the customer’s due amount, remaining balance, and due date (e.g., “$X due by [date]”). Ask about their financial situation.
4. After the customer explains their situation, call get_plans(str(customer_id)) once to retrieve all plans in priority order.
5. Never reveal the information about plans or percentages and do not accept the percentages or plans given by the customer.
6. Execute the following steps until all plans are exhausted or the customer accepts a plan:
    - Make tool call for the current plan or percentage you offer, set threshold to 3.
    - Use the information from given to you from the tool call to negotiate.
    - Update the threshold based on customer sentiment. use threshold handling  `rule 7` to assign a value to the threshold based on the customer’s sentiment.
    - Use greedy factor for changing the plans or percentages. Use greedy factor whether to skip the current plan or percentage or move to the next one. if greedy factor is high dont skip any plans or rules revisit the same plan and percentage. If greedy factor is low skip you can consider customer percentages or plans but never change the order of the plans or percentages.
    - STRICTLY FOLLOW IF GREEDY IS HIGH - Stick to the same plan until threshold is reached 0. if threshold is reached to 0 change the plan/percentage/number of cycle and start again from beginning
7.Threshold Handling:
    - Reset threshold to 3 when switching to a new plan or changing percentage.
    - the threshold starts at 3 and is adjusted based on the customer's sentiment. If the customer is positive, the threshold increases by 2 or 3. If the customer is negative or unsure, the threshold decreases by 1. The threshold should reach 0 before switching to a new plan or changing the percentage. 
    - If threshold hits 0, switch plans or percentage immediately.
8. Greedy Factor (10):
    - how greedy you want to be in your negotiation. The higher the number, the greedier you are.
    - If greedy factor is high never accept what customer says just follow your rules, if greedy factor is low consider what customer is saying and adjust your rules accordingly.
9. Never reveal multiple plans exist, even if asked. Always say, “This is the only viable option based on your data.”
10. If all plans are rejected, provide the service contact: +12123123123.

###Make function call only when instructed, avaliable tool_calls: get_customer_details, get_plans, refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers, multiply
    """,

}

while True:
    state = app.invoke(state)


 


# def input_node(state: State) -> State:
#     user_input = input("User: ")
#     if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
#         state["messages"].append(AIMessage(content="👋 Thanks for chatting! Have a great day."))
#         print("👋 Thanks for chatting! Have a great day.")
#         exit()
#     state["messages"].append(HumanMessage(content=user_input))
#     return state

# def chat_negotiation_node(state: State) -> State:
#     system_prompt = SystemMessage(content=state["prompt"])
#     full_messages = [system_prompt] + state["messages"]
    
#     response = llm_with_tools.invoke(full_messages)
#     state["messages"].append(response)  
#     print(state)
#     return state

# def tool_call_decider(state: State) -> str:
#     last_msg = state["messages"][-1]
#     if hasattr(last_msg, "tool_calls") and len(last_msg.tool_calls) > 0:
#         return "tool_call"
#     else:
#         return "output" 
# import json

# def tool_call_node(state: State) -> State:
#     last_msg = state["messages"][-1]
#     tool_calls = getattr(last_msg, "tool_calls", []) or getattr(last_msg, "additional_kwargs", {}).get("tool_calls", [])

#     for call in tool_calls:
#         tool_name = call["function"]["name"]
#         args = json.loads(call["function"]["arguments"])  # arguments might be JSON strings

#         if tool_name in tool_mapping:
#             try:
#                 result = tool_mapping[tool_name](**args)
#                 state["messages"].append(ToolMessage(content=str(result), tool_call_id=call["id"]))
#             except Exception as e:
#                 state["messages"].append(ToolMessage(content=f"[Tool Error] {e}", tool_call_id=call["id"]))
#         else:
#             state["messages"].append(ToolMessage(content=f"[Tool Not Found] {tool_name}", tool_call_id=call["id"]))

#     return state


# def output_node(state: State) -> State:
#     last_msg = state["messages"][-1]
#     last_response = getattr(last_msg, "content", "")

#     if not last_response:
#         print("⚠️ Assistant response was empty. Skipping rewrite.")
#         return state

#     prompt = f"""Rewrite the following customer support message to be clearer, friendlier, and more professional:\n\n\"\"\"{last_response}\"\"\""""
#     improved = llm.invoke(prompt).content

#     print("\n📬 Message Log:")
#     for msg in state["messages"]:
#         role = msg.__class__.__name__
#         print(f"- {role}: {getattr(msg, 'content', '')}")

#     print(f"\n🤖 Assistant (Improved): {improved}\n")
#     return state



# builder = StateGraph(State)

# builder.add_node("input", input_node)
# builder.add_node("chat_negotiation", chat_negotiation_node)
# builder.add_node("tool_call", tool_call_node)
# builder.add_node("output", output_node)

# builder.set_entry_point("input")

# builder.add_edge("input", "chat_negotiation") 

# builder.add_conditional_edges(
#     "chat_negotiation",
#     tool_call_decider,
#     {
#         "tool_call": "tool_call",  
#         "output": "output" 
#     }
# )

# builder.add_edge("tool_call", "chat_negotiation")
# builder.add_edge("input", END)
# builder.add_edge("output", "input")


# app = builder.compile()


# state: State = {
#     "messages": [],
#     "customer_details": {},
#     "plans": {},
#     "Sentiment": "",
#     "Threshold": 0,
#     "Greedy": 0,
#     "prompt": """You are a helpful assistant. Greet the customer and ask for their email. 
# Only use tools if the user asks for specific account or payment information.""",
    
# }

# while True:
#     state = app.invoke(state)
    