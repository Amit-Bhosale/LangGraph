from IPython.display import Image,display
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
import random

class State(TypedDict):
    graph_state:str

def node_1(state):
    return {"graph_state":state['graph_state'] +" I am"}

def node_2(state):
    return {"graph_state":state['graph_state'] +" happy"}

def node_3(state):
    return {"graph_state":state['graph_state'] +" sad"}


def decide_mood(state):
    user_input = state['graph_state']

    if random.random() < 0.5:
        return "node_2"
    
    return "node_3"


# # build graph
builder=StateGraph(State)

# initalize graph nodes
builder.add_node("node_1",node_1)
builder.add_node("node_2",node_2)
builder.add_node("node_3",node_3)


# logic
builder.add_edge(START,"node_1")
builder.add_conditional_edges("node_1",decide_mood)
builder.add_edge("node_2",END)
builder.add_edge("node_3",END)

graph=builder.compile()
print(graph.invoke({"graph_state":"Hi iam Amit"}))

# view diagram of graph
# display(Image(graph.get_graph().draw_mermaid_png()))





