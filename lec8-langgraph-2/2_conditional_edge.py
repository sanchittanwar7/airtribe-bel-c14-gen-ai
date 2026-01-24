
print("\n" + "="*80)
print("EXAMPLE 2: CONDITIONAL EDGES")
print("="*80)

from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
import dotenv
dotenv.load_dotenv()

# Enhanced State with flags
class ConditionalState(TypedDict):
    question: str
    has_context: bool
    context: str
    answer: str

def retrieve_docs(state: ConditionalState) -> ConditionalState:
    """Simulate document retrieval"""
    question = state["question"]
    
    # Simulate retrieval logic
    if "python" in question.lower():
        return {
            "has_context": True,
            "context": "Python is a high-level programming language."
        }
    else:
        return {"has_context": False, "context": ""}

def answer_with_context(state: ConditionalState) -> ConditionalState:
    """Answer using retrieved context"""
    llm = ChatOpenAI(model="gpt-4o")
    prompt = f"Context: {state['context']}\n\nQuestion: {state['question']}"
    response = llm.invoke(prompt)
    return {"answer": response.content}

def fallback_answer(state: ConditionalState) -> ConditionalState:
    """Fallback when no context found"""
    return {"answer": "I don't have enough context to answer that question."}

# Conditional routing function
def route_based_on_context(state: ConditionalState) -> Literal["answer", "fallback"]:
    """Decide next node based on state"""
    if state.get("has_context", False):
        return "answer"
    else:
        return "fallback"

# Build conditional graph
conditional_workflow = StateGraph(ConditionalState)

conditional_workflow.add_node("retrieve", retrieve_docs)
conditional_workflow.add_node("answer", answer_with_context)
conditional_workflow.add_node("fallback", fallback_answer)

# Add conditional edge
conditional_workflow.add_conditional_edges(
    "retrieve",
    route_based_on_context,
    {
        "answer": "answer",
        "fallback": "fallback"
    }
)

conditional_workflow.add_edge("answer", END)
conditional_workflow.add_edge("fallback", END)
conditional_workflow.set_entry_point("retrieve")

conditional_app = conditional_workflow.compile()

# Test both paths
print("\n--- Test 1: With Context ---")
result1 = conditional_app.invoke({"question": "What is Python?"})
print(f"Answer: {result1['answer']}")

# print("\n--- Test 2: Without Context ---")
# result2 = conditional_app.invoke({"question": "What is quantum computing?"})
# print(f"Answer: {result2['answer']}")