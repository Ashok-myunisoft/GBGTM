FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies first so rebuilds cache better.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . .

# Expose both application ports.
EXPOSE 8007 8009

# Run both servers in the same container:
# - app.py on 8007
# - main.py on 8009
CMD ["sh", "-c", "python app.py & python main.py & wait"]
