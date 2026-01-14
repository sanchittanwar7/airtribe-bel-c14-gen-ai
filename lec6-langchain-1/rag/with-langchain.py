from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

# ========== STEP 1: Load Documents ==========
# Option 1: Text Loader
from langchain_community.document_loaders import TextLoader
loader = TextLoader("company_policy.txt")
documents = loader.load()

# Option 2: PDF Loader
# Requires: pip3 install pypdf
# from langchain_community.document_loaders import PyPDFLoader
# loader = PyPDFLoader("company_policy.pdf")
# documents = loader.load()

# Option 3: CSV Loader
# from langchain_community.document_loaders import CSVLoader
# loader = CSVLoader("company_policy.csv")
# documents = loader.load()

# Option 4: Web Loader
# Requires: pip3 install beautifulsoup4
# from langchain_community.document_loaders import WebBaseLoader
# loader = WebBaseLoader("https://drive.google.com/file/d/1eh8v1OSNOcURgz0FPdYVXKqvJcCJBYFC/view?usp=sharing")
# documents = loader.load()

print(f"Loaded {len(documents)} document(s)")

# ========== STEP 2: Split into Chunks ==========
# Option 1: Recursive Character Text Splitter (Current - Recommended)
# Recursively tries to split by different separators to keep related text together.
# 1. "\n\n" (Paragraphs) -> 2. "\n" (Sentences) -> 3. " " (Words) -> 4. "" (Chars)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(documents)

# Option 2: Character Text Splitter
# Simpler. Splits based on a single separator (default "\n\n").
# from langchain.text_splitter import CharacterTextSplitter
# splitter = CharacterTextSplitter(
#     separator="\n\n",
#     chunk_size=200,
#     chunk_overlap=50
# )
# chunks = splitter.split_documents(documents)

# Option 3: Token Text Splitter
# Splits based on token count (useful for LLM context limits).
# Requires: pip install tiktoken
# from langchain.text_splitter import TokenTextSplitter
# splitter = TokenTextSplitter(
#     chunk_size=50,  # Tokens, not characters
#     chunk_overlap=10
# )
# chunks = splitter.split_documents(documents)

print(f"Split into {len(chunks)} chunks")

# ========== STEP 3 & 4: Embed and Store ==========
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("Stored in vector database")

# ========== STEP 5: Create Retriever ==========
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# ========== STEP 6: Build RAG Chain ==========
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context. 
If you cannot answer from the context, say "I don't have information about that."

Context:
{context}

Question: {question}

Answer:
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

# ========== STEP 7: Query! ==========
questions = [
    "How many days of annual leave do I get?",
    "Can I carry forward sick leave?",
    "How many days can I work from home?",
    "What's the policy on overtime pay?"  # Not in context
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_chain.invoke(q)}")