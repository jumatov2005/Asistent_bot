import os

# Railway va lokal uchun universal konfiguratsiya
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SUPER_ADMIN = int(os.environ.get("SUPER_ADMIN", 0))

# Database configuration
DB_USER = os.environ.get("PGUSER", "postgres")
DB_PASS = os.environ.get("PGPASSWORD", "password")
DB_NAME = os.environ.get("PGDATABASE", "railway")
DB_HOST = os.environ.get("PGHOST", "localhost")
DB_PORT = os.environ.get("PGPORT", "5432")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")
