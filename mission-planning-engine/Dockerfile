FROM python:3.13-slim AS base

WORKDIR /app

# Install system deps for PostGIS client (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e ".[dashboard,tak,ais,db]" 2>/dev/null || \
    pip install --no-cache-dir -e "." && \
    pip install --no-cache-dir pytak pyais fastapi uvicorn || true

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "-m", "mpe"]
