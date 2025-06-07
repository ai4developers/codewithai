# =============================================================================
# 📘 AI for Developers – Code Examples for Learning
#
# Welcome to the code examples shared under the AI for Developers initiative!
# These examples are designed to help you explore, experiment, and accelerate
# your journey in building intelligent, agent-based systems and AI-integrated
# workflows.
#
# Whether you're working with LangChain, Semantic Kernel, or custom AI agents,
# the goal is to provide practical blueprints that go beyond prompting and into
# programming real AI workflows.
# Refer : https://langchain-ai.github.io/langgraph/agents/agents/
# -----------------------------------------------------------------------------
# ⚠️ Disclaimer & Brand Usage Note
#
# These examples are provided for educational purposes only.
# - Please review and test thoroughly before using in production.
# - Do not redistribute under the name "AI for Developers" without permission.
# - You are welcome to learn, remix, and extend — just keep attribution and 
#   brand safety in mind.
#
# The "AI for Developers" brand stands for community, trust, and ethical innovation.
# Help us keep it that way by using this content responsibly.
#
# -----------------------------------------------------------------------------
# 🔗 Join the movement: https://www.linkedin.com/groups/14276631/
#     Github repository : https://github.com/ai4developers/codewithai/tree/main/langgraph/chatbot
# Stay curious, build boldly.
# — AI for Developers Team
# =============================================================================

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

import os
from langchain.chat_models import init_chat_model

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path for google creds"

llm = init_chat_model("google_genai:gemini-1.5-flash-002")


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break


