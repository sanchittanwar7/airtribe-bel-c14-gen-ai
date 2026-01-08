"""
Conceptual RAG System - Understanding the Flow

This demonstrates the CONCEPT without vector databases.
Next session: Full implementation with vector DBs.
"""

import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    """Generate embedding"""
    response = client.embeddings.create(
        input=[text.replace("\n", " ")],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    """Calculate similarity"""
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def simple_rag_query(query, documents, top_k=2):
    """
    Simple RAG: Query documents and generate answer
    
    This is a CONCEPTUAL implementation.
    Next session: Production-ready with vector databases!
    """
    
    print(f"\n{'='*70}")
    print(f"QUERY: {query}")
    print(f"{'='*70}")
    
    # STEP 1: EMBED THE QUERY
    print("\n[Step 1] Converting query to embedding...")
    query_embedding = get_embedding(query)
    print(f"✓ Query embedding generated ({len(query_embedding)} dimensions)")
    
    # STEP 2: FIND SIMILAR DOCUMENTS
    print(f"\n[Step 2] Searching {len(documents)} documents...")
    
    similarities = []
    for doc in documents:
        doc_embedding = get_embedding(doc)
        similarity = cosine_similarity(query_embedding, doc_embedding)
        similarities.append((doc, similarity))
    
    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_results = similarities[:top_k]
    
    print(f"✓ Found {top_k} most relevant documents:")
    for i, (doc, score) in enumerate(top_results, 1):
        print(f"\n  {i}. Similarity: {score:.4f}")
        print(f"     {doc[:80]}...")
    
    # STEP 3: BUILD CONTEXT
    print(f"\n[Step 3] Building context from retrieved documents...")
    context = "\n\n".join([doc for doc, _ in top_results])
    print(f"✓ Context prepared ({len(context)} characters)")
    
    # STEP 4: GENERATE ANSWER
    print(f"\n[Step 4] Generating answer with LLM...")
    
    prompt = f"""Answer the question based on the provided context.

<context>
{context}
</context>

Question: {query}

Answer based only on the context provided:"""
    
    message = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = message.choices[0].message.content
    print(f"✓ Answer generated")
    
    print(f"\n{'='*70}")
    print("ANSWER:")
    print(f"{'='*70}")
    print(answer)
    
    return answer


# Demo
if __name__ == "__main__":
    print("="*70)
    print("CONCEPTUAL RAG SYSTEM DEMONSTRATION")
    print("="*70)
    
    print("""
This demonstrates the RAG concept flow:
  Query → Embed → Search → Retrieve → Generate

Note: This generates embeddings on-the-fly.
Next session: Store embeddings in vector databases for efficiency!
    """)
    
    # Sample knowledge base
    knowledge_base = [
        "Acme Corp offers 15 days of paid vacation annually. Employees must submit vacation requests at least 2 weeks in advance.",
        
        "Remote work policy: Employees can work from home up to 3 days per week with manager approval.",
        
        "Health insurance covers medical, dental, and vision. Employees contribute 20% of premiums.",
        
        "The equipment stipend is $500 per year for home office setup. Submit receipts to HR for reimbursement.",
        
        "Professional development budget: $1,000 annually for courses, conferences, or certifications.",
    ]
    
    # Test queries
    queries = [
        "How many vacation days do employees get?",
        "What's the remote work policy?",
        "Tell me about the equipment budget"
    ]
    
    for query in queries:
        simple_rag_query(query, knowledge_base, top_k=2)
        print("\n")
    
