from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
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

from rails import enforce_input_guardrails, enforce_output_guardrails

# Initialize the model
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", api_key=TOGETHER_API_KEY)

# LangGraph Nodes
def input_validation_node(state):
    violated, updated_state = enforce_input_guardrails(state)
    if violated:
        raise HTTPException(status_code=400, detail="Input validation failed due to policy violation.")
    return updated_state

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
                state["client_id"] = args["client_id"]
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
            content=f"<response>{json.dumps(result, default=str)}</response>"
        )

        state["messages"].append(tool_msg)

        # Re-invoke the LLM with updated context
        response = llm.invoke(state["messages"], tools=tools)

    state["messages"].append(response)
    return state

def output_validation_node(state):
    violated, updated_state = enforce_output_guardrails(state)
    if violated:
        print("\nOutput violation detected. Attempting self-repair...\n")
        original = state["messages"][-1]["content"]
        correction_prompt = f"""
        Your previous response violated policy (e.g., sensitive data, hallucination, system info).
        Please revise the following to be fully compliant without explaining the violation.

        Response to fix:
        \"\"\"{original}\"\"\"
        """
        corrected = llm.invoke([{"role": "system", "content": correction_prompt}]).content
        state["messages"][-1]["content"] = corrected
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
def run_negotiate_chain(user_input: str, client_id: str = "") -> dict:
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

        print("\nRAW AI RESPONSE")
        print(content)

        return {"negotiation_response": content}

    except Exception as e:
        print(f"Error in /api/negotiate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
