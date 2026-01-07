from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from database.db import db
from states.states import AdminManageState, BroadcastState
from keyboards.reply import back_kb, main_admin_kb, broadcast_target_kb, settings_kb, comments_filter_kb
from texts import TEXTS
import asyncio

router = Router()

def get_admin_info(user_id):
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

# --- STATS ---
@router.message(F.text.in_([TEXTS["btn_users"]["uz"], TEXTS["btn_users"]["ru"], TEXTS["btn_users"]["en"]]))
async def show_stats(message: types.Message):
    lang, role = get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return # Security check

    stats = db.get_stats()
    text = TEXTS["stats_info"][lang].format(
        users=stats["users"], admins=stats["admins"], total=stats["total"]
    )
    await message.answer(text, parse_mode="HTML")

# --- BROADCAST ---
@router.message(F.text.in_([TEXTS["btn_broadcast"]["uz"], TEXTS["btn_broadcast"]["ru"], TEXTS["btn_broadcast"]["en"]]))
async def ask_broadcast_target(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return
    
    await message.answer(TEXTS["select_broadcast_target"][lang], reply_markup=broadcast_target_kb(lang))
    await state.set_state(BroadcastState.ask_target)

@router.message(BroadcastState.ask_target)
async def ask_broadcast_message(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    text = message.text
    
    if text and text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
        await state.clear()
        return
        
    target = ""
    # Safe text comparison
    if text == TEXTS["broadcast_all"][lang]: target = "all"
    elif text == TEXTS["broadcast_admins"][lang]: target = "admins"
    else: return 

    await state.update_data(target=target)
    await message.answer(TEXTS["ask_broadcast_msg"][lang], reply_markup=back_kb(lang))
    await state.set_state(BroadcastState.ask_message)

@router.message(BroadcastState.ask_message)
async def run_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    lang, role = get_admin_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
        await state.clear()
        return

    data = await state.get_data()
    target = data.get("target")
    
    await message.answer(TEXTS["broadcast_started"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
    
    if target == "all": receivers = db.get_all_user_ids()
    else: receivers = db.get_admin_ids()
        
    count = 0
    msg_type, file_id, caption = get_media_info(message)
    
    # Batch processing or optimize later
    for chat_id in receivers:
        try:
            await message.copy_to(chat_id)
            count += 1
            await asyncio.sleep(0.05) # Prevent flood wait
        except: pass
            
    db.add_broadcast_log(message.from_user.id, target, msg_type, file_id, caption, count)
    
    await message.answer(TEXTS["broadcast_ended"][lang].format(total=count))
    await state.clear()

# --- COMMENTS VIEW ---
@router.message(F.text.in_([TEXTS["btn_comments"]["uz"], TEXTS["btn_comments"]["ru"], TEXTS["btn_comments"]["en"]]))
async def view_comments_menu(message: types.Message):
    lang, role = get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return
    
    # Comments filter kb needs is_super flag
    await message.answer(TEXTS["comments_filter_title"][lang], reply_markup=comments_filter_kb(lang, role=="super_admin"))

@router.message(lambda msg: msg.text and any(txt in msg.text for txt in ["1 kunlik", "1 день", "1 day", "1 haftalik", "1 неделя", "1 week", "1 oylik", "1 месяц", "1 month"]))
async def filter_comments_action(message: types.Message):
    lang, role = get_admin_info(message.from_user.id)
    text = message.text
    
    # Robust logic
    f_type = "default"
    if "1 kun" in text or "1 ден" in text or "1 day" in text: f_type = "1_day_new"
    elif "1 haf" in text or "1 нед" in text or "1 week" in text: f_type = "1_week"
    elif "1 oyl" in text or "1 мес" in text or "1 month" in text: f_type = "1_month"
    
    comments = db.get_filtered_comments(f_type)
    
    if not comments:
        await message.answer(TEXTS["no_comments"][lang])
        return
    
    ids_to_mark = []
    for c in comments:
        # Access by name via Row!
        c_type = c["message_type"]
        display_role = "Admin" if c["sender_role"] in ["admin", "super_admin"] else "User"
        display_text = TEXTS["comment_format"][lang].format(
            role=display_role, username=c["sender_username"], msg=c["comment"] + (f" [{c_type}]" if c_type!="text" else ""), date=c["created_at"]
        )
        
        if c_type == "text":
            await message.answer(display_text, parse_mode="HTML")
        else:
             file_id = c["file_id"]
             try:
                 if c_type == "photo": await message.answer_photo(file_id, caption=display_text, parse_mode="HTML")
                 elif c_type == "video": await message.answer_video(file_id, caption=display_text, parse_mode="HTML")
                 elif c_type == "audio": await message.answer_audio(file_id, caption=display_text, parse_mode="HTML")
                 elif c_type == "voice": await message.answer_voice(file_id, caption=display_text, parse_mode="HTML")
             except:
                 await message.answer(display_text + "\n(Media not available)", parse_mode="HTML")
        
        ids_to_mark.append(c["id"])
        await asyncio.sleep(0.1)

    db.mark_comments_read(ids_to_mark)

@router.message(F.text.in_([TEXTS["btn_del_read_comments"]["uz"], TEXTS["btn_del_read_comments"]["ru"], TEXTS["btn_del_read_comments"]["en"]]))
async def delete_read_comments(message: types.Message):
    lang, role = get_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    db.delete_read_comments()
    await message.answer(TEXTS["comments_deleted"][lang])

# --- ADMIN MANAGEMENT ---
@router.message(F.text.in_([TEXTS["btn_list_admin"]["uz"], TEXTS["btn_list_admin"]["ru"], TEXTS["btn_list_admin"]["en"]]))
async def list_admins(message: types.Message):
    lang, role = get_admin_info(message.from_user.id)
    admins = db.get_admins()
    if not admins:
        await message.answer(TEXTS["admin_list_empty"][lang])
        return
    msg = TEXTS["admin_list_header"][lang]
    for adm in admins: 
        msg += f"👤 @{adm['username']} (ID: {adm['telegram_id']}) - {adm['role']}\n"
    await message.answer(msg, parse_mode="HTML")

@router.message(F.text.in_([TEXTS["btn_add_admin"]["uz"], TEXTS["btn_add_admin"]["ru"], TEXTS["btn_add_admin"]["en"]]))
async def add_admin_ask(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    await message.answer(TEXTS["ask_admin_username"][lang], reply_markup=back_kb(lang))
    await state.set_state(AdminManageState.add_admin)

@router.message(AdminManageState.add_admin)
async def add_admin_action(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))
        await state.clear()
        return

    target_user = db.get_user_by_username(message.text)
    if target_user:
        # Check integrity
        db.update_user_role(target_user["telegram_id"], "admin")
        await message.answer(TEXTS["admin_added"][lang].format(username=target_user["username"]))
    else:
        await message.answer(TEXTS["user_not_found"][lang])
    await state.clear()
    await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))

@router.message(F.text.in_([TEXTS["btn_del_admin"]["uz"], TEXTS["btn_del_admin"]["ru"], TEXTS["btn_del_admin"]["en"]]))
async def del_admin_ask(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    await message.answer(TEXTS["ask_del_admin_username"][lang], reply_markup=back_kb(lang))
    await state.set_state(AdminManageState.delete_admin)

@router.message(AdminManageState.delete_admin)
async def del_admin_action(message: types.Message, state: FSMContext):
    lang, role = get_admin_info(message.from_user.id)
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))
        await state.clear()
        return
        
    username = message.text.replace("@", "")
    success = db.downgrade_admin(username)
    if success: await message.answer(TEXTS["admin_deleted"][lang].format(username=username))
    else: await message.answer(TEXTS["user_not_found"][lang])
    await state.clear()
    await message.answer(TEXTS["btn_settings"][lang], reply_markup=settings_kb(lang, role))
