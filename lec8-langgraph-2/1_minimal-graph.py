from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict
import os
import dotenv
dotenv.load_dotenv()    

print("\n" + "="*80)
print("EXAMPLE 1: MINIMAL Q&A GRAPH")
print("="*80)

# Step 1: Define State
class QAState(TypedDict):
    question: str
    answer: str

# Step 2: Define Nodes (Python functions)
def input_node(state: QAState) -> QAState:
    """Store user question in state"""
    print(f"[INPUT NODE] Question: {state['question']}")
    return state

def answer_node(state: QAState) -> QAState:
    """Call LLM with question and write answer"""
    print(f"[ANSWER NODE] Processing question...")
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Call LLM
    response = llm.invoke(state["question"])
    
    return {"answer": response.content}

# Step 3: Build the Graph
workflow = StateGraph(QAState)

# Add nodes
workflow.add_node("input", input_node)
workflow.add_node("answer", answer_node)

# Add edges
workflow.add_edge("input", "answer")
workflow.add_edge("answer", END)

# Set entry point
workflow.set_entry_point("input")

# Compile
app = workflow.compile()

# Step 4: Run the Graph
result = app.invoke({"question": "What is LangGraph?"})
print(f"\nFinal Answer: {result['answer']}\n")

"""
Key Takeaways:
- State flows through nodes
- Each node returns partial updates
- Edges connect nodes in sequence
- END marks completion
"""