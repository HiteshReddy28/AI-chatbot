from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os, json, decimal
from rails import enforce_input_guardrails, enforce_output_guardrails
from calculation import (
    refinance_same, refinance_step_down, refinance_step_up,
    extended_payment_plan, settlement_plan_with_waivers
)
from Shared import get_client_details, get_plans

# Load API key
load_dotenv()
key = os.getenv("TOGETHER_API_KEY_1")

# Define model
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key)

tool_mapping = {
    "get_client_details": get_client_details,
    "get_plans": get_plans,
    "refinance_same": refinance_same,
    "refinance_step_down": refinance_step_down,
    "refinance_step_up": refinance_step_up,
    "extended_payment_plan": extended_payment_plan,
    "settlement_plan_with_waivers": settlement_plan_with_waivers
}

llm_with_tools = llm.bind_tools(list(tool_mapping.values()))

class State(TypedDict):
    messages: list
    customer_details: dict
    plans: dict
    Sentiment: str
    Threshold: int
    Greedy: int
    pchange: bool
    user_history: bool
    priority: int

def input_node(state: State) -> State:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Thanks for chatting! Goodbye.")
        state["end_conversation"] = True
        return state
    state["messages"].append({"role": "user", "content": user_input})
    return state

def input_guardrails_node(state: State) -> State:
    user_msg = state["messages"][-1]["content"]
    violated, warning = enforce_input_guardrails(user_msg)
    if violated:
        print("\nInput Violation(s):")
        for v in warning["violations"]:
            print(f" - {v['message']}")
        state["messages"].append({
            "role": "system",
            "content": f"<Violation> {'; '.join([v['message'] for v in warning['violations']])} </Violation>"
        })
    return state

def sentiment_threshold_node(state: State) -> State:
    last_msg = state["messages"][-1]["content"]
    prompt = """
    Analyze sentiment and assign threshold:
    Positive → 5
    Unsure → 4
    Negative → 2
    Assertive → 1
    Format: <sentiment>...</sentiment><threshold>...</threshold>
    """
    response = llm.invoke([
        {"role": "system", "content": prompt},
        {"role": "user", "content": last_msg}
    ]).content

    try:
        sentiment = response.split("<sentiment>")[1].split("</sentiment>")[0].strip()
        threshold = int(response.split("<threshold>")[1].split("</threshold>")[0].strip())
    except Exception:
        sentiment, threshold = "unsure", 3

    state["Sentiment"] = sentiment
    state["Threshold"] = threshold
    return state

def chat_negotiation_node(state: State) -> State:
    if not state.get("customer_details") and state["messages"][-1]["content"].isdigit():
        cid = state["messages"][-1]["content"]
        state["customer_details"] = get_client_details(client_id=cid)
        state["messages"].append({"role": "system", "content": f"[Client details retrieved for {cid}]"})

    negotiation_prompt = f"""
<system>
You're a professional assistant for Cognute Bank.
Strictly follow these rules:
- Only suggest one verified plan at a time.
- Use get_plans and appropriate refinance_* functions.
- Never guess or mention internal tools.
- Do not suggest alternatives until threshold is exceeded.
</system>
Customer Details: {state["customer_details"]}
Plans: {state.get("plans", {})}
"""
    response = llm_with_tools.invoke([{"role": "system", "content": negotiation_prompt}] + state["messages"])

    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })

    return state

def output_guardrails_node(state: State) -> State:
    last = state["messages"][-1]["content"]
    violated, warning = enforce_output_guardrails(last)
    if violated:
        print("Output Guardrails Triggered:")
        for v in warning["violations"]:
            print(f" - {v['message']}")
        state["messages"].append({
            "role": "system",
            "content": f"<Violation> {'; '.join([v['message'] for v in warning['violations']])} </Violation>"
        })
    return state

def tool_call_decider(state: State) -> str:
    if "tool_calls" in state["messages"][-1].get("additional_kwargs", {}):
        return "tool_call"
    return "output"

def tool_call_node(state: State) -> State:
    last_msg = state["messages"].pop()
    call = last_msg["additional_kwargs"]["tool_calls"][0]
    tool = call["function"]["name"]
    args = json.loads(call["function"]["arguments"])
    result = tool_mapping[tool](**args)

    if tool == "get_client_details":
        state["customer_details"] = result
    elif tool == "get_plans":
        state["plans"] = result
        state["priority"] = state.get("priority", 1)
        if isinstance(result, dict):
            key = list(result.keys())[0]
            plan = result[key]
            func = plan.get("function")
            inputs = plan.get("inputs", {})
            if func in tool_mapping:
                calc = tool_mapping[func](**inputs)
                state["messages"].append({"role": "tool", "name": func, "content": f"{calc}"})

    state["messages"].append({
        "role": "tool",
        "name": tool,
        "content": f"{result}",
        "tool_call_id": call["id"]
    })
    return state

def summarize_node(state: State) -> State:
    if len(state["messages"]) < 10:
        return state
    summary = llm.invoke([{
        "role": "system",
        "content": f"""Summarize clearly this conversation:\n{state["messages"]}"""
    }]).content
    state["messages"] = [{"role": "system", "content": f"[Summary]\n{summary}"}]
    return state

def output_node(state: State) -> State:
    print("Assistant:", state["messages"][-1]["content"])
    return state

# Graph Construction
builder = StateGraph(State)
builder.set_entry_point("input")

builder.add_node("input", input_node)
builder.add_node("input_guardrails", input_guardrails_node)
builder.add_node("sentiment_threshold", sentiment_threshold_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("output_guardrails", output_guardrails_node)
builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)

builder.add_edge("input", "input_guardrails")
builder.add_edge("input_guardrails", "sentiment_threshold")
builder.add_edge("sentiment_threshold", "chat_negotiation")
builder.add_conditional_edges("chat_negotiation", tool_call_decider, {
    "tool_call": "tool_call",
    "output": "output_guardrails"
})
builder.add_edge("tool_call", "chat_negotiation")
builder.add_edge("output_guardrails", "summarize")
builder.add_edge("summarize", "output")
builder.add_edge("output", "input")
builder.add_edge("input", END)

app = builder.compile()

# Initial State
state: State = {
    "messages": [],
    "customer_details": {},
    "plans": {},
    "Sentiment": "",
    "Threshold": 3,
    "Greedy": 10,
    "pchange": False,
    "user_history": False,
    "priority": 1
}

# Run
print("Assistant: Hello! Welcome to Cognute Bank. Please provide your Client ID to begin.")
while True:
    state = app.invoke(state, config={"recursion_limit": 100})
    if state.get("end_conversation"):
        break
