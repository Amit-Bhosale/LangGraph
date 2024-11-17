from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from llm import llm

# Define arithmetic functions
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two integers and return the result."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract two integers and return the result."""
    return a - b

# Define State class
class State(MessagesState):
    pass

# Bind tools to LLM
tools = [add, subtract, multiply, divide]
llm_with_tools = llm.bind_tools(tools)

# Define assistant node logic
sys_message = SystemMessage(content="Your helpful assistant tasked with performing arithmetic operations.")
def assistant(state: State):
    return {"messages": [llm_with_tools.invoke([sys_message] + state["messages"])]}

# Build the graph
builder = StateGraph(State)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,  # Route to tools if needed, else to END
)
builder.add_edge("tools", "assistant")

# Compile the graph
graph = builder.compile()

# Input message
messages = [HumanMessage(content="what is division 12 by 3 and then add with 2")]

# Execute the graph
messages = graph.invoke({"messages": messages})

# Output the messages
for m in messages["messages"]:
    print(m.pretty_print())
