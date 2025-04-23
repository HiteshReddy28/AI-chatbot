from rails import enforce_input_guardrails, enforce_output_guardrails
import decimal
import json


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

def safe_json_dumps(data):
    def handle_decimal(obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    return json.dumps(data, default=handle_decimal)


#OUTPUT_GUARDRAILS
def output_guardrails_node(state: State) -> State:
    assistant_msg = state["messages"][-1]["content"]
    violated, warning = enforce_output_guardrails(assistant_msg)

    if violated:
        print("\nOutput Policy Violation(s) Detected:")
        for v in warning["violations"]:
            print(f" - {v['message']}")

        # Construct a system prompt for revision
        correction_prompt = f""" You previously responded with content that violated policy rules. 
                                Revise the message below to strictly comply with internal rules. 
                                DO NOT include explanations. Only return a clean, corrected response.

                            Original Response:
                            \"\"\"{assistant_msg}\"\"\"    """

        fixed = llm.invoke([{"role": "system", "content": correction_prompt}]).content

        # Replace assistant’s message content with the corrected version
        state["messages"][-1]["content"] = fixed

        # Add all violation messages to system for traceability
        violation_summary = "\n".join([v["message"] for v in warning["violations"]])
        state["messages"].append({
            "role": "system",
            "content": f"<Violation> {violation_summary} </Violation>"
        })

    return state


def tool_call_node(state: State) -> State:
    last_msg = state["messages"][-1]
    tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    
    if not tool_calls:
        return state

    tool_call = tool_calls[0]
    fn = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    
    try:
        args = json.loads(tool_call["function"]["arguments"])
        if fn == "get_client_details":
            try:
                client_id = int(args["client_id"])  # Will raise if it's not a valid int
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid client_id passed: {args['client_id']}")
            result = get_client_details(client_id=client_id)
            state["customer_details"] = result

        elif fn == "get_plans":
            result = get_plans(args["customer_id"], args["priority"])
            state["plans"] = result  # Also populate state

        else:
            raise HTTPException(status_code=500, detail=f"Unknown tool function: {fn}")

        # Append tool message for LLM context
        tool_msg = ToolMessage(
            tool_call_id=tool_call["id"],
            name=fn,
            content=f"<response>{safe_json_dumps(result)}</response>"
        )

        state["messages"].append(tool_msg)

    except Exception as tool_error:
        error_msg = f"Tool execution error in {fn}: {tool_error}"
        state["messages"].append({
            "role": "system",
            "content": f"<error>{error_msg}</error>"
        })

    return state
