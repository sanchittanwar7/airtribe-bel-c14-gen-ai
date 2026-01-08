import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_without_context(question):
    """Ask question WITHOUT providing context"""
    print("\n" + "="*60)
    print("WITHOUT CONTEXT:")
    print("="*60)
    
    message = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": question}
        ]
    )
    
    response = message.choices[0].message.content
    print(f"\nQ: {question}")
    print(f"A: {response}")
    return response

# Demo questions about fictional company data
questions = [
    "What is Acme Corp's policy on remote work?",
    "How many vacation days do Acme Corp employees get?",
    "What is the equipment stipend for Acme Corp remote workers?"
]

if __name__ == "__main__":
    print("DEMONSTRATION: LLM Knowledge Limitations")
    print("="*60)
    print("Asking about fictional company 'Acme Corp'...\n")
    
    for question in questions:
        ask_without_context(question)
