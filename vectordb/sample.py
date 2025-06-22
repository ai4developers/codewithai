from sentence_transformers import SentenceTransformer
import numpy as np
import matplotlib.pyplot as plt

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your text
text = "Hello World"

# Generate vector
embedding = model.encode(text)

# Plot vector as a bar chart
plt.figure(figsize=(14, 4))
plt.bar(range(len(embedding)), embedding)
plt.title(f"Vector representation of '{text}'")
plt.xlabel("Vector Dimensions")
plt.ylabel("Value")
plt.show()