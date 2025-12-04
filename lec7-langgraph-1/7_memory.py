from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain.callbacks import StdOutCallbackHandler
from langgraph.checkpoint.memory import MemorySaver


import os
import dotenv
dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
tools = []

# WITHOUT MEMORY
# print("\n--- WITHOUT MEMORY ---")
# agent = create_react_agent(model, tools)  # No checkpointer

# response1 = agent.invoke({"messages": [("user", "Calculate 10+5")]})
# print(response1["messages"][-1].content)

# response2 = agent.invoke({"messages": [("user", "Double that")]})
# print(response2["messages"][-1].content)

# WITH MEMORY
print("\n--- WITH MEMORY ---")
memory = MemorySaver()
agent = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "user_1"}}

response1 = agent.invoke(
    {"messages": [("user", "Calculate 10+5")]},
    config
)
print(response1["messages"][-1].content)

response2 = agent.invoke(
    {"messages": [("user", "Double that")]},
    config
)
print(response2["messages"][-1].content)