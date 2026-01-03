import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages = [
    {"role": "system", "content": "You are a helpful assistant that replies concisely."},
    {"role": "user", "content": "Explain semantic search in two sentences."}
]

resp = client.chat.completions.create(
    model="gpt-4o-mini",   # pick a model available to you
    messages=messages,
    temperature=0.2,
    max_tokens=120
)

# Inspect response
print("Raw response: ", resp)
print("--------------------------------")
print("Finish reason :", resp.choices[0].finish_reason)
print("--------------------------------")
print("Content :", resp.choices[0].message.content)
print("--------------------------------")
print("Usage :", resp.usage)