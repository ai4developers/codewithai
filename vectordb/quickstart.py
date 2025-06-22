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
#     Github repository : https://github.com/ai4developers/codewithai/tree/main/vectordb
# Stay curious, build boldly.
# — AI for Developers Team
# =============================================================================


# 📌 Install first: pip install faiss-cpu sentence-transformers

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# 1️⃣ Load an embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2️⃣ Sample text data
documents = [
    "The cat sits on the mat.",
    "Dogs are loyal animals.",
    "I love machine learning and AI.",
    "Birds can fly high in the sky."
]

# 3️⃣ Embed documents
embeddings = model.encode(documents)

# 4️⃣ Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance

# 5️⃣ Add embeddings
index.add(np.array(embeddings))

# 6️⃣ Query: find similar docs to a new sentence
query = "Tell me about pets."
query_embedding = model.encode([query])

# 7️⃣ Search
k = 2  # top 2 results
distances, indices = index.search(np.array(query_embedding), k)

print("\nQuery:", query)
print("\nTop results:")
for idx, dist in zip(indices[0], distances[0]):
    print(f" - {documents[idx]} (distance: {dist:.4f})")
