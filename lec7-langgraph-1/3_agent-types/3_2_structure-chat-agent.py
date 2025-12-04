import os
import dotenv
# Install necessary packages:
# pip install langchain langchain-openai langchain_community langchain_core langgraph

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain import hub
from datetime import datetime

# Load environment variables (ensure OPENAI_API_KEY is set in your .env file)
dotenv.load_dotenv()

@tool
def search_logs(service: str, time_range: str, severity: str) -> str:
    """Search system logs for a service in a time range."""
    # Note: In a real app, this would perform actual data fetching.
    # We return a list of dictionaries as a string representation for simplicity,
    # which the LLM can parse and use for the next step.
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

@tool
def create_ticket(severity: str, count: int, message: str) -> dict:
    """Create incident ticket with specific severity, count, and message."""
    print(f"\n--- Creating Ticket: Severity={severity}, Count={count}, Message='{message}' ---\n")
    return {
        "ticket_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "severity": severity,
        "count": count,
        "message": message,
        "status": "CREATED"
    }

# 1. Initialize the LLM
# Structured chat agents work best with models supporting function/tool calling.
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

# 2. Define the tools
tools = [search_logs, create_ticket]

# 3. Pull the prompt template from the LangChain Hub
# This prompt is optimized for structured output and tool use.
prompt = hub.pull("hwchase17/structured-chat-agent")

print(prompt)

# 4. Create the structured chat agent
# This returns a Runnable that decides which tool to use next.
agent = create_structured_chat_agent(llm, tools, prompt)

# 5. Create the Agent Executor
# This manages the loop of thinking -> using tool -> getting output -> thinking...
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# 6. Invoke the agent with the same goal
response = agent_executor.invoke({
    # Note: The input key is typically "input" for AgentExecutor
    "input": "Search service logs for the last hour for high severity API errors. Create a ticket for it."
})

print("\n--- Final Agent Output ---")
# The final response is accessed via the 'output' key
print(response["output"])
