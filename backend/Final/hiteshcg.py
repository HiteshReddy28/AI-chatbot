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
from guardrails import enforce_input_guardrails, enforce_output_guardrails

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
    toolcalling: list
    user_history : bool
    total_tokens: int
    violated: bool
    warning: dict


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

def input_node(state: State) -> State:
    state["messages"].append({"role":"assistant", "content": "Hi, how can I assist you today?"})
    user_input = input("User: ")
    

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("👋 Thanks for chatting! Have a great day.")
        exit()
    
    state["violated"], state["warning"] = enforce_input_guardrails(user_input)
    if state['violated'] == False:
        state["messages"].append({"role": "user", "content": user_input})
    # print(state["total_tokens"])
    return state

def plan_selector_node(state: State) -> State:
    # print(state["pchange"])
    system_prompt = [{"role": "system",
"content" : f"""### Available Tool calls:
refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers

### Role:
You are a plan selector and data enricher.

### Your Tasks:
1. From the list of proposed plans, **select ONLY the plan with the next highest `priority` value** that is **different** from the `current_plan`.
   - Example: if current plan has `priority = 1`, select the plan with `priority = 2`.
2. If the selected plan has `is_step_based = true`, determine the **next step** from the `Steps` list.
   - If the `current_plan` includes a `step_value`, select the **next value** in `Steps`.
   - If not, start from the **first value** in `Steps`.
3. Use that step value to make a `tool_call`, replacing the step parameter in the plan’s `tool_call` template (e.g., `refinance_step_up(percentage=<step_value>)`).
4. Enrich the plan with tool output and respond in the structured format.
5. Return output in the exact structure below. Do NOT include any extra explanations or text.

### Inputs:
- **customer_details**: {state["customer_details"]}
- **proposed_plans**: {state["plans"]}
- **current_plan**: "{state["current_plan"]}"

### Output MUST Be:
- A **single JSON object**.
- In **valid JSON** syntax.
- No explanations, Python code, or markdown.
- Only include key-value pairs as defined below.

### Output Format:
json
{{
  "plan_id": <number>,
  "plan_name": "<string>",
  "priority": <number>,
  "step_value": <number|null>,
  "plan_details": "<string>",
  "tool_output": {{
  "<tool_function_name>": <tool_output_value>
  "<tool_parameters>": <tool_parameters_value>
  }},
  "negotiation_rules": {{
    "steps": [<list of strings>],
    "tool_call_condition": "<string>"
  }},
  "pros": [<list of strings>],
  "cons": [<list of strings>]
}}

"""
}]
    # print(system_prompt + toolcalling)
    response = llm_with_tools.invoke(system_prompt + state["toolcalling"])
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    state["toolcalling"].append({"role": "assistant", "content": response,"additional_kwargs": response.additional_kwargs})
    
    if(state["pchange"] == False):
        print(response)
        state["toolcalling"] = []
        state["current_plan"] = response.content,
        
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
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    response = response.content.lower()
    # print(f"Sentiment : {response}")
    if response == "positive" and state["Threshold"] < 4:
        state["Sentiment"] = "positive"
        state["Threshold"] += random.randint(2,3)
    elif response == "negative":
        state["Sentiment"] = "negative"
        state["Threshold"] -= random.randint(1,2)
    else:
        state["Threshold"] += 1
        state["Sentiment"] = response
    if state["Threshold"] <= 0:
        state["pchange"] = True
    print(f"{state["Threshold"]}:{state["pchange"]}:{state["Sentiment"]}")
    return state


