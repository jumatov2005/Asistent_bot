from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    language = State()

class AnonymousState(StatesGroup):
    message = State()

class CommentState(StatesGroup):
    text = State() # User fikri uchun

class BroadcastState(StatesGroup):
    ask_target = State() # Kimga (all/admin)
    ask_message = State() # Xabar matni

class AdminManageState(StatesGroup):
    add_admin = State()
    delete_admin = State()

class ReplyState(StatesGroup):
    answer = State()
    receiver_id = State() # Bu state da saqlanadi, handlerda update_data qilinadi

class SettingsState(StatesGroup):
    change_lang = State()

class TechnicalWorkState(StatesGroup):
    ask_news = State()
