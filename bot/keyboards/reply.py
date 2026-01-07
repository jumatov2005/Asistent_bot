from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import TEXTS

def main_user_kb(lang: str = "uz"):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TEXTS["btn_anon_msg"][lang])],
        [KeyboardButton(text=TEXTS["btn_profile"][lang]), KeyboardButton(text=TEXTS["btn_settings"][lang])]
    ], resize_keyboard=True)

def main_admin_kb(lang: str = "uz", is_super: bool = False):
    keyboard = [
        [KeyboardButton(text=TEXTS["btn_users"][lang]), KeyboardButton(text=TEXTS["btn_broadcast"][lang])],
        [KeyboardButton(text=TEXTS["btn_comments"][lang]), KeyboardButton(text=TEXTS["btn_settings"][lang])]
    ]
    if is_super:
        keyboard.insert(0, [KeyboardButton(text=TEXTS["btn_anon_admin_view"][lang])])
        # Texnik ishlar
        keyboard.insert(3, [KeyboardButton(text=TEXTS["btn_tech_works"][lang])])
        
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def settings_kb(lang: str = "uz", role: str = "user"):
    rows = []
    rows.append([KeyboardButton(text=TEXTS["btn_change_lang"][lang])])
    
    if role == "user":
        rows.append([KeyboardButton(text=TEXTS["btn_contact_admin"][lang]), KeyboardButton(text=TEXTS["btn_donate"][lang])])
        rows.append([KeyboardButton(text=TEXTS["btn_feedback"][lang])])
    elif role in ["admin", "super_admin"]:
        rows.append([KeyboardButton(text=TEXTS["btn_add_admin"][lang]), KeyboardButton(text=TEXTS["btn_del_admin"][lang])])
        rows.append([KeyboardButton(text=TEXTS["btn_list_admin"][lang])])
    
    rows.append([KeyboardButton(text=TEXTS["btn_back"][lang])])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def back_kb(lang: str = "uz"):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TEXTS["btn_back"][lang])]
    ], resize_keyboard=True)

def broadcast_target_kb(lang: str = "uz"):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TEXTS["broadcast_all"][lang]), KeyboardButton(text=TEXTS["broadcast_admins"][lang])],
        [KeyboardButton(text=TEXTS["btn_back"][lang])]
    ], resize_keyboard=True)

# --- NEW KEYBOARDS ---

def technical_works_kb(lang: str = "uz"):
    """Valid only for Super Admin"""
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TEXTS["btn_tech_news"][lang])],
        [KeyboardButton(text=TEXTS["btn_tech_maintenance_on"][lang]), KeyboardButton(text=TEXTS["btn_tech_maintenance_off"][lang])],
        [KeyboardButton(text=TEXTS["btn_back"][lang])]
    ], resize_keyboard=True)

def comments_filter_kb(lang: str = "uz", is_super: bool = False):
    rows = [
        [KeyboardButton(text=TEXTS["btn_filter_1_day"][lang]), KeyboardButton(text=TEXTS["btn_filter_1_week"][lang])],
        [KeyboardButton(text=TEXTS["btn_filter_1_month"][lang])]
    ]
    if is_super:
        rows.append([KeyboardButton(text=TEXTS["btn_del_read_comments"][lang])])
    
    rows.append([KeyboardButton(text=TEXTS["btn_back"][lang])])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def anon_filter_kb(lang: str = "uz"):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=TEXTS["anon_1_day"][lang]), KeyboardButton(text=TEXTS["anon_1_week"][lang])],
        [KeyboardButton(text=TEXTS["anon_1_month"][lang])],
        [KeyboardButton(text=TEXTS["anon_delete_read"][lang])],
        [KeyboardButton(text=TEXTS["anon_back"][lang])]
    ], resize_keyboard=True)
