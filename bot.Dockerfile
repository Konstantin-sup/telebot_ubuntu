FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main_bot.py .
COPY logs_config.py .
COPY main_bot_package/ ./main_bot_package/
COPY db_model/ ./db_model/

RUN mkdir -p /app/data

CMD ["python", "main_bot.py"]
