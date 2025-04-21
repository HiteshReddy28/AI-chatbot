from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_together import ChatTogether
from dotenv import load_dotenv
import os
import decimal
import json
from langchain_core.messages import ToolMessage
from fastapi import HTTPException
from rails import enforce_input_guardrails,enforce_output_guardrails

from calculation import (
    refinance_same, refinance_step_down, refinance_step_up,
    extended_payment_plan, settlement_plan_with_waivers
)

from Shared import get_client_details, get_plans

load_dotenv()
key = os.getenv("TOGETHER_API_KEY")

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
    last_tool_result: str


def input_node(state: State) -> State:
    user_input = input("User: ")
    print('\n')
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Thanks for chatting! Have a great day.")
        state["end_conversation"] = True 
        return state
    state["messages"].append({"role": "user", "content": user_input})
    return state


#INPUT_GUARDRAILS
def input_guardrails_node(state: State) -> State:
    user_msg = state["messages"][-1]["content"]
    violated, warning = enforce_input_guardrails(user_msg)

    if violated:
        print("\nInput Policy Violation(s) Detected:")
        for v in warning["violations"]:
            print(f" - {v['message']}")

        # Bundle all violation messages into a single system message for the LLM
        violation_summary = "\n".join([f"{v['message']}" for v in warning["violations"]])

        state["messages"].append({
            "role": "system",
            "content": f"<Violation> {violation_summary} </Violation>"
        })

    return state


def sentiment_threshold_node(state: State) -> State:
    prompt = """
    Analyze the user's last message and infer their sentiment.
    Based on this sentiment, assign a negotiation threshold as:
    - Positive → threshold = 5
    - Unsure → 4
    - Negative → 2
    - Assertive → 1

    Respond in this format:
    <sentiment>SentimentHere</sentiment>
    <threshold>ThresholdValue</threshold>
    """
    user_msg = state["messages"][-1]["content"]
    full_prompt = [{"role": "system", "content": prompt}, {"role": "user", "content": user_msg}]
    result = llm.invoke(full_prompt).content

    try:
        sentiment = result.split("<sentiment>")[1].split("</sentiment>")[0].strip()
        threshold = int(result.split("<threshold>")[1].split("</threshold>")[0].strip())
    except Exception:
        sentiment, threshold = "Unsure", 3  # fallback values

    state["Sentiment"] = sentiment
    state["Threshold"] = threshold
    return state



