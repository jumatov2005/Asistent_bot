from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from database.db import db
from states.states import RegisterState
from keyboards.inline import language_choice_kb
from keyboards.reply import main_user_kb, main_admin_kb
from texts import TEXTS
from config import SUPER_ADMIN_ID

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """
    /start bosganda
    """
    await state.clear() # Har doim state tozalanadi
    
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if user:
        # Dictionary access via sqlite3.Row
        lang = user["language"]
        role = user["role"]
        
        # Super admin check sync
        if user_id == SUPER_ADMIN_ID and role != "super_admin":
            db.update_user_role(user_id, "super_admin")
            role = "super_admin"

        try:
            greeting = TEXTS["greeting_registered"][lang]
            await message.answer(greeting)
            
            if role == "user":
                await message.answer(TEXTS["menu_main_user"][lang], reply_markup=main_user_kb(lang))
            else:
                await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
        except Exception as e:
            # Fallback agar userda lang noto'g'ri bo'lsa
            await message.answer(TEXTS["greeting_registered"]["uz"])
    else:
        # User yo'q -> Ro'yxatdan o'tish
        await message.answer(TEXTS["start_welcome"]["uz"], reply_markup=language_choice_kb())
        await state.set_state(RegisterState.language)

@router.callback_query(RegisterState.language, F.data.startswith("lang_"))
async def register_language(callback: types.CallbackQuery, state: FSMContext):
    """
    Til tanlanganda
    """
    try:
        lang_code = callback.data.split("_")[1]
        user_id = callback.from_user.id
        username = callback.from_user.username or ""
        first_name = callback.from_user.first_name
        
        role = "user"
        if user_id == SUPER_ADMIN_ID:
            role = "super_admin"
            
        db.add_user(user_id, first_name, username, lang_code, role)
        
        await callback.message.delete()
        await callback.message.answer(TEXTS["language_selected"][lang_code])
        
        if role == "user":
            await callback.message.answer(TEXTS["menu_main_user"][lang_code], reply_markup=main_user_kb(lang_code))
        else:
            await callback.message.answer(TEXTS["menu_main_admin"][lang_code], reply_markup=main_admin_kb(lang_code, role=="super_admin"))
            
    except Exception as e:
        await callback.answer("Error processing request")
    finally:
        await state.clear()
