FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first so rebuilds cache better.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . .

# Expose both ports used by the single-container setup.
EXPOSE 8007 9000

# Run the mock MCP backend and the frontend API in the same container.
# app.py listens on 8007, frontend_ai.py listens on 9000.
CMD ["sh", "-c", "python app.py & exec uvicorn frontend_ai:app --host 0.0.0.0 --port 9000"]
