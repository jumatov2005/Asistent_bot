from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from database.db import db
from states.states import ReplyState, TechnicalWorkState
from keyboards.inline import reply_anon_kb
from keyboards.reply import main_admin_kb, back_kb, technical_works_kb, anon_filter_kb
from texts import TEXTS
import asyncio

router = Router()

def get_super_admin_info(user_id):
    user = db.get_user(user_id)
    if not user: return None, None
    return user["language"], user["role"]

def get_media_info(message: types.Message):
    if message.photo: return "photo", message.photo[-1].file_id, message.caption or ""
    elif message.video: return "video", message.video.file_id, message.caption or ""
    elif message.audio: return "audio", message.audio.file_id, message.caption or ""
    elif message.voice: return "voice", message.voice.file_id, message.caption or ""
    elif message.video_note: return "video_note", message.video_note.file_id, ""
    else: return "text", None, message.text or ""

# --- ANONIM XABARLAR BO'LIMI (MENU) ---
@router.message(F.text.in_([TEXTS["btn_anon_admin_view"]["uz"], TEXTS["btn_anon_admin_view"]["ru"], TEXTS["btn_anon_admin_view"]["en"]]))
async def view_anon_menu(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    await message.answer(TEXTS["anon_menu_title"][lang], reply_markup=anon_filter_kb(lang))


# --- ANONIM XABARLARNI KO'RISH (HANDLERS) ---
@router.message(lambda msg: msg.text and any(txt in msg.text for txt in ["1 kunlik", "1 день", "1 day", "1 haftalik", "1 неделя", "1 week", "1 oylik", "1 месяц", "1 month"]))
async def view_filtered_anon_msgs(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    if role != "super_admin": return

    text = message.text
    # Determine filter type based on button text
    f_type = "1_month" # default
    if text in [TEXTS["anon_1_day"]["uz"], TEXTS["anon_1_day"]["ru"], TEXTS["anon_1_day"]["en"]]:
        f_type = "1_day_new"
    elif text in [TEXTS["anon_1_week"]["uz"], TEXTS["anon_1_week"]["ru"], TEXTS["anon_1_week"]["en"]]:
        f_type = "1_week"
    elif text in [TEXTS["anon_1_month"]["uz"], TEXTS["anon_1_month"]["ru"], TEXTS["anon_1_month"]["en"]]:
        f_type = "1_month"
        
    msgs = db.get_filtered_anonymous_messages(f_type)
    
    if not msgs:
        await message.answer(TEXTS["anon_no_messages"][lang])
        return

    ids_to_mark = []
    
    for m in msgs:
        # DB Row access
        m_id = m['id']
        sender_id = m['sender_telegram_id'] 
        sender = m['sender_username']
        text_content = m['message']
        msg_type = m['message_type']
        file_id = m['file_id']
        date = m['created_at']
        
        type_caption = TEXTS["media_type_caption"][lang].format(type=msg_type)
        display_text = TEXTS["anon_msg_format"][lang].format(
            id=m_id, date=date, sender=sender, msg=text_content
        )
        full_caption = f"{type_caption}\n\n{display_text}"
        
        kb = reply_anon_kb(sender_id)
        
        try:
            if msg_type == "text":
                await message.answer(full_caption, reply_markup=kb, parse_mode="HTML")
            else:
                if msg_type == "photo": await message.answer_photo(file_id, caption=full_caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "video": await message.answer_video(file_id, caption=full_caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "audio": await message.answer_audio(file_id, caption=full_caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "voice": await message.answer_voice(file_id, caption=full_caption, reply_markup=kb, parse_mode="HTML")
                elif msg_type == "video_note": await message.answer_video_note(file_id, reply_markup=kb)
            
            ids_to_mark.append(m_id)
            await asyncio.sleep(0.05) # Prevent flood
            
        except Exception as e:
            await message.answer(f"Error msg {m_id}: {e}")

    # Mark as read (faqat 1 kunlik yangi bo'lsa yoki umumiy ko'rilganda ham read qilish kerakmi? Prompt "ko'rilganda read = true" degan)
    if ids_to_mark:
        db.mark_anonymous_messages_read(ids_to_mark)


# --- DELETE READ ANON MESSAGES ---
@router.message(F.text.in_([TEXTS["anon_delete_read"]["uz"], TEXTS["anon_delete_read"]["ru"], TEXTS["anon_delete_read"]["en"]]))
async def delete_read_anon_msgs(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    db.delete_read_anonymous_messages()
    await message.answer(TEXTS["anon_deleted_success"][lang])

# --- ANON BACK ---
@router.message(F.text.in_([TEXTS["anon_back"]["uz"], TEXTS["anon_back"]["ru"], TEXTS["anon_back"]["en"]]))
async def anon_back_action(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    if role != "super_admin": return
    # Back to Main Admin Panel
    await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, True))


# --- REPLY ANON CALLBACK (Existing Logic) ---
@router.callback_query(F.data.startswith("reply_anon_"))
async def reply_anon_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        sender_id = int(callback.data.split("_")[2])
    except (IndexError, ValueError):
        await callback.answer("Error")
        return

    lang, role = get_super_admin_info(callback.from_user.id)
    if role != "super_admin": return

    await state.update_data(receiver_id=sender_id)
    await callback.message.answer(TEXTS["ask_reply"][lang], reply_markup=back_kb(lang))
    await state.set_state(ReplyState.answer)
    await callback.answer()

@router.message(ReplyState.answer)
async def send_reply_anon(message: types.Message, state: FSMContext, bot: Bot):
    lang, role = get_super_admin_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, True))
        await state.clear()
        return

    data = await state.get_data()
    receiver_id = data.get("receiver_id")
    msg_type, file_id, caption = get_media_info(message)
    
    try:
        receiver_user = db.get_user(receiver_id)
        if receiver_user:
            r_lang = receiver_user["language"]
            header = TEXTS["reply_received"][r_lang].format(msg="")
            
            if msg_type == "text":
                 await bot.send_message(receiver_id, header + caption, parse_mode="HTML")
            else:
                 await message.copy_to(receiver_id, caption=header+caption, parse_mode="HTML")

            db.add_reply_log(receiver_id, caption, msg_type, file_id)
            await message.answer(TEXTS["reply_sent"][lang], reply_markup=main_admin_kb(lang, True))
        else:
            await message.answer(TEXTS["error_user_not_found"][lang])
    except Exception as e:
        await message.answer(f"Error: {e}")
    
    await state.clear()

# --- TECH WORKS (Existing Logic) ---
@router.message(F.text.in_([TEXTS["btn_tech_works"]["uz"], TEXTS["btn_tech_works"]["ru"], TEXTS["btn_tech_works"]["en"]]))
async def tech_works_menu(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    if role != "super_admin": return
    await message.answer(TEXTS["tech_menu_title"][lang], reply_markup=technical_works_kb(lang))

@router.message(F.text.in_([TEXTS["btn_tech_maintenance_on"]["uz"], TEXTS["btn_tech_maintenance_on"]["ru"], TEXTS["btn_tech_maintenance_on"]["en"]]))
async def enable_maintenance(message: types.Message):
    lang, role = get_super_admin_info(message.from_user.id)
    db.set_maintenance_mode(True)
    await message.answer(TEXTS["maintenance_enabled"][lang], reply_markup=technical_works_kb(lang))

@router.message(F.text.in_([TEXTS["btn_tech_maintenance_off"]["uz"], TEXTS["btn_tech_maintenance_off"]["ru"], TEXTS["btn_tech_maintenance_off"]["en"]]))
async def disable_maintenance(message: types.Message, bot: Bot):
    lang, role = get_super_admin_info(message.from_user.id)
    db.set_maintenance_mode(False)
    await message.answer(TEXTS["maintenance_disabled"][lang], reply_markup=technical_works_kb(lang))
    
    ids = db.get_all_user_ids()
    for uid in ids:
        try: await bot.send_message(uid, TEXTS["maintenance_deactive_msg"][lang]) 
        except: pass

@router.message(F.text.in_([TEXTS["btn_tech_news"]["uz"], TEXTS["btn_tech_news"]["ru"], TEXTS["btn_tech_news"]["en"]]))
async def ask_tech_news(message: types.Message, state: FSMContext):
    lang, role = get_super_admin_info(message.from_user.id)
    await message.answer(TEXTS["ask_tech_broadcast_msg"][lang], reply_markup=back_kb(lang))
    await state.set_state(TechnicalWorkState.ask_news)

@router.message(TechnicalWorkState.ask_news)
async def send_tech_news(message: types.Message, state: FSMContext, bot: Bot):
    lang, role = get_super_admin_info(message.from_user.id)
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, True))
        await state.clear()
        return

    ids = db.get_all_user_ids()
    count = 0
    for uid in ids:
        try:
            await message.copy_to(uid)
            count += 1
            await asyncio.sleep(0.05)
        except: pass
            
    await message.answer(TEXTS["broadcast_ended"][lang].format(total=count), reply_markup=main_admin_kb(lang, True))
    await state.clear()
