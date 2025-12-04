import os
import dotenv
dotenv.load_dotenv()

from typing import TypedDict, List, Dict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

print("\n" + "="*80)
print("EXAMPLE 4: LOOP WITH RETRY LOGIC")
print("="*80)

class LoopState(TypedDict):
    question: str
    search_results: List[Dict]
    attempts: int
    enough_results: bool
    summary: str

def search_with_attempts(state: LoopState) -> LoopState:
    """Search and track attempts"""
    attempts = state.get("attempts", 0) + 1
    print(f"[SEARCH] Attempt {attempts}")
    
    # Simulate varying results
    if attempts == 1:
        results = [{"title": "Result 1", "snippet": "Some info"}]
        enough = False
    else:
        results = [
            {"title": "Result 1", "snippet": "Some info"},
            {"title": "Result 2", "snippet": "More info"},
            {"title": "Result 3", "snippet": "Even more info"}
        ]
        enough = len(results) >= 3
    
    return {
        "search_results": results,
        "attempts": attempts,
        "enough_results": enough
    }

def summarize_results(state: LoopState) -> LoopState:
    """Create summary from results"""
    summary = f"Found {len(state['search_results'])} results after {state['attempts']} attempts."
    return {"summary": summary}

def fallback_node(state: LoopState) -> LoopState:
    """Fallback when max attempts reached"""
    return {"summary": f"Could not find enough results after {state['attempts']} attempts."}

# Routing function for loop
def should_continue_searching(state: LoopState) -> Literal["summarize", "search", "fallback"]:
    """Decide whether to continue, summarize, or fallback"""
    max_attempts = 3
    
    if state.get("enough_results", False):
        return "summarize"
    elif state.get("attempts", 0) >= max_attempts:
        return "fallback"
    else:
        return "search"

# Build loop graph
loop_workflow = StateGraph(LoopState)

loop_workflow.add_node("search", search_with_attempts)
loop_workflow.add_node("summarize", summarize_results)
loop_workflow.add_node("fallback", fallback_node)

# Conditional edge with loop back
loop_workflow.add_conditional_edges(
    "search",
    should_continue_searching,
    {
        "search": "search",  # Loop back!
        "summarize": "summarize",
        "fallback": "fallback"
    }
)

loop_workflow.add_edge("summarize", END)
loop_workflow.add_edge("fallback", END)
loop_workflow.set_entry_point("search")

loop_app = loop_workflow.compile()

# Run
result = loop_app.invoke({"question": "Test loop"})
print(f"\nResult: {result['summary']}")
print(f"Total attempts: {result['attempts']}\n")