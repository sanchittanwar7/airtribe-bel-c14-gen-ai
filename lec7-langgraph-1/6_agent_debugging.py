from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.callbacks import StdOutCallbackHandler
from langchain.callbacks import StdOutCallbackHandler

import os
import dotenv
dotenv.load_dotenv()

from datetime import datetime

@tool
def search_logs(service: str, time_range: str, severity: str) -> str:
    """Search system logs for a service in a time range."""
    return [
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
    ]

@tool
def create_ticket(severity: str, count: int, message: str) -> dict:
    """Create incident ticket."""
    return {
        "ticket_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "severity": severity,
        "count": count,
        "message": message
    }

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
tools = [search_logs, create_ticket]

agent = create_react_agent(model, tools)

response = agent.invoke({
    "messages": [("user", "Search service logs for last hour for high severity API errors. Create a ticket for it.")]
}, config={
        "callbacks": [StdOutCallbackHandler()]
    })

print(response["messages"][-1].content)