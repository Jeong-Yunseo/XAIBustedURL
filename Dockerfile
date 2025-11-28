FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1 \
	HF_HOME=/root/.cache/huggingface

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	git \
	&& pip install --no-cache-dir pytest \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV KAFKA_BROKER=kafka:9092 \
	REDIS_HOST=redis \
	REDIS_PORT=6379 \
	CELERY_BROKER_URL=redis://redis:6379/0 \
	CELERY_RESULT_BACKEND=redis://redis:6379/1

CMD ["python", "src/main.py"]
