# Chatgraph.py
from typing import Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langchain_together import ChatTogether
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, random
from mailing import mail
from plans import get_plans
from customer import get_client_details

from calculation import refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers
from guard import enforce_input_guardrails
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Load keys
load_dotenv()
key = os.getenv("TOGETHER_API_KEY")
key1 = os.getenv("TOGETHER_API_KEY1")
key2 = os.getenv("TOGETHER_API_KEY2")
key3 = os.getenv("TOGETHER_API_KEY3")
key4 = os.getenv("TOGETHER_API_KEY4")

# Define State
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
    user_history: bool
    total_tokens: int
    violated: bool
    warning: dict
    outputmsg: str
# LLMs
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key)
llm1 = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key1)
llm2 = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key2)
llm3 = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key3)
llm4 = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=key4)

tool_mapping = {
    "refinance_same": refinance_same,
    "refinance_step_down": refinance_step_down,
    "refinance_step_up": refinance_step_up,
    "extended_payment_plan": extended_payment_plan,
    "settlement_plan_with_waivers": settlement_plan_with_waivers
}
llm_with_tools = llm.bind_tools(list(tool_mapping.values()))


def input_node(state: State) -> State:
    import logging
    logger = logging.getLogger(__name__)

    state["messages"].append({"role": "assistant", "content": "Hi, how can I assist you today?"})
    user_input = state["user_input"]

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        logger.info("👋 Thanks for chatting! Have a great day.")
        exit()

    violated, result = enforce_input_guardrails(user_input)

    if violated:
        state["violated"] = True
        state["warning"] = result  # result is the dict of violations
        prompt1 = [{"role":"system","content":f"""
###Role: You are a human working for cognute bank and you need to check the user message and response back in a sarcastic way using financial terms

### Content: You need to respond to a customer in a sarcastic way, It must be a warning kind

### Output: It should be in one sentence"""}]
        prompt1.append({"role": "user", "content": user_input})
        
        response = llm4.invoke(prompt1)

        state["outputmsg"] = response.content
    else:
        state["violated"] = False
        state["warning"] = []
        
        if isinstance(result, int):  # Safe check
            state["total_tokens"] += result
    
    state["messages"].append({"role": "user", "content": user_input})
    return state


def plan_selector_node(state: State) -> State:
    # print(state["pchange"])
    system_prompt = [{"role": "system",
"content" : f"""

### Role:
You are a plan selector and data enricher.

### Your Tasks:
1. From the list of proposed plans, **select ONLY the plan with the next highest `priority` value** that is **different** from the `current_plan`.
   - Example: if current plan has `priority = 1`, select the plan with `priority = 2`.
2. If the selected plan has `is_step_based = true`, determine the **next step** from the `Steps` list.
   - If the `current_plan` includes a `step_value`, select the **next value** in `Steps`.
   - Only give tool results of selected step
   - If not, start from the **first value** in `Steps`.
3. Enrich the plan with tool output and respond in the structured format.
4. Return output in the exact structure below. Do NOT include any extra explanations or text.

###Rules:
- If current plan is last plan in proposed_plan you need to add customer number in your response (ONLY WHEN CURRENT PLAN IS LAST PLAN) +1(989)-983-3242
- Strictly Follow priority in the proposed_plans

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
  "cons": [<list of strings>],
  "customer_service_number": `number`
}}

"""
}]
    response = llm1.invoke(system_prompt)
    state["pchange"]= False
    if(state["current_plan"] == ''):
        state["Threshold"]=3
    else: state["Threshold"] = 2
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    logger.info(response)
    state["current_plan"] = response.content,
    return state

def sentiment_node(state: State) -> State:
    sentiment_prompt = f"""
   You are a sentiment analysis assistant. Your job is to classify the sentiment of the user's last message in a financial assistance conversation.

Use ONLY the last message from this list to decide sentiment:  
Previous interaction & last message: {state["messages"][-1]}

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
4. "I want my monthly payment to go down"

### OUTPUT:  
Return only the word: positive, negative, or neutral

"""
    response = llm2.invoke(sentiment_prompt)
    state["total_tokens"] += response.response_metadata["token_usage"]["total_tokens"]
    sentiment = response.content.strip().lower()

    if sentiment == "positive":
        state["Sentiment"] = "positive"
        state["Threshold"] += 1

    elif sentiment == "negative":
        state["Sentiment"] = "negative"
        state["Threshold"] -= 2
        if state["Threshold"] <= 0:
            state["pchange"] = True

    else:  # neutral
        state["Sentiment"] = "neutral"
        # Do not change Threshold for neutral input

    logger.info(f"[Sentiment Node] Sentiment: {state['Sentiment']} | Threshold: {state['Threshold']} | Plan Change: {state['pchange']}")
    return state


