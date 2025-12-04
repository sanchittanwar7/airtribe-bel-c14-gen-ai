print("\n" + "="*80)
print("EXAMPLE 6: MEMORY PATTERNS")
print("="*80)

from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import os
import dotenv
dotenv.load_dotenv()

class MemoryState(TypedDict):
    user_id: str
    conversation_history: List[str]
    current_question: str
    answer: str

def load_memory(state: MemoryState) -> MemoryState:
    """Load conversation history for user"""
    user_id = state["user_id"]
    print(f"[LOAD MEMORY] Loading history for user: {user_id}")
    
    # Simulate loading from database
    history = [
        "User: What is LangGraph?",
        "Assistant: LangGraph is a framework for building stateful agents.",
    ]
    
    return {"conversation_history": history}

def answer_with_memory(state: MemoryState) -> MemoryState:
    """Answer using conversation history"""
    llm = ChatOpenAI(model="gpt-4o")
    
    history_text = "\n".join(state.get("conversation_history", []))
    prompt = f"""Conversation history:
{history_text}

Current question: {state['current_question']}

Provide an answer that considers the conversation history."""
    
    response = llm.invoke(prompt)
    return {"answer": response.content}

def update_memory(state: MemoryState) -> MemoryState:
    """Update conversation history"""
    print(f"[UPDATE MEMORY] Saving conversation...")
    
    # In production: save to database
    updated_history = state["conversation_history"] + [
        f"User: {state['current_question']}",
        f"Assistant: {state['answer']}"
    ]
    
    return {"conversation_history": updated_history}

# Build memory graph
memory_workflow = StateGraph(MemoryState)

memory_workflow.add_node("load", load_memory)
memory_workflow.add_node("answer", answer_with_memory)
memory_workflow.add_node("update", update_memory)

memory_workflow.add_edge("load", "answer")
memory_workflow.add_edge("answer", "update")
memory_workflow.add_edge("update", END)
memory_workflow.set_entry_point("load")

memory_app = memory_workflow.compile()

# Run
result = memory_app.invoke({
    "user_id": "user123",
    "current_question": "Can you explain more about its benefits?"
})
print(f"\nAnswer: {result['answer']}")
print(f"History length: {len(result['conversation_history'])}\n")



# https://smith.langchain.com/o/60aef616-03f9-4ae5-b069-4efb1d4b9165?paginationModel=%7B%22pageIndex%22%3A0%2C%22pageSize%22%3A5%7D