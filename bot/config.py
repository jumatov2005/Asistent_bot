import os

# Railway va lokal uchun universal konfiguratsiya
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SUPER_ADMIN = int(os.environ.get("SUPER_ADMIN", 0))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")
