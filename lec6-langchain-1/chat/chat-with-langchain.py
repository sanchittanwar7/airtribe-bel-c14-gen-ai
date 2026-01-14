from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI Implementation ---
# Block 1: MODEL - The LLM wrapper
print("--- OpenAI ---")
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)
# print("--- Anthropic ---")
# model = ChatAnthropic(
#     model="claude-sonnet-4-5-20250929", 
#     temperature=0.7, 
#     api_key=os.getenv("ANTHROPIC_API_KEY")
# )

# Block 2: PROMPT - Template for input
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence for a {audience}."
)

# Block 3: CHAIN - Connect them together using LCEL (pipe operator)
chain = prompt | model | StrOutputParser()

# Run it
result = chain.invoke({"topic": "neural networks", "audience": "5 year old"})
print(result)
