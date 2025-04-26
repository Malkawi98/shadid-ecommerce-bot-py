import re
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable, RunnableConfig
from app.knowledge_base import kb # Import the initialized kb instance
from app.mock_ecommerce_api import get_order_info
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class BotState(BaseModel):
    input: str
    chat_history: list = Field(default_factory=list) # To store conversation history
    output: Optional[str] = None
    next_node: Optional[str] = None # <-- ADD THIS FIELD to hold routing decision


# 1. Classifier Node
def classify_input(state: BotState) -> Dict[str, Any]:
    """Classifies the user input to determine the next step."""
    user_input = state.input.lower()
    order_match = re.search(r'\b(\d{5,})\b', user_input)

    if order_match:
        print("Classifier: Input classified as Order Inquiry.")
        return {"next_node": "order_info"} # This key will update BotState.next_node
    else:
        print("Classifier: Input classified as General Knowledge.")
        return {"next_node": "knowledge_base"} # This key will update BotState.next_node

# 2. Order Status Fetcher Node
def fetch_order_status(state: BotState) -> Dict[str, str]:
    """Fetches order status using the mock API."""
    user_input = state.input
    order_id_match = re.search(r'\b(\d{5,})\b', user_input)

    if order_id_match:
        order_id = order_id_match.group(1)
        print(f"Order Fetcher: Found Order ID {order_id}. Fetching info...")
        result = get_order_info(order_id)
        if result.get("status") == "Invalid Order ID format. Please provide numbers only.":
             output = result["status"]
        elif result.get("status") == "Order Not Found":
             output = f"Sorry, I couldn't find any order with the ID {order_id}."
        else:
            status = result.get('status', 'N/A')
            tracking = result.get('tracking')
            if tracking:
                output = f"Order {order_id} Status: {status}. Tracking: {tracking}"
            else:
                output = f"Order {order_id} Status: {status}. Tracking information not available yet."
    else:
        print("Order Fetcher: No Order ID found in input.")
        output = "Please provide your order ID (e.g., 'What is the status of order 12345?') so I can check its status."

    # Update the state dictionary with the 'output' key
    return {"output": output} # This key will update BotState.output

# 3. Knowledge Base Retriever Node
def retrieve_from_kb(state: BotState) -> Dict[str, str]:
    """Retrieves information from the knowledge base."""
    query = state.input
    print(f"KB Retriever: Searching for relevant info for: '{query}'")
    docs = kb.similarity_search(query, k=1)
    if docs:
        output = docs[0].page_content
        print(f"KB Retriever: Found relevant document.")
    else:
        output = "Sorry, I couldn't find specific information about that in my knowledge base. Could you try rephrasing your question?"
        print("KB Retriever: No relevant documents found.")

    # Update the state dictionary with the 'output' key
    return {"output": output} # This key will update BotState.output

# --- Graph Definition ---
workflow = StateGraph(BotState)

# Add nodes
workflow.add_node("classify", classify_input)
workflow.add_node("order_info", fetch_order_status)
workflow.add_node("knowledge_base", retrieve_from_kb)

# Set entry point
workflow.set_entry_point("classify")

workflow.add_conditional_edges(
    "classify",
    lambda state: state.next_node, # <-- CHANGE THIS: Use attribute access
    {
        "order_info": "order_info",
        "knowledge_base": "knowledge_base",
    }
)

workflow.add_edge("order_info", END)
workflow.add_edge("knowledge_base", END)

bot_app = workflow.compile()
