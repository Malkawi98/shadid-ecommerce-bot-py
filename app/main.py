# app/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles # If you add static CSS/JS later
from app.graph import bot_app, BotState # Import the compiled graph and state

# Load environment variables (like OPENAI_API_KEY)
load_dotenv()

# --- FastAPI App Setup ---
app = FastAPI(title="E-commerce Support Bot")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files (optional, for CSS/JS if not using CDN)
# app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main chat interface page."""
    return templates.TemplateResponse("index.html", {"request": request, "response": None, "message": None})

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    """Handles user input from the form, runs the graph, and returns the response."""
    print(f"Received message: {message}")

    # Prepare the initial state for the graph
    initial_state = BotState(input=message)

    # Invoke the LangGraph application
    # The config is optional but good practice, especially for tracing (e.g., with LangSmith)
    # from langchain_core.runnables import RunnableConfig
    # config = RunnableConfig(configurable={"thread_id": "user-session-1"}) # Example config
    final_state = bot_app.invoke(initial_state) # Add config=config if needed

    bot_response = final_state.get("output", "Sorry, something went wrong.")
    print(f"Bot response: {bot_response}")

    # Render the template again, passing the user message and bot response
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": message, # The user's last message
        "response": bot_response # The bot's reply
    })

# --- Run (for local development) ---
# Use uvicorn to run the app:
# uvicorn app.main:app --reload --port 8000