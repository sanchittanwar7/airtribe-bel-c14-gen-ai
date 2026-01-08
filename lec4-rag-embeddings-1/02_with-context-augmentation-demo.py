import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Our "knowledge base" - just a simple string for now
COMPANY_POLICY = """
Acme Corp Remote Work Policy (Updated 2024):
- Employees can work remotely up to 3 days per week.
- Remote work must be approved by direct managers in advance.
- All employees must attend in-person meetings on Wednesdays.
- Remote workers must be available during core hours: 10 AM - 3 PM EST.
- Equipment stipend: $500 annually for home office setup.
"""

def ask_with_context(question, context):
    """Ask question WITH provided context"""
    print("\n" + "="*60)
    print("WITH CONTEXT PROVIDED:")
    print("="*60)
    
    # Construct prompt with context
    prompt = f"""Here is some context information:

<context>
{context}
</context>

Based ONLY on the context above, please answer this question: {question}

If the answer cannot be found in the context, say "I don't have that information in the provided context."
"""
    
    message = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response = message.choices[0].message.content
    print(f"\nQ: {question}")
    print(f"A: {response}")
    return response

# Demo
if __name__ == "__main__":
    print("DEMONSTRATION: The Power of Context")
    print("="*60)
    
    questions = [
        "How many days per week can I work remotely at Acme Corp?",
        "What day must I come to the office?",
        "What's the equipment budget?",
        "What's the dress code?"  # Not in context!
    ]
    
    for question in questions:
        ask_with_context(question, COMPANY_POLICY)
