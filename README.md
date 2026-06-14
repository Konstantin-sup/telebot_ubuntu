# 📁 Telegram File Bot

A Telegram bot for saving, browsing, and deleting your files — built with Python, Telebot, and FastAPI.

## What it does

- **Save** text, documents, photos, videos, audio, voice messages, and video notes (circles)
- **Browse** files organized by month and date folders
- **Retrieve** files directly in the chat
- **Delete** files or entire albums with confirmation
- **Track storage** — each user has a 250 MB quota

## Tech Stack

- **Python** — core language
- **pyTelegramBotAPI (Telebot)** — Telegram bot
- **FastAPI** — internal REST API for DB operations
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **MySQL** — database
- **Docker / Docker Compose** — containerization
- **python-dotenv** — environment config

## Project Structure

```
├── main_bot.py                  # Telegram bot entry point
├── fastapi_db/
│   └── main_api.py              # FastAPI REST API
├── db_model/
│   ├── main_table_model.py      # File metadata model
│   ├── user_quota_model.py      # User storage quota model
│   ├── api_functions.py         # DB queries + HTTP client
│   ├── engine_session.py        # SQLAlchemy engine & session
│   └── declarative_base.py      # Base class
├── main_bot_package/
│   ├── telebot_functions.py     # Keyboard/button helpers
│   └── file_date_functions.py   # File save/read/delete logic
├── alembic/                     # DB migration history
├── Dockerfile.bot               # Dockerfile for the bot
├── Dockerfile.api               # Dockerfile for the API
├── docker-compose.yml           # Orchestration
└── .env.example                 # Environment variables template
```

## Database Schema

**`main_table`** — stores file metadata per user:

| Column | Type | Description |
|---|---|---|
| `file_id` | BIGINT PK | Auto-increment |
| `user_id` | VARCHAR | Telegram user ID |
| `file_path` | VARCHAR UNIQUE | Path on disk |
| `file_name` | VARCHAR | File name |
| `file_type` | VARCHAR | photo / video / audio / document / text |
| `file_size` | BIGINT | Size in bytes |
| `tele_file_id` | VARCHAR | Telegram file ID (for resending) |
| `month_dir` | VARCHAR | Month folder name |
| `date_dir` | VARCHAR | Date folder name |
| `date_creation` | DateTime | Upload timestamp |
| `media_group_id` | VARCHAR | Album group ID (nullable) |
| `media_group_name` | VARCHAR | Album display name (nullable) |

**`user_quota`** — tracks used storage per user.

## Deploy with Docker

### Requirements
- Docker
- Docker Compose

### Steps

**1. Clone the repo:**
```bash
git clone <repo-url>
cd <repo>
```

**2. Create the `.env` file:**
```bash
cp .env.example .env
```

Fill in the values:
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here

# MySQL
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=filebot_db
MYSQL_USER=filebot_user
MYSQL_PASSWORD=your_password

# Path inside the container where files will be stored
PATH_TO_DATA=/app/data
```

**3. Create the data folder** (will be mounted into the bot container):
```bash
mkdir data
```

**4. Run:**
```bash
docker compose up --build -d
```

That's it. Docker will:
- Start MySQL and wait until it's healthy
- Run Alembic migrations automatically
- Start the FastAPI server
- Start the bot

### Useful commands

```bash
# View logs
docker compose logs -f

# Stop all containers
docker compose down

# Rebuild after code changes
docker compose up --build -d
```

---

## Local Setup (without Docker)

1. Clone the repo and create a virtual environment:
```bash
git clone <repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
API_URL=http://127.0.0.1:8000
PATH_TO_DATA=/path/to/data/directory
```

3. Run migrations:
```bash
alembic upgrade head
```

4. Start the FastAPI server:
```bash
uvicorn fastapi_db.main_api:app --reload
```

5. Start the bot:
```bash
python main_bot.py
```

---

## File size limits

- Max file size per upload: **15 MB**
- Max storage per user: **250 MB**

## Supported file types

| Type | Formats |
|---|---|
| Text | plain text messages |
| Document | any file format |
| Photo | .jpg |
| Video | .mp4 |
| Video note | .mp4 (circles) |
| Audio | .mp3 |
| Voice | .ogg |
| Album | group of photos/videos |


