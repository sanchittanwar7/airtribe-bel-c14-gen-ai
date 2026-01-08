"""
Understanding Cosine Similarity
How we measure similarity between embeddings
"""

import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text, model="text-embedding-3-small"):
    """Generate embedding for text"""
    text = text.replace("\n", " ").strip()
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors
    
    Formula: cos(θ) = (A · B) / (||A|| × ||B||)
    
    Geometric interpretation:
    - Measures the angle between two vectors
    - Ignores magnitude, focuses on direction
    
    Returns:
        Float between -1 and 1:
        - 1.0 = Same direction (very similar)
        - 0.0 = Perpendicular (unrelated)
        - -1.0 = Opposite direction (opposite meaning)
    """
    # Convert to numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Calculate dot product (numerator)
    dot_product = np.dot(vec1, vec2)
    
    # Calculate magnitudes (denominator)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    
    # Cosine similarity
    similarity = dot_product / (magnitude1 * magnitude2)
    
    return similarity


def compare_texts(text1, text2):
    """Helper to compare two texts"""
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    similarity = cosine_similarity(emb1, emb2)
    return similarity


# Demo
if __name__ == "__main__":
    print("="*70)
    print("UNDERSTANDING COSINE SIMILARITY")
    print("="*70)
    
    print("\nCosine similarity measures the ANGLE between vectors:")
    print("  - Closer angle = More similar meaning")
    print("  - Score ranges from -1 to 1")
    print("  - Higher score = More similar\n")
    
    # print("="*70)
    # print("DEMO 1: Identical Text")
    # print("="*70)
    
    # text = "Machine learning is fascinating"
    # sim = compare_texts(text, text)
    # print(f"\nText 1: '{text}'")
    # print(f"Text 2: '{text}'")
    # print(f"Similarity: {sim:.4f}")
    # print("→ Perfect match! Score = 1.0 (or very close)")
    
    # print("\n" + "="*70)
    # print("DEMO 2: Similar Meaning (Paraphrases)")
    # print("="*70)
    
    # pairs = [
    #     ("The cat is sleeping on the couch", 
    #      "A feline is resting on the sofa"),
        
    #     ("I love programming in Python",
    #      "Python programming is my passion"),
        
    #     ("The weather is beautiful today",
    #      "Today's weather is really nice"),
    # ]
    
    # for text1, text2 in pairs:
    #     sim = compare_texts(text1, text2)
    #     print(f"\nText 1: '{text1}'")
    #     print(f"Text 2: '{text2}'")
    #     print(f"Similarity: {sim:.4f} ← High similarity!")
    
    # print("\n" + "="*70)
    # print("DEMO 3: Different Topics (Low Similarity)")
    # print("="*70)
    
    # pairs = [
    #     ("The cat is sleeping on the couch",
    #      "Python is a programming language"),
        
    #     ("I love pizza with extra cheese",
    #      "Quantum mechanics is complex"),
        
    #     ("The stock market crashed today",
    #      "Roses are red, violets are blue"),
    # ]
    
    # for text1, text2 in pairs:
    #     sim = compare_texts(text1, text2)
    #     print(f"\nText 1: '{text1}'")
    #     print(f"Text 2: '{text2}'")
    #     print(f"Similarity: {sim:.4f} ← Low! Different topics")
    
    print("\n" + "="*70)
    print("DEMO 4: Semantic Search Example")
    print("="*70)
    
    # A mini knowledge base
    documents = [
        "Python is a high-level programming language",
        "Machine learning models can predict outcomes",
        "The cat jumped over the fence",
        "Data science involves statistics and programming",
        "Basketball is played with five players per team"
    ]
    
    query = "Tell me about programming languages"
    
    print(f"\nQuery: '{query}'")
    print(f"\nSearching through {len(documents)} documents...\n")
    
    # Get query embedding
    query_emb = get_embedding(query)
    
    # Compare with each document
    results = []
    for doc in documents:
        doc_emb = get_embedding(doc)
        sim = cosine_similarity(query_emb, doc_emb)
        results.append((doc, sim))
    
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("Results (ranked by relevance):")
    print("-" * 70)
    for i, (doc, score) in enumerate(results, 1):
        stars = "★" * int(score * 10)
        print(f"\n{i}. Score: {score:.4f} {stars}")
        print(f"   {doc}")
    
    # print("\n" + "="*70)
    # print("DEMO 5: Similarity Matrix (Visualizing Relationships)")
    # print("="*70)
    
    # test_sentences = [
    #     "dog",
    #     "puppy", 
    #     "cat",
    #     "kitten",
    #     "flying",
    #     "aircraft"
    # ]
    
    # print("\nComputing similarity matrix for words...\n")
    
    # Generate all embeddings
    # embeddings = [get_embedding(s) for s in test_sentences]
    
    # Print header
    # print(f"{'':10}", end="")
    # for s in test_sentences:
    #     print(f"{s:>10}", end="")
    # print()
    # print("-" * 60)
    
    # Print similarity matrix
    # for i, s1 in enumerate(test_sentences):
    #     print(f"{s1:10}", end="")
    #     for j, s2 in enumerate(test_sentences):
    #         sim = cosine_similarity(embeddings[i], embeddings[j])
    #         print(f"{sim:10.3f}", end="")
    #     print()
