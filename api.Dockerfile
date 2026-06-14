FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY logs_config.py .
COPY fastapi_db/ ./fastapi_db/
COPY db_model/ ./db_model/
COPY alembic/ ./alembic/
COPY alembic.ini .

#runnig migrations too
CMD ["sh", "-c", "alembic upgrade head && uvicorn fastapi_db.main_api:app --host 0.0.0.0 --port 8000"]
