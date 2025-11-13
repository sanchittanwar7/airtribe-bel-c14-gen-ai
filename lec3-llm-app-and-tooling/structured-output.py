import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Using response_format for JSON
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a data extraction assistant. Response must be in JSON format"},
        {"role": "user", "content": "Extract information: John Smith is 30 years old and works as a software engineer in Seattle."}
    ],
    # response_format={"type": "json_object"}  # Forces JSON output
)

try:
    data = json.loads(response.choices[0].message.content)
    print(json.dumps(data, indent=2))
except:
    print("Not a json response. Raw text: ", response.choices[0].message.content)
