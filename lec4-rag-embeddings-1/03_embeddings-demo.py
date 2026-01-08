"""
Understanding Embeddings: Basic Operations
This demo shows how to generate and inspect embeddings
"""

import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text, model="text-embedding-3-small"):
    """
    Generate embedding for text using OpenAI API
    
    Args:
        text: Input text string
        model: Embedding model to use
    
    Returns:
        List of floats (the embedding vector)
    """
    # Clean the text
    text = text.replace("\n", " ").strip()
    
    # Call API
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    
    # Extract embedding from response
    embedding = response.data[0].embedding
    
    return embedding


# Demo
if __name__ == "__main__":
    print("="*70)
    print("DEMO 1: What Does an Embedding Look Like?")
    print("="*70)
    
    sample_text = "Machine learning is a subset of artificial intelligence"
    embedding = get_embedding(sample_text)
    
    print(f"\nOriginal Text:")
    print(f"  '{sample_text}'")
    
    print(f"\nEmbedding Properties:")
    print(f"  - Type: {type(embedding)}")
    print(f"  - Dimensions: {len(embedding)}")
    print(f"  - First 10 values: {embedding[:10]}")
    print(f"  - Data type: {type(embedding[0])}")
    
    # Calculate some statistics
    embedding_array = np.array(embedding)
    print(f"\nStatistics:")
    print(f"  - Min value: {embedding_array.min():.4f}")
    print(f"  - Max value: {embedding_array.max():.4f}")
    print(f"  - Mean: {embedding_array.mean():.4f}")
    print(f"  - Std dev: {embedding_array.std():.4f}")
    print(f"  - Vector magnitude: {np.linalg.norm(embedding_array):.4f}")
    