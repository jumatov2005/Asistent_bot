from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from database.db import db
from states.states import AnonymousState, CommentState
from keyboards.reply import back_kb, main_user_kb, settings_kb, main_admin_kb
from keyboards.inline import reply_anon_kb, language_choice_kb
from texts import TEXTS

router = Router()

async def get_user_info(user_id):
    user = await db.get_user(user_id)
    if not user: return "uz", "user"
    return user["language"], user["role"]

def get_media_info(message: types.Message):
    if message.photo: return "photo", message.photo[-1].file_id, message.caption or ""
    elif message.video: return "video", message.video.file_id, message.caption or ""
    elif message.audio: return "audio", message.audio.file_id, message.caption or ""
    elif message.voice: return "voice", message.voice.file_id, message.caption or ""
    elif message.video_note: return "video_note", message.video_note.file_id, ""
    else: return "text", None, message.text or ""

# --- ANONIM XABAR ---
@router.message(F.text.in_([TEXTS["btn_anon_msg"]["uz"], TEXTS["btn_anon_msg"]["ru"], TEXTS["btn_anon_msg"]["en"]]))
async def ask_anon_message(message: types.Message, state: FSMContext):
    lang, role = await get_user_info(message.from_user.id)
    await message.answer(TEXTS["ask_anon_msg"][lang], reply_markup=back_kb(lang))
    await state.set_state(AnonymousState.message)

@router.message(AnonymousState.message)
async def send_anon_message(message: types.Message, state: FSMContext, bot: Bot):
    lang, role = await get_user_info(message.from_user.id)
    
    # Text back check
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_user"][lang], reply_markup=main_user_kb(lang))
        await state.clear()
        return

    msg_type, file_id, text_content = get_media_info(message)
    username = message.from_user.username or ("User " + str(message.from_user.id))
    
    # DB Save
    await db.add_anonymous_message(message.from_user.id, username, text_content, msg_type, file_id)
    
    try:
        await message.answer(TEXTS["anon_msg_sent"][lang], reply_markup=main_user_kb(lang))
    except: pass # User bloklagan bo'lsa
    
    await state.clear()
    
    # Notify Super Admins
    admins = await db.get_admins()
    for admin in admins:
        if admin["role"] == "super_admin":
            try:
                a_lang = admin["language"]
                type_name = TEXTS["media_type_caption"][a_lang].format(type=msg_type)
                caption = f"{type_name}\n\n{TEXTS['anon_msg_received'][a_lang].format(msg=text_content, username=username)}"
                kb = reply_anon_kb(message.from_user.id)
                
                if msg_type == "text":
                    await bot.send_message(admin["telegram_id"], caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "photo":
                    await bot.send_photo(admin["telegram_id"], file_id, caption=caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "video":
                    await bot.send_video(admin["telegram_id"], file_id, caption=caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "audio":
                    await bot.send_audio(admin["telegram_id"], file_id, caption=caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "voice":
                    await bot.send_voice(admin["telegram_id"], file_id, caption=caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "video_note":
                    await bot.send_video_note(admin["telegram_id"], file_id, reply_markup=kb)
            except Exception:
                pass


# --- PROFILE ---
@router.message(F.text.in_([TEXTS["btn_profile"]["uz"], TEXTS["btn_profile"]["ru"], TEXTS["btn_profile"]["en"]]))
async def show_profile(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    lang, role = user["language"], user["role"]
    text = TEXTS["profile_info"][lang].format(
        id=user["telegram_id"], name=user["first_name"], username=f"@{user['username']}" if user['username'] else "No", lang=lang, role=role
    )
    await message.answer(text, parse_mode="HTML")

# --- SETTINGS MENU ---
@router.message(F.text.in_([TEXTS["btn_settings"]["uz"], TEXTS["btn_settings"]["ru"], TEXTS["btn_settings"]["en"]]))
async def show_settings(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    lang, role = user["language"], user["role"]
    await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))

# --- CHANGE LANGUAGE ---
@router.message(F.text.in_([TEXTS["btn_change_lang"]["uz"], TEXTS["btn_change_lang"]["ru"], TEXTS["btn_change_lang"]["en"]]))
async def ask_change_lang(message: types.Message):
    await message.answer("Tilni tanlang / Выберите язык:", reply_markup=language_choice_kb())

@router.callback_query(F.data.startswith("lang_"))
async def change_lang_action(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    await db.update_user_language(user_id, lang_code)
    try: await callback.message.delete()
    except: pass
    
    await callback.message.answer(TEXTS["language_selected"][lang_code])
    
    user = await db.get_user(user_id)
    role = user["role"]
    
    if role == "user":
        await callback.message.answer(TEXTS["menu_main_user"][lang_code], reply_markup=main_user_kb(lang_code))
    else:
        await callback.message.answer(TEXTS["menu_main_admin"][lang_code], reply_markup=main_admin_kb(lang_code, role=="super_admin"))

# --- DONATE & CONTACT ---
@router.message(F.text.in_([TEXTS["btn_donate"]["uz"], TEXTS["btn_donate"]["ru"], TEXTS["btn_donate"]["en"]]))
async def show_donate(message: types.Message):
    lang, role = await get_user_info(message.from_user.id)
    await message.answer(TEXTS["donate_info"][lang], parse_mode="HTML")

@router.message(F.text.in_([TEXTS["btn_contact_admin"]["uz"], TEXTS["btn_contact_admin"]["ru"], TEXTS["btn_contact_admin"]["en"]]))
async def show_contact(message: types.Message):
    lang, role = await get_user_info(message.from_user.id)
    await message.answer(TEXTS["contact_info"][lang], parse_mode="HTML")

# --- FEEDBACK ---
@router.message(F.text.in_([TEXTS["btn_feedback"]["uz"], TEXTS["btn_feedback"]["ru"], TEXTS["btn_feedback"]["en"]]))
async def ask_feedback(message: types.Message, state: FSMContext):
    lang, role = await get_user_info(message.from_user.id)
    await message.answer(TEXTS["ask_feedback"][lang], reply_markup=back_kb(lang))
    await state.set_state(CommentState.text)

@router.message(CommentState.text)
async def save_feedback(message: types.Message, state: FSMContext):
    lang, role = await get_user_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))
        await state.clear()
        return
        
    msg_type, file_id, text_content = get_media_info(message)
    username = message.from_user.username or "No Username"
    
    await db.add_comment(message.from_user.id, role, username, text_content, msg_type, file_id)
    
    await message.answer(TEXTS["feedback_saved"][lang], reply_markup=settings_kb(lang, role))
    await state.clear()

# --- BACK ---
@router.message(F.text.in_([TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]))
async def go_back(message: types.Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    if not user: return
    lang, role = user["language"], user["role"]
    
    if role == "user":
        await message.answer(TEXTS["menu_main_user"][lang], reply_markup=main_user_kb(lang))
    else:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
