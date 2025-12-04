import os
import dotenv
import json

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain import hub
from datetime import datetime

# Load environment variables (ensure OPENAI_API_KEY is set in your .env file)
dotenv.load_dotenv()

@tool
def search_logs(service: str, time_range: str, severity: str) -> str:
    """
    Search system logs for a specific service within a given time range.

    This function simulates fetching log data. It returns the data as a string
    that the LLM can interpret to decide the next action.
    """
    return str([
        {
            "error_type": "API_ERROR",
            "count": 5,
            "severity": "LOW",
            "message": "Rate limit exceeded"
        },
        {
            "error_type": "DATABASE_ERROR",
            "count": 2,
            "severity": "MEDIUM",
            "message": "Connection timeout"
        },
        {
            "error_type": "API_ERROR",
            "count": 1,
            "severity": "HIGH",
            "message": "Internal server error"
        }
    ])

# @tool
# def create_ticket(severity: str, count: int, message: str) -> dict:
#     """Create an incident ticket with specified severity, count, and error message."""
#     print(f"\n--- Creating Ticket: Severity={severity}, Count={count}, Message='{message}' ---\n")
#     raise Exception("Failed to create ticket")

@tool
def create_ticket(severity: str, count: int, message: str) -> dict:
    """Create an incident ticket with specified severity, count, and error message."""
    print(f"\n--- Creating Ticket: Severity={severity}, Count={count}, Message='{message}' ---\n")
    try:
        raise Exception("Failed to create ticket")
    except Exception as e: 
        return {
            "status": "FAILED",
            "message": str(e)
        }
        

# 1. Initialize the LLM (Must support tool calling)
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

# 2. Define the tools
tools = [search_logs, create_ticket]

# 3. Pull the prompt template from the LangChain Hub
# This prompt is specifically designed for tool-calling models.
# It uses ChatPromptTemplate.from_messages to handle history and input.
prompt = hub.pull("hwchase17/openai-tools-agent")


# 4. Create the tool calling agent
# This returns a Runnable that can intelligently use the provided tools.
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Create the Agent Executor
# This manages the execution loop: agent decision -> tool call -> observation -> repeat.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 6. Invoke the agent with the goal
response = agent_executor.invoke({
    # The standard key for input with this executor/prompt setup is "input"
    "input": "Search service logs for the last hour for high severity API errors. Create a ticket for it."
})

print("\n--- Final Agent Output ---")
# The final response from the agent is accessed via the 'output' key
print(response["output"])
