from backend.app.embeddings.embedder import generate_embedding
from sklearn.metrics.pairwise import cosine_similarity


text1 = "I love Python."
text2 = "Python is my favorite programming language."

embedding1 = generate_embedding(text1)
embedding2 = generate_embedding(text2)

similarity = cosine_similarity(
    [embedding1],
    [embedding2]
)[0][0]

print("TEXT 1:")
print(text1)

print("\nTEXT 2:")
print(text2)

print("\nSEMANTIC SIMILARITY:")
print(round(float(similarity), 4))