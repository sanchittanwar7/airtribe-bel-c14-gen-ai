from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def stream_chat_completion(prompt):
    """
    Stream a chat completion from OpenAI's API.
    
    Args:
        prompt (str): The user's prompt/question
    """
    print("Assistant: ")
    
    # Create a streaming chat completion
    stream = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "system", "content": "You are a poetic assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True  # Enable streaming
    )
    
    # Process the stream
    full_response = ""
    for chunk in stream:
        # Extract the content from the chunk
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    
    print("\n")  # New line after completion
    return full_response

stream_chat_completion("Write a short haiku about a rainy evening.")
