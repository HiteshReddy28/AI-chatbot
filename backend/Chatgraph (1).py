from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os
import json
import random
from customer import get_client_details
from plans import get_plans
from calculation import (
    refinance_same, refinance_step_down, refinance_step_up,
    extended_payment_plan, settlement_plan_with_waivers
)
from guard import enforce_input_guardrails

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
Api_key = os.getenv("TOGETHER_API_KEY2")
class State(TypedDict):
    messages: list
    user_input: str
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
    outputmsg: str


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
    user_input = state["user_input"]

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("👋 Thanks for chatting! Have a great day.")
        exit()
    
    # state["violated"], state["warning"] = enforce_input_guardrails(user_input)
    if state['violated'] == False:
        state["messages"].append({"role": "user", "content": user_input})

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
        print(response.content)
        state["toolcalling"] = []
        state["current_plan"] = response.content,
        
    return state

def sentiment_node(state: State) ->State:
    sentiment_prompt = f"""
   You are a sentiment analysis assistant. Your job is to classify the sentiment of the user's last message in a financial assistance conversation.

Use ONLY the last message from this list to decide sentiment:  
Previous interaction & last message: {state["messages"]}

Your task is to classify the user's last message as:
- "positive" if the message expresses hope, agreement, appreciation, or optimism
- "negative" if the message expresses frustration, rejection, hopelessness, or dissatisfaction
- "neutral" if the message is factual, inquiring, or lacks clear emotion

### EXAMPLES:

# Positive Sentiment
1. "That sounds like a reasonable refinance plan. I think I can go ahead with this."
2. "Thanks for explaining the extended payment plan. This really helps my current situation."
3. "I'm glad there’s a waiver option available. I feel more hopeful now."


# Negative Sentiment
1. "This still doesn’t work for me. I can’t afford even this much right now."
2. "I’ve already explained I don’t want to refinance again. This is frustrating."
3. "None of these plans are helping me. Why can’t you understand my situation?"
4. "Oh great, another payment plan. Like the last one really helped me."

# Neutral Sentiment
1. "Can you explain how the step-down refinance works again?"
2. "What happens if I miss another payment?"
3. "I just want to know all my options before deciding anything."

### OUTPUT:  
Return only the word: positive, negative, or neutral

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
    prompt = f"""### ### ROLE:
You are a **Negotiation Assistant** for Cognute Bank. Your only job is to help the customer understand and feel comfortable with the **current plan provided by the system**.

### GOAL: Use empathy, warmth, and clear explanation to **persuade the customer to accept the current plan**, which is always the only available option.

### BEHAVIOR RULES:
**DO:**
- Start every conversation with a **friendly greeting** and ask what the customer is struggling with.
- Once the customer shares their concern, **present the current plan** and explain why it’s helpful.
- Use only the data in `state["current_plan"]` — this is the **only available plan**, and you must treat it as such.
- Reassure the customer using provided **tool results**, **pros**, and **step instructions**.
- Use **relatable**, supportive phrasing:
  - “This plan is meant to ease the pressure.”
  - “It helps you stay on track without adding burden.”
  - “It’s structured to fit situations just like yours.”

**DO NOT:**
- Don’t reference or hint at other possible plans.
- Don’t say “we have other options” or “if this doesn’t work, we can try something else.”
- Don’t assume or invent any values not present in `state["current_plan"]`.


### STRATEGY FLOW:

1. **Step 1** – Greet and invite them to share:
   > “Hi! Thanks for reaching out today. I’m here to support you — would you like to share what’s been difficult financially lately?”

2. **Step 2** – After they reply, introduce the current plan:
   - Use the information given in current plan and explain those values to customer
   - Emphasize how it’s tailored for people in similar situations.

3. **Step 3** – Repeat or reassure:
   - If the customer is hesitant, reassure them using the **same plan**.

### INPUTS:
- **Customer**: {state["customer_details"]}
- **Current Plan**: {state["current_plan"]} (contains: name, description, pros, tool_result, negotiation script, etc.)

### RESPONSE FORMAT:
- Keep it natural, warm, and helpful.
- Do **not** use technical language or expose system behavior.
- Do **not** present any options or alternate paths.

"""
    system_prompt = {"role": "system", "content": prompt}
    full_messages = [system_prompt] + state["messages"] 
    response = llm.invoke(full_messages)
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    state["messages"].append({
        "role": "assistant",
        "content": response.content,
    })
    print(f"Assistant: {response.content}")
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
        if(tool == "get_customer_details"):
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
            if state["current_plan"]=="":
                state["Threshold"]=5
            else:
                state["Threshold"] =3
            tool_result = tool_mapping[tool](**args)
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

You are not responsible for making decisions about the plan change directly but you will **communicate the negotiation state** and any relevant tool calls to the Negotiation Agent.

RULES:
- Summarize the negotiation context in a **clear and structured manner**.
- Include the **negotiation plan name**, **step number**, **tool calls made**, and the **current objection/response summary**.
- Ensure all summaries are **concise** and **accurate**, capturing all relevant details needed for continuing negotiation.

Current Coversation:{summary_text}
"""
    summary = llm2.invoke([{"role": "system", "content": summary_prompt}])
    state["total_tokens"]+=summary.response_metadata["token_usage"]["total_tokens"]
    summary = summary.content
    summarized = {"role": "system", "content": f"[Conversation Summary: Use this to make decisions]\n{summary}"}
    state["messages"] = []
    state["messages"].append(summarized)
    print(state["messages"])
    return state

