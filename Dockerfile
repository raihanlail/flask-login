FROM python:3.11-slim

WORKDIR /app

ENV HOST=0.0.0.0

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir flask \
    && pip install --no-cache-dir pydantic[email]

COPY . .

EXPOSE 8080

CMD ["python3", "app.py"]