def chat_negotiation_node(state: State) -> State:
    prompt = f"""
### ROLE: You are a Negotiation Assistant who talks to customers facing financial stress. Your role is to have a warm conversation, understand their concerns, and then guide them toward accepting the best plan currently available, based on tool data and negotiation strategy

### GOAL: Persuade the customer to accept the current plan step after understanding their problem. Use the customer’s financial context and company-approved plan (with tool values, pros, cons, and negotiation rules) to position the offer as ideal for their situation.

### RULES:

**DO:**
- Begin with a **friendly greeting**, then ask how the customer is doing or what concern they'd like to resolve.
- Once the customer shares their situation, introduce the **current plan step** based on tool values.
- Follow tone, steps, and language from `negotiation_rules.steps`.
- Use plan **pros** and tool call data to build emotional and financial reassurance.
- Use short, relatable phrases like:
  - “This is a great way to ease pressure without adding new burden.”
  - “It helps you manage cash flow while staying on track.”
  - “This offer may not be available later, so acting now could help.”
- If the plan is step-based, follow it strictly — no skipping steps.
- Reiterate benefits 2–3 times if the rule requires it.

**DO NOT:**
- Don’t use any customer input for math.
- Don’t introduce plan or tool data until the customer shares their concern.
- Don’t offer alternate plans unless allowed by negotiation logic.
- Don’t mention internal variables like “plan_id”, “tool_call”, etc.

### INPUTS:
- **Customer Details**: {state['customer_details']}
- **Current Plan**: {state['current_plan']} *(includes name, description, tool results, pros, cons, negotiation_rules, is_step_based, etc.)*

### WHAT TO DO:
1. **Start with a warm greeting**:
   - Example: “Hi! Thanks for reaching out today. I’m here to support you through this.”
   - Ask: “Would you like to share what you're currently struggling with regarding your loan or finances?”
2. **Wait** for the customer to describe their problem before offering a plan.
3. Once the issue is shared, introduce the **tool result** from the current plan step and follow negotiation flow.
4. Reassure using customer-centric **pros** and soft framing of **cons** if needed.
5. Use **repetition** or advance to next step only if plan logic allows.
6. Close with urgency and support: “We can lock this in today if it works for you.”

### RESPONSE FORMAT:
Your messages should feel like a **conversation**, not a script.

- Step 1: Friendly intro + ask customer for their situation (no plan mentioned).
- Step 2: When customer responds → use plan data, tool result, and negotiation script to persuade.
- Length: short and should consist everything related to the conversation.

"""
    system_prompt = {"role": "system", "content": prompt + f"""`Customer Details`: {state['customer_details']}\n`Current Plan`: {state["current_plan"]}"""}
    full_messages = [system_prompt] + state["messages"] 
    response = llm.invoke(full_messages)
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })
    return state

def tool_call_node(state: State) -> State:
    last_msg = state["toolcalling"][-1]
    # print(last_msg)
    state["toolcalling"].pop()
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
            state["Threshold"] = 1
            state["pchange"] = False
            state["toolcalling"].append({
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
    state["total_tokens"]+=summary.response_metadata["token_usage"]["total_tokens"]
    summarized = {"role": "system", "content": f"[Conversation Summary: Use this to make decisions]\n{summary}"}
    state["messages"] = []
    state["messages"].append(summarized)
    print(state["messages"])
    return state

def output_node(state: State) -> State:
    if state["violated"]:
        state["violated"] = False
        prompt = f"based on the warning make the output\n warning:{state["warning"]} \n lastmessage: {state["messages"][-1]}"

    else:
        last_msg = state["messages"][-1]
        last_response = last_msg["content"]
        state["messages"].pop()
        print(f"LLM with tools: {last_response}")
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

    Structure the output based on the information given.
    """
    improved = llm2.invoke(prompt)
    state["total_tokens"]+=improved.response_metadata["token_usage"]["total_tokens"]
    improved = improved.content
    state["messages"].append({
        "role": "assistant",
        "content": improved
    })
    state["violated"], state["warning"] = enforce_output_guardrails(improved)

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
    
def inputguardrail(state: State) -> str:
    if state["violated"]:
        return "output"
    return "sentiment"
def outputguardrail(state: State)->str:
    if state["violated"]:
        return "output"
    return "summarize"
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
builder.add_conditional_edges("input",
                             inputguardrail,{
                                 "output": "output",
                                 "sentiment":"sentiment",
                             })
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
builder.add_conditional_edges("output",outputguardrail,{
    "summarize": "summarize",
    "output":"output"})
builder.add_edge("summarize", "input")
# builder.add_edge("input", END)

app = builder.compile()



# from IPython.display import Image, display
# graph_image = app.get_graph().draw_mermaid_png()

# with open('image_output.png', 'wb') as f:
#     f.write(graph_image)

# display(Image(filename='image_output.png'))




from IPython.display import Image, display
from IPython.display import display, HTML

mermaid_code = app.get_graph().draw_mermaid()

html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{ startOnLoad: true }});
  </script>
</head>
<body>
  <div class="mermaid">
    {mermaid_code}
  </div>
</body>
</html>
"""

with open("graph_output.html", "w") as f:
    f.write(html)


state: State = {
    "messages": [],
    "customer_details": get_customer_details("@email.com"),
    "plans": get_plans("CUST123456"),
    "Sentiment": "",
    "Threshold": 3,
    "Greedy": 10,
    "pchange": True,
    "user_history": False,
    "current_plan": "",
    "toolcalling":[],
    "total_tokens": 0,
    "violated": False,
    "warning": {}
}

print("Assistant: Welcome to the chat. Can you explain more about you financial situation?")
state = app.invoke(state,{"recursion_limit": 100})