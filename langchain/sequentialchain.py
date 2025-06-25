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
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")

extract_prompt = PromptTemplate(
    input_variables=["text"],
    template="Extract names and dates from this text:\n{text}"
)

summary_prompt = PromptTemplate(
    input_variables=["entities"],
    template="Summarize what this list of entities is about:\n{entities}"
)

extract_chain = LLMChain(prompt=extract_prompt, llm=llm, output_key="entities")
summary_chain = LLMChain(prompt=summary_prompt, llm=llm, output_key="summary")

overall_chain = SequentialChain(
    chains=[extract_chain, summary_chain],
    input_variables=["text"],
    output_variables=["entities", "summary"],
    verbose=True
)

input_text = "John met Sarah on March 3rd. They visited Paris on May 10th."

result = overall_chain.invoke({"text": input_text})
print(result['entities'])
print(result['summary'])