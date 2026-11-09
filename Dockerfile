FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# Install minimal OS packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements-dev.txt* ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# Standalone high-performance Instagram scraper microservice (curl_cffi TLS impersonation)
CMD ["python", "run.py"]
