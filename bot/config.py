import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Bot tokenini olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Super admin ID sini olish (int ga o'tkazish)
try:
    SUPER_ADMIN_ID = int(os.getenv("SUPER_ADMIN_ID"))
except (TypeError, ValueError):
    # Agar .env da xato bo'lsa yoki yo'q bo'lsa, xatolik chiqmasligi uchun 0 qo'yamiz
    SUPER_ADMIN_ID = 0
