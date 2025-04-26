FROM python:3.9-slim

WORKDIR /app

# Install dependencies with retry mechanism for network issues
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout 100 --retries 3 -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Set environment variables for OpenAI
ENV OPENAI_API_TYPE=open_ai
ENV OPENAI_API_VERSION=2023-05-15

# Expose the port that the application will run on
EXPOSE 8005

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