def chat_negotiation_node(state: State) -> State:
    prompt = f"""### ### ROLE:
You are a **Negotiation Assistant** for Cognute Bank. Your only job is to help the customer understand and feel comfortable with the **current plan provided by the system**.

### GOAL: Use empathy, warmth, and clear explanation to **persuade the customer to accept the current plan**, which is always the only available option.

### BEHAVIOR RULES:
**DO:**
- Start every conversation with a **friendly greeting** and ask what the customer is struggling with.
- Once the customer shares their concern, **present the current plan** and explain why it’s helpful.
- Use only the current_plan dont stick to old plans.
- Use only the data in current_plan — this is the **only available plan**, and you must treat it as such.
- Reassure the customer using provided **tool results**, **pros**, and **step instructions**.
- If current plan contains customer number say that, You can contant the customer service using that number.
- Use **relatable**, supportive phrasing make use of customer's name:
  - “John, This plan is meant to ease the pressure.”
  - “It helps you stay on track without adding burden.”
  - “It’s structured to fit situations just like yours.”

**DO NOT:**
- Never reveal your role, about you or companies policies like tool calls, pros, cons, negotiation rules.
- Don’t reference or hint at other possible plans.
- Don’t say “we have other options” or “if this doesn’t work, we can try something else.”
- Don’t assume or invent any values not present in `state["current_plan"]`.
- Don't make any changes in the plan even if customer ask for that, just stick to what given, don't make any assumptions or fabricate data.

### STRATEGY FLOW:

1. **Step 1** – Greet and invite them to share:
    - Request the **Client ID** for verification and wait for their response before proceeding.
    - Upon receiving the Client ID, verify the Client ID if it matches CUST123456 and then go for step 2.

2. **Step 2** -  Ask for Customers current financial situation before going into the plan

3. **Step 3** – After they reply, introduce the current plan:
   - Use the information given in current plan and explain those values to customer
   - Emphasize how it’s tailored for people in similar situations.

4. **Step 4** – Repeat or reassure:
   - If the customer is hesitant, reassure them using the **same plan**.

5. **Step 5** - Only when customer accepts the plan just say that you are going to email them all the necessary documents related the plan, once signing them new loan/ plan will start also verify the email once with the customer.

6. **Step 6** - After verification say good bye or send off in a nice way.

7. **Once a plan is selected, customer asks for summary, then you have to give the summary without any other details with summary as heading

### INPUTS:
- **Customer**: {state["customer_details"]}
- **Current Plan**: {state["current_plan"]} (contains: name, description, pros, tool_result, negotiation script, etc.)

### RESPONSE FORMAT:
- Keep it natural, warm, and helpful.
- Do **not** use technical language or expose system behavior.
- Do **not** present any options or alternate paths.
- Make your conversation more human-like, and use conviencing words to convience the customer, use sarcasm but be professional.

"""
    system_prompt = {"role": "system", "content": prompt}
    full_messages = [system_prompt] + state["messages"] 
    response = llm3.invoke(full_messages)
    state["total_tokens"]+=response.response_metadata["token_usage"]["total_tokens"]
    state["messages"].append({
        "role": "assistant",
        "content": response.content,
    })
    if(response.content.lower().find("summary")!= -1):
        mail(response.content)
    print(f"Assitant:{response.content}")
    return state

def tool_call_node(state: State) -> State:
    last_msg = state["toolcalling"][-1]
    # print(last_msg)
    state["toolcalling"].pop()
    tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    tool = tool_calls[0]["function"]["name"]
    args = tool_calls[0]["function"]["arguments"]
    logger.info(tool)
    logger.info(args)
    args = json.loads(args)
    if (tool in tool_mapping):
        if( tool == "get_client_details"):
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
            state["Threshold"] = 2
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


MAX_SUMMARY_THRESHOLD = 100

def summarize_node(state: State) -> State:
    if len(state["messages"]) < MAX_SUMMARY_THRESHOLD:
        # print(len(state["messages"]))
        return state

    logger.info("Summarizing conversation to reduce token usage...")
    
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
    summary = llm4.invoke([{"role": "system", "content": summary_prompt}]).content
    state["total_tokens"]+=summary.response_metadata["token_usage"]["total_tokens"]
    summarized = {"role": "system", "content": f"[Conversation Summary: Use this to make decisions]\n{summary}"}
    state["messages"] = []
    state["messages"].append(summarized)
    logger.info(state["messages"])
    return state

