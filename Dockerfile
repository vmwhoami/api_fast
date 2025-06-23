FROM python:3-slim-bullseye

 
WORKDIR /app

# Debug: Show what files Docker can see
RUN echo "=== Docker build context contents ==="
COPY . /tmp/debug/
RUN ls -la /tmp/debug/
RUN echo "=== Looking for requirements.txt ==="
RUN find /tmp/debug/ -name "requirements.txt"

# Try to copy requirements.txt
COPY requirements.txt .
RUN echo "=== Successfully copied requirements.txt ==="
RUN ls -la requirements.txt

WORKDIR /app

# Install packages directly (no venv needed)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "=== Looking for requirements.txt ==="
RUN find /tmp/debug/ -name "requirements.txt"
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]