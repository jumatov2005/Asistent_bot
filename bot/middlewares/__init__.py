from .maintenance import MaintenanceMiddleware
from .throttling import ThrottlingMiddleware
from aiogram import Dispatcher

def setup(dp: Dispatcher):
    # Throttling eng oldin turishi kerak (spamni erta ushlash uchun)
    # Lekin Maintenance undan ham muhimroq bo'lishi mumkin.
    # Tartib: Maintenance -> Throttling
    
    dp.message.middleware(MaintenanceMiddleware())
    dp.callback_query.middleware(MaintenanceMiddleware())
    
    dp.message.middleware(ThrottlingMiddleware(limit=0.7))
    dp.callback_query.middleware(ThrottlingMiddleware(limit=0.7))
