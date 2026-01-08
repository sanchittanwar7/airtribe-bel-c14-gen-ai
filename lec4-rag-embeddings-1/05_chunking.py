"""
Text Chunking Strategies for RAG Systems
"""

def chunk_by_characters(text, chunk_size=500, overlap=50):
    """
    Split text into chunks by character count with overlap
    
    Args:
        text: Input text
        chunk_size: Maximum characters per chunk
        overlap: Characters to overlap between chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # Move back for overlap
    
    return chunks


def chunk_by_sentences(text, sentences_per_chunk=3):
    """
    Split text into chunks by sentence count
    More natural boundaries than character splitting
    """
    # Simple sentence splitter (production would use NLTK or spaCy)
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = '. '.join(sentences[i:i + sentences_per_chunk]) + '.'
        chunks.append(chunk)
    
    return chunks


def chunk_by_paragraphs(text):
    """
    Split by paragraphs - preserves semantic boundaries
    """
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]

# Demo
if __name__ == "__main__":
    sample_text = """
Artificial Intelligence has transformed how we interact with technology. Machine learning models can now understand and generate human language with remarkable accuracy.

Large Language Models (LLMs) are trained on vast amounts of text data. They learn patterns, context, and even reasoning capabilities. However, they have limitations.

One major limitation is that LLMs don't know about data they weren't trained on. This is where Retrieval Augmented Generation comes in. RAG systems retrieve relevant information and provide it to the LLM.

By combining retrieval with generation, we get the best of both worlds. The LLM can leverage its reasoning capabilities while having access to up-to-date, specific information.
    """
    
    print("ORIGINAL TEXT LENGTH:", len(sample_text), "characters\n")
    
    print("="*60)
    print("METHOD 1: Character-based chunking (500 chars, 50 overlap)")
    print("="*60)
    chunks1 = chunk_by_characters(sample_text, 500, 50)
    for i, chunk in enumerate(chunks1, 1):
        print(f"\nChunk {i} ({len(chunk)} chars):\n{chunk[:100]}...")
    
    print("\n" + "="*60)
    print("METHOD 2: Sentence-based chunking (2 sentences per chunk)")
    print("="*60)
    chunks2 = chunk_by_sentences(sample_text, 2)
    for i, chunk in enumerate(chunks2, 1):
        print(f"\nChunk {i}:\n{chunk}")
    
    print("\n" + "="*60)
    print("METHOD 3: Paragraph-based chunking")
    print("="*60)
    chunks3 = chunk_by_paragraphs(sample_text)
    for i, chunk in enumerate(chunks3, 1):
        print(f"\nChunk {i}:\n{chunk[:150]}...")
        