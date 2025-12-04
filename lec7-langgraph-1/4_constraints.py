from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

import os
import dotenv
dotenv.load_dotenv()

# 1. LLM/Chat Model
model = ChatOpenAI(model="gpt-4", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# 2. Tools (functions with schema)
@tool
def search_logs(service: str, time_range: str) -> str:
    """Search system logs for a service in a time range.
    
    Args:
        service: Service name (e.g., 'api', 'database')
        time_range: Time range (e.g., '1h', '24h')
    """
    # Mock implementation
    return f"Searched {service} logs for {time_range}. Found 5 errors."

# 3. Agent Type + Executor
tools = [search_logs]
agent = create_react_agent(model, tools)

# 4. Invoke
try:
    for chunk in agent.stream({"messages": [("user", "What errors in API last hour?")]}, config={"recursion_limit": 2}):
        print(chunk)
        print("----")
except Exception as e:
    print(f"Error: {e}")