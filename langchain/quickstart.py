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
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


# 1) Create a prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)

# 2) Connect Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")

# 3) Create the chain
chain = LLMChain(prompt=prompt, llm=llm)

# 4) Run the chain
response = chain.run({"topic": "quicksort algorithm"})
print(response)