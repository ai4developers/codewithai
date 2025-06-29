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
# Refer : https://python.langchain.com/docs/introduction/
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
#     Github repository : https://github.com/ai4developers/codewithai/tree/main/langchain
# Stay curious, build boldly.
# — AI for Developers Team
# =============================================================================
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun

# Step 1: Create the LLM (Google Gemini model)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")

# Step 2: Use DuckDuckGoSearchRun for web search (no API key needed)
search = DuckDuckGoSearchRun()

# Step 3: Wrap it into a Tool
search_tool = Tool(
    name="DuckDuckGoSearch",
    func=search.run,
    description="Use this tool to search the web for current information"
)

# Step 4: Initialize the agent with the tool and LLM
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Step 5: Run a query that uses the search tool
query = "What are the latest updates on LangChain AI workflows?"
response = agent.run(query)

# Step 6: Print result
print("\n🔍 AI Agent's Answer:\n", response)
