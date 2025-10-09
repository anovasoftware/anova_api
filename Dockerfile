# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# System deps only if you need to compile some wheels; keep minimal otherwise
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Expose Django/Gunicorn port
EXPOSE 8000

# Run your bootstrap script; it will start the server
# (set START_SERVER=1 and USE_GUNICORN=1 in docker-compose)
CMD ["python", "docker_startup.py"]
