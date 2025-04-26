# E-commerce Support Bot

A FastAPI-based e-commerce support chatbot built with LangGraph that can answer product questions and check order statuses.

## Project Structure

- `app/main.py`: FastAPI application entry point
- `app/graph.py`: LangGraph workflow definition
- `app/knowledge_base.py`: Vector store for product knowledge
- `app/mock_ecommerce_api.py`: Mock API for order information
- `templates/index.html`: Chat interface
- `knowledge_base.txt`: Product information for the bot
- `requirements.txt`: Python dependencies

## Features

- Order status lookup by order ID
- Product knowledge base for general inquiries
- Simple web interface using Tailwind CSS

## Prerequisites

- Docker and Docker Compose
- OpenAI API key (for embeddings)

## Deployment with Docker

1. Set your OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

2. Build and start the Docker container:

```bash
docker-compose up -d
```

3. Access the application at http://localhost:8000

## Development

To run the application locally without Docker:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload --port 8000
```

## Docker Commands

- Build the Docker image:
```bash
docker build -t ecommerce-bot .
```

- Run the container:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here ecommerce-bot
```

- Stop the container:
```bash
docker-compose down
```
