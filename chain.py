from typing import TypedDict,Annotated
from llm import llm
from langchain_core.messages import HumanMessage, AnyMessage
from langgraph.graph.message import add_messages # reducer
from langgraph.graph import MessagesState, StateGraph,START,END

# class MessageState(TypedDict):
#     messages:Annotated[list[AnyMessage],add_messages]

def multiply(a:int, b:int):
# the description of the function is important because that what llm use to read the functionality and dertime the function action
    """
    Mutliply two integers and returns the value
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])

# State
class State(MessagesState):
    pass

# Node
def tool_calling_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state['messages'])]}

# tool_call=llm_with_tools.invoke([HumanMessage(content="What is 2 times 3",name="Amit")])


builder = StateGraph(State)
builder.add_node("tool_calling_llm",tool_calling_llm)
builder.add_edge(START,"tool_calling_llm")
builder.add_edge("tool_calling_llm",END)

# to check the graph is good to go
graph = builder.compile()

messages = graph.invoke({"messages": HumanMessage(content="What is 2 multiply by 4")})

# print(messages['messages'][-1].content)
print(messages)