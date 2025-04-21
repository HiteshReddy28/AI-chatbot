import yaml
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from guardrails import Guard
from langchain_together import ChatTogether
from fastapi import HTTPException
import os
import json

from Shared import (
    prompt,
    tools,
    TOGETHER_API_KEY,
    get_client_details,
    get_plans,
    refinance_same,
    refinance_step_down,
    refinance_step_up,
    extended_payment_plan,
    settlement_plan_with_waivers
)

# Function to load guardrails from the YAML file
def load_guardrails_yaml(file_path="guardrails.yaml"):
    with open(file_path, "r") as file:
        guardrails = yaml.safe_load(file)
    return guardrails

# Load the guardrails YAML dynamically
guardrails_yaml = load_guardrails_yaml("guardrails.yaml")

# Initialize the model
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=TOGETHER_API_KEY)

# Create Guardrails from the loaded YAML
input_guard = Guard.for_rail_string(guardrails_yaml["input_schema"])
output_guard = Guard.for_rail_string(guardrails_yaml["output_schema"])

# LangGraph Nodes 
def input_validation_node(state):
    user_msg = state["messages"][-1].content
    result = input_guard.validate(user_msg)
    if not result.valid:
        raise HTTPException(status_code=400, detail=f"Input validation failed: {result.error_message}")
    return state

def call_model_node(state):
    response = llm.invoke(state["messages"], tools=tools)

    while hasattr(response, "tool_calls") and response.tool_calls:
        tool_call = response.tool_calls[0]
        fn = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Dispatch the tool function
        try:
            if fn == "get_client_details":
                result = get_client_details(args["client_id"])
            elif fn == "get_plans":
                result = get_plans(args["customer_id"], args["priority"])
            elif fn == "refinance_same":
                result = refinance_same(**args)
            elif fn == "refinance_step_down":
                result = refinance_step_down(**args)
            elif fn == "refinance_step_up":
                result = refinance_step_up(**args)
            elif fn == "extended_payment_plan":
                result = extended_payment_plan(**args)
            elif fn == "settlement_plan_with_waivers":
                result = settlement_plan_with_waivers(**args)
            else:
                raise HTTPException(status_code=500, detail=f"Unknown tool function: {fn}")
        except Exception as tool_error:
            raise HTTPException(status_code=500, detail=f"Tool execution error in {fn}: {tool_error}")

        tool_msg = ToolMessage(
            tool_call_id=tool_call.id,
            name=fn,
            content=f"<response>{json.dumps(result)}</response>"
        )

        state["messages"].append(tool_msg)

        # Rerun LLM after tool call
        response = llm.invoke(state["messages"], tools=tools)

    state["messages"].append(response)
    return state

def output_validation_node(state):
    ai_msg = state["messages"][-1].content
    result = output_guard.validate(ai_msg)
    if not result.valid:
        raise HTTPException(status_code=500, detail=f"Output validation failed: {result.error_message}")
    return state

# LangGraph Flow Setup 
graph = StateGraph()
graph.add_node("input_guardrails", input_validation_node)
graph.add_node("llm_response", call_model_node)
graph.add_node("output_guardrails", output_validation_node)

graph.set_entry_point("input_guardrails")
graph.add_edge("input_guardrails", "llm_response")
graph.add_edge("llm_response", "output_guardrails")
graph.add_edge("output_guardrails", END)

chain = graph.compile()

# Public Chain Runner 
def run_negotiate_chain(user_input: str, client_id: str = "") -> str:
    try:
        state = {
            "messages": [
                SystemMessage(content=prompt),
                HumanMessage(content=user_input),
            ],
            "client_id": client_id
        }

        result_state = chain.invoke(state)
        final_msg = result_state["messages"][-1]

        if not isinstance(final_msg, AIMessage):
            raise HTTPException(status_code=500, detail="Unexpected model response type.")

        content = final_msg.content

        # Just print the raw AI response to debug
        print("\nRAW AI RESPONSE")
        print(content)

        # Skip validation and directly return the content for now
        return {"negotiation_response": content}
        
    except Exception as e:
        print(f"Error in /api/negotiate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