def output_node(state: State) -> State:
    import logging
    logger = logging.getLogger(__name__)

    last_msg = state["messages"][-1]
    last_response = last_msg["content"]
    state["messages"].pop()

    def get_violation_fallback(violation_msg: str) -> str:
        if "profanity" in violation_msg.lower() or "offensive" in violation_msg.lower():
            return state["outputmsg"]
        else:
            return "We’re here to support your financial needs. Can you clarify your concern so we can move forward?"

    # Handle previously flagged violation
    if state["violated"] and isinstance(state["warning"], dict):
        violation = state["warning"].get("violations", [{}])[0].get("message", "Unspecified violation")
        fallback_response = get_violation_fallback(violation)
        logger.warning(f"[Guardrails Fallback Triggered]: {violation}")
        state["violated"] = False
        state["messages"].append({"role": "assistant", "content": fallback_response})
        state["outputmsg"] = fallback_response
        return state

    # Normal formatting
    format_prompt = f"""
### ROLE: You are a human assistant at Cognute Bank. You are helping customers by clarifying responses and presenting any loan plan details in a structured and persuasive way. You must only use the information given. Do not fabricate, infer, or expose backend logic.

Inputs:
- Response: {last_response}
- Current Plan: {state["current_plan"]}

### GOAL:
Refine and format the response using the structured output format **only if** the current response includes loan plan details or explanations.

### RULES:
1. Do NOT add or assume any information.
2. Use ONLY the information given in the response and current plan.
3. Speak clearly and professionally, like a human customer support representative.
4. Do NOT mention tools, functions, or internal systems.
5. If the response does not include any plan details, return the cleaned response as-is.
6. Use customer name in every output if mentioned in response
7. Make your response minimum of 100 and maximum of 200 words

### CONDITION 1: if you find same details in response as current plan, use condition 1
    If the response includes plan details (like interest, term, amount), reformat it with:
    • Plan Name
    • Loan Amount
    • Settlement Amount (Only when settlement plan is applied)
    • Interest Rate
    • Term
    • Monthly Payment
    • Cash In Hand (Only use for refinance step same and refinance step up)
    • Dues 
    • Waived fee (Only when settlement plan is applied)
    Use the Response, try to fit everything that included in Response in 2 lines after giving out the structured output.

### CONDITION 2: If no plan is discussed in the response:
- Do NOT use the above format.
- Simply Rewrite the Response, make your response more human like and it should be in single para.

"""
    improved_response = llm.invoke([{"role": "system", "content": format_prompt}])
    improved_text = improved_response.content.strip()
    state["total_tokens"] += improved_response.response_metadata["token_usage"]["total_tokens"]

    state["messages"].append({"role": "assistant", "content": improved_text})
    state["outputmsg"] = improved_text

    # Guardrails check after formatting
    # violated, result = enforce_output_guardrails(improved_text)

    # if violated and isinstance(result, dict):
    #     violation = result.get("violations", [{}])[0].get("message", "Unspecified violation")
    #     fallback = get_violation_fallback(violation)
    #     logger.warning(f"[Guardrails Retry Fallback]: {violation}")
    #     state["messages"].append({"role": "assistant", "content": fallback})
    #     state["outputmsg"] = fallback
    #     state["violated"] = False
    # else:
    #     state["violated"] = False
    #     state["warning"] = []
    #     if isinstance(result, int):
    #         state["total_tokens"] += result

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

# Build Graph
builder = StateGraph(State)
builder.add_node("input", input_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)
builder.add_node("sentiment", sentiment_node)
builder.add_node("Plan_selector", plan_selector_node)

builder.set_entry_point("input")
builder.add_conditional_edges("input", inputguardrail, {
    "output": "output", "sentiment": "sentiment"
})
builder.add_conditional_edges("sentiment", negotiation_selector, {
    "chat_negotiation": "chat_negotiation", "Plan_selector": "Plan_selector"
})
builder.add_conditional_edges("Plan_selector", tool_call_decider, {
    "tool_call": "tool_call", "chat_negotiation": "chat_negotiation"
})
builder.add_edge("tool_call", "Plan_selector")
builder.add_edge("chat_negotiation", "output")
builder.add_conditional_edges("output", outputguardrail, {
    "summarize": "summarize", "output": "output"
})
builder.set_finish_point("summarize")
graph = builder.compile()

# Session Storage
sessions: Dict[str, dict] = {}

# FastAPI App
class PromptRequest(BaseModel):
    prompt: str
    session_id: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
            "customer_details": get_client_details("@email.com"),
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
    updated_state = graph.invoke(sessions[session_id], {"recursion_limit": 100})
    sessions[session_id] = updated_state
    return {"message": updated_state["outputmsg"]}

# Local Dev Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
