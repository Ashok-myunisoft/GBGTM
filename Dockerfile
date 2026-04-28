FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first so rebuilds cache better.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . .

# Expose the frontend port.
EXPOSE 9000

# Run the frontend API in this container.
CMD ["uvicorn", "frontend_ai:app", "--host", "0.0.0.0", "--port", "9000"]
