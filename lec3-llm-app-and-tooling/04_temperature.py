import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Low temperature - deterministic
print("=== Low Temperature (0.2) ===")
for i in range(3):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        temperature=0.2,
        max_tokens=200,
    )
    print(f"Try {i+1}: {response.choices[0].message.content}")

print("\n=== High Temperature (1.5) ===")
for i in range(3):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Complete: Once upon a time"}],
        temperature=1.5,
        max_tokens=200,
    )
    print(f"Try {i+1}: {response.choices[0].message.content}")