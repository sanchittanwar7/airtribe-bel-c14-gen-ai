import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history = [
    {"role": "system", "content": "You are a helpful math tutor."}
]

def chat(user_message):
    """Add user message, get response, add to history."""
    # Add user message
    conversation_history.append({"role": "user", "content": user_message})
    
    # Get response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )
    
    # Extract assistant message
    assistant_message = response.choices[0].message.content
    
    # Add to history
    conversation_history.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message

# Multi-turn conversation
print("User: What is 15 * 23?")
print(f"Assistant: {chat('What is 15 * 23?')}\n")

print("User: Now add 100 to that.")
print(f"Assistant: {chat('Now add 100 to that.')}\n")

print("User: What was my first question?")
print(f"Assistant: {chat('What was my first question?')}\n")

print(f"\nFull conversation history: {len(conversation_history)} messages")