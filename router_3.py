from typing import TypedDict
from llm import llm
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage

def multiply(a:int, b:int):
# the description of the function is important because that what llm use to read the functionality and dertime the function action
    """
    Mutliply two integers and returns the value
    """
    return a * b

class State(MessagesState):
    pass

def tool_calling_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state['messages'])]}

llm_with_tools = llm.bind_tools([multiply])

# build graph
builder = StateGraph(State)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_node("tools",ToolNode([multiply]))

# LOGIC
builder.add_edge(START,'tool_calling_llm')
builder.add_conditional_edges('tool_calling_llm', 
                    # if the latest message (result)  from assistant is a toolcall -> "tools_conditon" routes to tools          
                    # if the latest message (result)  from assistant is not a toolcall -> "tools_conditon" routes to END          
                    tools_condition)
builder.add_edge("tools",END)


graph=builder.compile()


messages=[HumanMessage(content="what is 2 subtract by 3")]
messages=graph.invoke({"messages":messages})

for m in messages['messages']:
    m.pretty_print()