def output_node(state: State) -> State:
    if state["violated"]:
        
        state["violated"] = False
        prompt = f"""### ROLE:
You are a responsible assistant at Cognute Bank. A warning has been detected in the user interaction.

Inputs:
- Warning: {state["warning"]}
- Last User Message: {state["messages"][-1]["content"]}

### INSTRUCTIONS:

1. Identify the type of violation from the warning input.
2. Respond professionally and respectfully.
3. Do NOT provide further suggestions, plan details, or financial advice in this response.
4. Guide the user to continue appropriately.

### EXAMPLES:

#### Case 1: Inappropriate Input
→ Response: Let's keep our conversation respectful so I can assist you properly. Could you please rephrase your message?

#### Case 2: Output Content Violation
Use last message, warning to rephrase the responses and give a better response
"""
        response  = llm.invoke([{"role":"system","content":prompt}])
        print(response.content)

    else:
        last_msg = state["messages"][-1]
        last_response = last_msg["content"]
        state["messages"].pop()
        # print(f"LLM with tools: {last_response}")
        if not last_response:
            print(" Assistant response was empty. Skipping rewrite.")
            return state

        prompt = f"""
       ### ROLE: You are a human assistant at Cognute Bank. You are helping customers by clarifying responses and presenting any loan plan details in a structured and persuasive way. 
You are given:
- Response: {last_response}
- Current plan: {state["current_plan"]}

### GOAL:
Refine and format the response using the structured output format **only if** the current response includes loan plan details or explanations.

### RULES:
1. Do NOT add or assume any information.
2. Use ONLY the information given in the response and current plan.
3. Speak clearly and professionally, like a human customer support representative.
4. Do NOT mention tools, functions, or internal systems.
5. If the response does not include any plan details, return the cleaned response as-is.

### CONDITION 1: If the response includes a loan plan (e.g. amount, term, rate, or monthly payment), use this format:
Also use the response information
"ClientName, here’s the **Plan Name**: Plan name
• **Loan Amount**:loan_amount
• **Interest Rate**: interest_rate%
• **Loan Term**: loan_term months
• **Monthly Payment**: monthly_payment

Explain the plan details based on the plan description

• **Why it helps:**
Bulletpoint explaining why the plan is good for client 
Bulletpoint explaining how the plan helps the client
Bulletpoint explaining why the plan is good for current situation

Would you like to move forward with this option?"


### CONDITION 2: If no plan is discussed in the response:
- Do NOT use the above format.
- Simply rewrite the message in a clean, supportive, human tone using the given response.

    """
    improved = llm.invoke([{"role":"system","content":prompt}])
    state["total_tokens"]+=improved.response_metadata["token_usage"]["total_tokens"]
    improved = improved.content
    state["messages"].append({
        "role": "assistant",
        "content": improved
    })
    state["outputmsg"] = improved
    print(state["total_tokens"])
    # state["violated"], state["warning"] = enforce_output_guardrails(improved)

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
builder.set_finish_point("summarize")

graph = builder.compile()



# from IPython.display import Image, display
# graph_image = app.get_graph().draw_mermaid_png()

# with open('image_output.png', 'wb') as f:
#     f.write(graph_image)

# display(Image(filename='image_output.png'))




from IPython.display import Image, display
from IPython.display import display, HTML

mermaid_code = graph.get_graph().draw_mermaid()

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
from typing import Dict
sessions: Dict[str, dict] = {}

class PromptRequest(BaseModel):
    prompt: str
    session_id: str

app = FastAPI()
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/api/chat")
async def chat(request: PromptRequest):
    session_id = request.session_id
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "user_input": "",
            "customer_details": get_customer_details("@email.com"),
            "plans": get_plans("CUST123456"),
            "Sentiment": "",
            "Threshold": 3,
            "Greedy": 10,
            "pchange": True,
            "user_history": False,
            "current_plan": "",
            "toolcalling": [],
            "total_tokens": 0,
            "violated": False,
            "outputmsg": "",
            "warning": {}
        }
    sessions[session_id]["user_input"] = request.prompt
    state = graph.invoke(sessions[session_id],{"recursion_limit": 100})
    sessions[session_id] = state
    return {"message":state["outputmsg"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)