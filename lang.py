from langgraph.graph import StateGraph, END
from langchain_together import ChatTogether
from langchain_core.runnables import RunnableLambda
import os
import json
from Customers import get_customer_details
from Plans import get_plans
from calculation import refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers
 
def update_threshold(customer_id: str, change: str) -> str:
    return f"Threshold {change}d for {customer_id}"

# LLM setup with tools
llm = ChatTogether(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    api_key=os.getenv("TOGETHER_API_KEY")
)
llm_with_tools = llm.bind_tools([get_customer_details, get_plans, refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers
 ])


tool_mapping = { 
    "get_customer_details": get_customer_details,
    "get_plans": get_plans,
    "refinance_same": refinance_same,
    "refinance_step_down": refinance_step_down,
    "refinance_step_up": refinance_step_up,
    "extended_payment_plan": extended_payment_plan,
    "settlement_plan_with_waivers": settlement_plan_with_waivers,
}
# Define your state class

class NegotiatorState(dict):
    customer_data : dict
    Threshold : int
    Messages : list
    sentiment : str
    user_history : bool
    change_plan : bool
    plans : str
    

# Define Node Functions

def start_node(state):
    print("🟢 Starting negotiation...")
    return state

def input_node(state):
    user_input = input("user: ")
    state["Messages"].append({"role":"user","content":user_input})
    # prompt1 = [{""}]
    customer_data = get_customer_details("email_id")
    state["customer_data"] = customer_data
    if(state["user_history"] == True):
        state["Threshold"] = 4
    else:
        state["Threshold"] = 3
    print("Threshold")

    # response = llm_with_tools.invoke(prompt1)
    return state

def negotiate_node(state):
   
    prompt = [{"role":"system","content":"""Make tool calls only when needed
## Available Functions : get_customer_details, get_plans, refinance_same, refinance_step_down, refinance_step_up, extended_payment_plan, settlement_plan_with_waivers
 
## Rules :
1. Greet the customer and ask how you can assist them. Do not discuss plans at this stage.  
2. Request the email ID and wait for their response. Always make sure to **Call get_customer_info(email_id)** to retrieve customer information ONLY once. Do not call get_customer_info(email_id) without obtaining the email first.  
3. Once you have the customer information, provide the customer’s due amount and remaining balance along with the due date (e.g., "$X due") and ask about their current financial situation to better assist them.  
4. **Call get_plans(str(customer_id))** ONLY ONCE after the customer explains their situation to retrieve all available plans in priority order for the customer.  
5. Use the highest-priority plan first and never move to the next plan unless you have negotiated three times on each plan.    
7. Never mention that multiple plans exist or that each plan has a priority.  
8. Call the appropriate tools for each plan and use the data to convince the customer.  
9. If the customer refuses all available plans, provide them with the customer service contact: +1 (862)-405-7154.  
"""}]+ state["Messages"] # + list(state["customer_data"])+ list(state ["plans"])
    # customer_id = state.get("customer_id")
    # plans = get_plans(customer_id)
    # state["plans"] = plans

    # # Use LLM to negotiate
    # prompt = f"""
    # Customer Details: {state['customer_data']}
    # Plans: {plans}
    # Suggest the best negotiation plan and whether to update the threshold.
    # """
    # print(prompt)
    response = llm_with_tools.invoke(prompt)
    # state["negotiation_response"] = str(response)
    state["Messages"].append({"role" : "assistant" , "content" : response.content , "additional_kwargs":response.additional_kwargs})
    print(response)


    return state

def tool(state):
    # msg = state["Messages"][-1]

    last_msg = state["Messages"][-1]
    print(last_msg)
    # tool_calls = last_msg.get("additional_kwargs", {}).get("tool_calls", [])
    # tool = tool_calls[0]["function"]["name"]
    # args = tool_calls[0]["function"]["arguments"]
    # print(tool)
    # args = json.loads(args)
    # if (tool in tool_mapping):
    #     if( tool == "get_customer_details"):
    #         tool_result = tool_mapping[tool](**args)
    #         state["customer_details"] = tool_result
    #     elif (tool == "get_plans"):
    #         tool_result = tool_mapping[tool](**args)
    #         state["plans"] = tool_result
    #     else:
    #         tool_result = tool_mapping[tool](**args)
    #         state["Messages"].append({
    #             "role": "tool",
    #             "name": tool,
    #             "content": f"{tool_result}",
    #             "tool_call_id": tool_calls[0]["id"]
    #         })
    # else:
    #     state["Messages"].append({
    #             "role": "tool",
    #             "name": tool,
    #             "content": f"[Tool Not Found] {tool}"
    #         })
    return state
    # last_msg = state["Messages"][-1]["additional_kwargs"]["tool_calls"][0]
    # tool = last_msg["function"]["name"]
    # args = last_msg["function"]["arguments"]
    # print(tool)
    # if (tool == "get_customer_details"):
    #     result = get_customer_details("hi@gmail.com")
    #     state["Messages"].append({"role":"tool","content":result,"tool_call_id":last_msg["id"]})
    # elif (tool == "get_plans"):
    #     result = get_plans("customer_id")
    #     state["Messages"].append({"role":"tool","content":result,"tool_call_id":last_msg["id"]})
    
    # return state


def tool_checker(state):
    last_msg = state["Messages"][-1]["additional_kwargs"]
    if "tool_calls" in last_msg:
        return "tools"
    else:
        return "output"
    
def nego_check(state):
    lst_msg = state["Messages"]

# def update_threshols(state):
#     if(sentiment.lowerCase() == 'positive' or )

    
def output_node(state):
    # negotiation = state.get("negotiation_response", "")
    # enhanced = f"📜 Negotiation Summary:\n{negotiation}"
    # state["final_output"] = enhanced
    response = state["Messages"][-1]["content"]
    print(f"Bot: {response}")
    return state

# Build the LangGraph


graph = StateGraph(NegotiatorState)


# Add nodes
graph.add_node("input", RunnableLambda(input_node))
graph.add_node("negotiate", RunnableLambda(negotiate_node))
graph.add_node("tools" , RunnableLambda(tool) )
graph.add_node("output", RunnableLambda(output_node))

# Add edges
graph.set_entry_point("input")
graph.add_edge("input" , "negotiate")
graph.add_conditional_edges("negotiate" , tool_checker, {"tools":"tools","output":"output"})
graph.add_edge("tools","negotiate")
graph.add_edge("output", END)

# Compile and run
runnable = graph.compile()

from IPython.display import Image, display


graph_image = runnable.get_graph().draw_mermaid_png()

with open('image_output.png', 'wb') as f:
    f.write(graph_image)

display(Image(filename='image_output.png'))

# Example run
state: NegotiatorState = {
    "customer_data":{},
    "Threshold": 0,
    "Messages":[],
    "sentiment" : "",
    "user_history" : True,
    "plans" : " ",
    "change_plan" : True
}
while True:
    result = runnable.invoke(state)

# Print final output
# print(result["final_output"])
