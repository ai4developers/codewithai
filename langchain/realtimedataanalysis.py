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
from langchain.agents import initialize_agent, Tool, AgentType

# 1️⃣ Your custom HTTP fetcher
import requests

def fetch_url_content(url: str) -> str:
    """
    Fetches the HTML content of a URL and returns the first 500 characters.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        text = response.text
        return text[:500] + "..."  # Truncate for safety
    except Exception as e:
        return f"Error fetching URL: {e}"

# 2️⃣ Wrap it in a Tool
fetch_tool = Tool(
    name="CustomWebFetcher",
    func=fetch_url_content,
    description="Fetch the raw HTML content of a web page given a URL string."
)

# 3️⃣ Create the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")

# 4️⃣ Initialize the agent with your tool
agent = initialize_agent(
    tools=[fetch_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 5️⃣ Ask the agent a question that triggers the tool
question = (
    "Fetch the current weather from https://api.open-meteo.com/v1/forecast?latitude=35&longitude=139&current_weather=true "
    "and summarize whether it's good weather for outdoor sports."
)


result = agent.run(question)

print("\n=== Result ===")
print(result)
