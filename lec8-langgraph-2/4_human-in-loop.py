from langgraph.checkpoint.memory import MemorySaver
import os
import dotenv
dotenv.load_dotenv()

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

class HumanReviewState(TypedDict):
    question: str
    proposed_action: str
    approved: bool
    result: str

def propose_action(state: HumanReviewState) -> HumanReviewState:
    """Propose an action that needs approval"""
    action = f"Delete file based on: {state['question']}"
    print(f"[PROPOSE] Action: {action}")
    return {"proposed_action": action}

def execute_action(state: HumanReviewState) -> HumanReviewState:
    """Execute approved action"""
    print(f"[EXECUTE] Running: {state['proposed_action']}")
    return {"result": "Action completed successfully"}

def cancel_action(state: HumanReviewState) -> HumanReviewState:
    """Cancel if not approved"""
    return {"result": "Action cancelled by user"}

def route_approval(state: HumanReviewState) -> Literal["execute", "cancel"]:
    """Route based on approval"""
    return "execute" if state.get("approved", False) else "cancel"

# Build human-in-loop graph
human_workflow = StateGraph(HumanReviewState)

human_workflow.add_node("propose", propose_action)
human_workflow.add_node("execute", execute_action)
human_workflow.add_node("cancel", cancel_action)

human_workflow.add_conditional_edges(
    "propose",
    route_approval,
    {
        "execute": "execute",
        "cancel": "cancel"
    }
)

human_workflow.add_edge("execute", END)
human_workflow.add_edge("cancel", END)
human_workflow.set_entry_point("propose")

# Use checkpointer for interrupts
memory = MemorySaver()
# Interrupt AFTER the 'propose' node to inspect and approve
human_app = human_workflow.compile(checkpointer=memory, interrupt_after=["propose"])

# Run the graph up to approval
config = {"configurable": {"thread_id": "1"}}
print("\n--- Starting Workflow ---")
result = human_app.invoke({"question": "Delete logs"}, config)

# The graph has paused after 'propose'.
# We can inspect the state to see what was proposed.
snapshot = human_app.get_state(config)
proposed_action = snapshot.values.get("proposed_action")
print(f"\n[SYSTEM] Paused. Current state snapshot: {snapshot.values}")

# Get user input
user_input = input(f"\nDo you approve the action '{proposed_action}'? (y/n): ").strip().lower()

if user_input == 'y':
    print("[USER] Approved.")
    # Update state with approval
    human_app.update_state(config, {"approved": True})
else:
    print("[USER] Denied.")
    # Update state with denial
    human_app.update_state(config, {"approved": False})

# Resume execution
print("\n--- Resuming Workflow ---")
# Passing None as input resumes from the suspended state
final_result = human_app.invoke(None, config)
print(f"\nFinal Result: {final_result.get('result')}\n")