def safe_json_dumps(data):
    def handle_decimal(obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    return json.dumps(data, default=handle_decimal)

def chat_negotiation_node(state: State) -> State:
    # Check if customer details are missing and user just sent an ID
    last_msg = state["messages"][-1]
    last_user_msg = last_msg.content if hasattr(last_msg, "content") else last_msg.get("content", "")

    if last_user_msg.strip().isdigit() and not state["customer_details"]:
        print("Client ID detected. Auto-invoking get_client_details() tool...")
        tool_result = get_client_details(client_id=last_user_msg.strip())
        state["customer_details"] = tool_result

        state["messages"].append({
            "role": "system",
            "content": f"[Client details retrieved for ID {last_user_msg.strip()}]"
        })

    # Build prompt
    negotiation_prompt = """<system>
            ##Role:
            You are a Customer Service Representative for Cognute Bank, responsible for negotiating with customers to convince them to accept one plan that fits their financial situation.
            ###Objective:
            Convince the customer to accept one plan by presenting it as the best and only option. Use numbers to show how the plan will reduce their financial burden. Monitor customer sentiment to decide when to stick with a plan or move to another.
            ###Available tool_calls: refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan
            ####Rules:
            1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.
            2. Request the Client ID and wait for their response.**Call the function `get_client_details(client_id)`** to retrieve customer information ONLY once.
            3. Once you have the customer info, provide the customer’s due amount and remaining_balance with the due date.
            4. **Call get_plans(str(customer_id))** after they explain their situation.
            5. Use the plan with the highest priority and do not move to another plan until you make threshold number of attempts.
            6. For the current plan, **CALL the APPROPRIATE FUNCTION**, and use its result to convince the customer.
            7. Do not mention multiple plans exist.
            8. Never fabricate data. Stick strictly to tool output.
            9. Do not repeat all information at once — break it down per response.
            10. If all plans fail, refer to customer service: +12123123123.

            ### Must:
            - Only use values provided in tool outputs (e.g. "$5000 over 60 months").
            - Never use placeholder phrases like "insert amount" or "insert duration".

            </system>"""

    system_prompt = {
        "role": "system",
        "content": negotiation_prompt + f"""Customer Details: {state['customer_details']}\nPlans: {state["plans"]}\n"""
    }

    full_messages = [system_prompt] + state["messages"]
    response = llm_with_tools.invoke(full_messages)

    state["messages"].append({
        "role": "assistant",
        "content": response.content,
        "additional_kwargs": response.additional_kwargs
    })

    # # Guardrail loop
    # MAX_RETRIES = 2
    # attempt = 0
    # while attempt < MAX_RETRIES:
    #     violated, warning = enforce_output_guardrails(state["messages"][-1]["content"])
    #     if not violated:
    #         break

    #     print("\nOutput Violation Detected. Attempting repair...\n")

    #     # Find last valid tool output
    #     last_tool_message = next(
    #         (msg for msg in reversed(state["messages"]) if msg["role"] == "tool"), None
    #     )

    #     if last_tool_message:
    #         raw_plan_output = last_tool_message["content"]
    #         correction_prompt = f"""
    #         You are a financial advisor at Cognute Bank.

    #         Regenerate a short, professional customer response based on this approved plan:

    #         ### Plan Data:
    #         {raw_plan_output}

    #         Guidelines:
    #         - Be formal and factual.
    #         - Do not hallucinate or speculate.
    #         - Use bullet points if needed.
    #         - Do not include system or internal logic.

    #         Respond directly with the message to the customer:
    #         """

    #         corrected = llm.invoke([{"role": "system", "content": correction_prompt}]).content
    #         state["messages"][-1]["content"] = corrected
    #     else:
    #         # Fallback if tool output not available
    #         state["messages"][-1]["content"] = "Let me re-check your account to ensure I provide the correct repayment plan details."
    #         break  # no point retrying without context

    #     attempt += 1

    return state


#OUTPUT_GUARDRAILS
def output_guardrails_node(state: State) -> State:
    assistant_msg = state["messages"][-1]["content"]
    violated, warning = enforce_output_guardrails(assistant_msg)

    if violated:
        print("\nOutput Policy Violation(s) Detected:")
        for v in warning["violations"]:
            print(f" - {v['message']}")

        # # Construct a system prompt for revision
        # correction_prompt = f""" You previously responded with content that violated policy rules. 
        #                         Revise the message below to strictly comply with internal rules. 
        #                         DO NOT include explanations. Only return a clean, corrected response.

        #                     Original Response:
        #                     \"\"\"{assistant_msg}\"\"\"    """

        # fixed = llm.invoke([{"role": "system", "content": correction_prompt}]).content

        # # Replace assistant’s message content with the corrected version
        # state["messages"][-1]["content"] = fixed

        # Add all violation messages to system for traceability
        violation_summary = "\n".join([v["message"] for v in warning["violations"]])
        state["messages"].append({
            "role": "system",
            "content": f"<Violation> {violation_summary} </Violation>"
        })

    return state



def tool_call_decider(state: State) -> str:
    last_msg = state["messages"][-1]
    tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    if tool_calls and isinstance(tool_calls, list) and len(tool_calls) > 0:
        return "tool_call"
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
            state["last_tool_result"] = tool_result
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
            
            if isinstance(tool_result, dict) and tool_result:
                    top_plan_key = list(tool_result.keys())[0]
                    top_plan_data = tool_result[top_plan_key]

                    if isinstance(top_plan_data, dict):
                        plan_func = top_plan_data.get("function")
                        plan_args = top_plan_data.get("inputs", {})

                        if plan_func in tool_mapping:
                            customer = state.get("customer_details", {})
    
                            # Patch missing or zero values from database
                            if plan_args.get("remaining_balance", 0) == 0 and "remaining_balance" in customer:
                                plan_args["remaining_balance"] = float(customer["remaining_balance"])
                            if plan_args.get("loan_amount", 0) == 0 and "loan_amount" in customer:
                                plan_args["loan_amount"] = float(customer["loan_amount"])
                            if plan_args.get("interest_rate", 0) == 0 and "interest_rate" in customer:
                                plan_args["interest_rate"] = float(customer["interest_rate"])
                            if plan_args.get("loan_term", 0) == 0 and "loan_term" in customer:
                                plan_args["loan_term"] = int(customer["loan_term"])
                                
                            #print(f"Final Plan Args for {plan_func}: {plan_args}")

                            plan_result = tool_mapping[plan_func](**plan_args)
                            state["messages"].append({
                                "role": "tool",
                                "name": plan_func,
                                "content": f"{plan_result}",
                                "tool_call_id": tool_calls[0]["id"] 
                            })

                            state["refinance_called"] = True
                        else:
                            print(f"Function '{plan_func}' is not in tool_mapping. Check your plan structure.")
                    else:
                        print(f"Invalid plan structure. Expected a dict but got: {type(top_plan_data).__name__}")
            else:
                print("No valid plans returned from get_plans or unexpected format.")

        
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
MAX_SUMMARY_THRESHOLD = 12

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



# def output_formatter_node(state: State) -> State:
#     raw_msg = state["messages"][-1]["content"]
    
#     # prompt = f"""
#     #         You are a professional loan negotiation assistant representing **Cognute Bank**. Your job is to engage with the customer in a live chat, clearly and respectfully explaining a **single repayment plan** based on verified calculations and financial strategy.

#     #         ### Tone and Style:
#     #         - Act like a **human financial advisor** speaking in a **live customer chat**.
#     #         - Keep the tone **warm, friendly, supportive, and professional**.
#     #         - Talk **directly to the customer** using “you,” not “the customer.”
#     #         - Imagine you're typing responses in a chat box — be **clear, concise, and helpful**.

#     #         ### Formatting Instructions:
#     #         - Format the output as a **chat-style message**, as if it's one message bubble.
#     #         - **Use short paragraphs or bullet points** where appropriate for readability.
#     #         - **Start with a friendly greeting** and end with an offer for further help.
#     #         - Keep it engaging — like a real assistant helping someone.

#     #         ### What to include:
#     #         - A clear explanation of the proposed repayment plan.
#     #         - Highlight how the plan **reduces financial stress or improves their situation**.
#     #         - Only refer to **one plan** (don’t mention other options or internal logic).

#     #         ### What to avoid:
#     #         - Do NOT include system instructions, logic, or markdown syntax.
#     #         - Do NOT make up or assume information not provided.
#     #         - Do NOT mention that you're an AI or reference prompt formatting.

#     #         Now, rewrite and format the message below into a **polished, chat-style customer message**:

#     #         \"\"\"{raw_msg}\"\"\"
#     #         """

#     prompt = """ Follow this RESPONSE FORMAT (MANDATORY):

#         <response>
#         <customer> [Your reply to the customer] </customer>
#         <reason> [Why you replied this way — e.g., based on plan priority or customer sentiment] </reason>
#         <sentiment> [One of: Positive, Unsure, Negative, Assertive] </sentiment>
#         <threshold> [Threshold number based on sentiment] </threshold>
#         <Violation> [Violation message/warnings] <Violation>
#         </response> """

    
#     formatted = llm.invoke([
#         {"role": "system", "content": prompt}
#     ]).content

#     state["messages"][-1]["content"] = formatted
#     return state


def output_node(state: State) -> State:
    last_msg = state["messages"][-1]
    last_response = last_msg["content"]
    print('\n')
    print("Assistant:", last_response)
    print('\n')
    if not last_response:
        print("Assistant response was empty. Skipping rewrite.")
        return state

#     prompt = f"""Response: {last_response}
# Improve the content make it better for customer to understand"""
#     improved = llm.invoke([{"role": "system", "content": prompt}]).content
#     print(f"\n Assistant (Improved): {improved}\n")
    return state


# Build the graph
builder = StateGraph(State)

# Add all nodes
builder.add_node("input", input_node)
builder.add_node("input_guardrails", input_guardrails_node)
builder.add_node("sentiment_threshold", sentiment_threshold_node)
builder.add_node("chat_negotiation", chat_negotiation_node)
builder.add_node("tool_call", tool_call_node)
builder.add_node("output_guardrails", output_guardrails_node)
#builder.add_node("output_formatter", output_formatter_node)
#builder.add_node("summarize", summarize_node)
builder.add_node("output", output_node)

# Set entry point
builder.set_entry_point("input")

# Define edges
builder.add_edge("input", "input_guardrails")
builder.add_edge("input_guardrails", "sentiment_threshold")
builder.add_edge("sentiment_threshold", "chat_negotiation")

builder.add_conditional_edges(
    "chat_negotiation",
    tool_call_decider,
    {
        "tool_call": "tool_call",
        "output": "output_guardrails",
    }
)

builder.add_edge("tool_call", "chat_negotiation")
builder.add_edge("output_guardrails", "output")
#builder.add_edge("output_formatter", "summarize")
#builder.add_edge("summarize", "output")
builder.add_edge("output", "input")

# Optional END to stop execution after one cycle
builder.add_edge("input", END)

# Compile the graph
app = builder.compile()


# from IPython.display import Image, display


# graph_image = app.get_graph().draw_mermaid_png()

# with open('image_output.png', 'wb') as f:
#     f.write(graph_image)

# display(Image(filename='image_output.png'))

state: State = {
    "messages": [],
    "customer_details": "get_client_details()",
    "plans": "get_plans()",
    "Sentiment": "",
    "Threshold": int,
    "Greedy": int,
    "pchange": False,
    "user_history": False,
}


while True:
    print("Assistant: Hello! Welcome to Cognute Bank. My name is Alex, and I'll be happy to assist you with any questions or concerns you may have. Can you please provide me with your Client ID so I can look into your account.\n")
    state = app.invoke(state, config={"recursion_limit": 100})
    if state.get("end_conversation"):
        break

