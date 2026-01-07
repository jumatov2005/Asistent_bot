from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from database.db import db
from states.states import BroadcastState, AdminManageState
from keyboards.reply import main_admin_kb, back_kb, broadcast_target_kb, comments_filter_kb
from texts import TEXTS
import asyncio

router = Router()

async def get_admin_info(user_id):
    user = await db.get_user(user_id)
    if not user: return None, None
    return user["language"], user["role"]

def get_media_info(message: types.Message):
    if message.photo: return "photo", message.photo[-1].file_id, message.caption or ""
    elif message.video: return "video", message.video.file_id, message.caption or ""
    elif message.audio: return "audio", message.audio.file_id, message.caption or ""
    elif message.voice: return "voice", message.voice.file_id, message.caption or ""
    elif message.video_note: return "video_note", message.video_note.file_id, ""
    else: return "text", None, message.text or ""

# --- USERS LIST (Functionality? Just Stats for now) ---
@router.message(F.text.in_([TEXTS["btn_users"]["uz"], TEXTS["btn_users"]["ru"], TEXTS["btn_users"]["en"]]))
async def show_stats(message: types.Message):
    lang, role = await get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return
    
    stats = await db.get_stats()
    text = TEXTS["stats_info"][lang].format(
        users=stats["users"], admins=stats["admins"], total=stats["total"]
    )
    await message.answer(text, parse_mode="HTML")

# --- BROADCAST ---
@router.message(F.text.in_([TEXTS["btn_broadcast"]["uz"], TEXTS["btn_broadcast"]["ru"], TEXTS["btn_broadcast"]["en"]]))
async def ask_broadcast_target(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return
    
    await message.answer(TEXTS["select_broadcast_target"][lang], reply_markup=broadcast_target_kb(lang))
    await state.set_state(BroadcastState.ask_target)

@router.message(BroadcastState.ask_target)
async def ask_broadcast_message(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    
    if message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
        await state.clear()
        return

    target = "all"
    if message.text in [TEXTS["broadcast_admins"]["uz"], TEXTS["broadcast_admins"]["ru"], TEXTS["broadcast_admins"]["en"]]:
        target = "admins"
        
    await state.update_data(target=target)
    await message.answer(TEXTS["ask_broadcast_msg"][lang], reply_markup=back_kb(lang))
    await state.set_state(BroadcastState.ask_message)

@router.message(BroadcastState.ask_message)
async def run_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    lang, role = await get_admin_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, role=="super_admin"))
        await state.clear()
        return

    data = await state.get_data()
    target_group = data.get("target") # all / admins
    
    if target_group == "admins":
        users_ids = await db.get_admin_ids()
    else:
        users_ids = await db.get_all_user_ids()
        
    await message.answer(TEXTS["broadcast_started"][lang])
    
    count = 0
    msg_type, file_id, caption = get_media_info(message)
    
    for uid in users_ids:
        try:
            await message.copy_to(uid)
            count += 1
            await asyncio.sleep(0.05) # Flood wait
        except:
            pass
            
    # Log broadcast
    await db.add_broadcast_log(message.from_user.id, target_group, msg_type, file_id, caption, count)
    
    await message.answer(TEXTS["broadcast_ended"][lang].format(total=count), reply_markup=main_admin_kb(lang, role=="super_admin"))
    await state.clear()

# --- COMMENTS VIEW ---
@router.message(F.text.in_([TEXTS["btn_comments"]["uz"], TEXTS["btn_comments"]["ru"], TEXTS["btn_comments"]["en"]]))
async def view_comments(message: types.Message):
    lang, role = await get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return
    
    await message.answer(TEXTS["comments_filter_title"][lang], reply_markup=comments_filter_kb(lang, role=="super_admin"))

@router.message(lambda msg: msg.text and any(txt in msg.text for txt in ["1 kunlik", "1 день", "1 day", "1 haftalik", "1 неделя", "1 week", "1 oylik", "1 месяц", "1 month"]))
async def view_filtered_comments(message: types.Message):
    lang, role = await get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return

    text = message.text
    f_type = "1_month"
    if text in [TEXTS["btn_filter_1_day"]["uz"], TEXTS["btn_filter_1_day"]["ru"], TEXTS["btn_filter_1_day"]["en"]]:
        f_type = "1_day_new"
    elif text in [TEXTS["btn_filter_1_week"]["uz"], TEXTS["btn_filter_1_week"]["ru"], TEXTS["btn_filter_1_week"]["en"]]:
        f_type = "1_week"
        
    comments = await db.get_filtered_comments(f_type)
    if not comments:
        await message.answer(TEXTS["no_comments"][lang])
        return
        
    ids_to_mark = []
    
    for c in comments:
        c_id = c['id']
        username = c['sender_username']
        role_sender = c['sender_role']
        msg_type = c['message_type']
        file_id = c['file_id']
        comment_text = c['comment']
        date = c['created_at']
        
        display_text = TEXTS["comment_format"][lang].format(
            role=role_sender, username=username, msg=comment_text, date=date
        )
        
        try:
            if msg_type == "text":
                await message.answer(display_text, parse_mode="HTML")
            else:
                if msg_type == "photo": await message.answer_photo(file_id, caption=display_text, parse_mode="HTML")
                elif msg_type == "video": await message.answer_video(file_id, caption=display_text, parse_mode="HTML")
                elif msg_type == "audio": await message.answer_audio(file_id, caption=display_text, parse_mode="HTML")
                elif msg_type == "voice": await message.answer_voice(file_id, caption=display_text, parse_mode="HTML")
                elif msg_type == "video_note": await message.answer_video_note(file_id)
            
            ids_to_mark.append(c_id)
            await asyncio.sleep(0.05)
        except: pass

    if ids_to_mark:
        await db.mark_comments_read(ids_to_mark)


@router.message(F.text.in_([TEXTS["btn_del_read_comments"]["uz"], TEXTS["btn_del_read_comments"]["ru"], TEXTS["btn_del_read_comments"]["en"]]))
async def del_read_comments(message: types.Message):
    lang, role = await get_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    await db.delete_read_comments()
    await message.answer(TEXTS["comments_deleted"][lang])

# --- ADMIN MANAGEMENT ---
@router.message(F.text.in_([TEXTS["btn_list_admin"]["uz"], TEXTS["btn_list_admin"]["ru"], TEXTS["btn_list_admin"]["en"]]))
async def list_admins(message: types.Message):
    lang, role = await get_admin_info(message.from_user.id)
    if role not in ["admin", "super_admin"]: return

    admins = await db.get_admins()
    if not admins:
        await message.answer(TEXTS["admin_list_empty"][lang])
        return
        
    text = TEXTS["admin_list_header"][lang]
    for i, adm in enumerate(admins, 1):
        username = adm["username"] or str(adm["telegram_id"])
        # Ensure 'role' access is safe
        a_role = adm["role"]
        text += f"{i}. @{username} [{a_role}]\n"
        
    await message.answer(text)

@router.message(F.text.in_([TEXTS["btn_add_admin"]["uz"], TEXTS["btn_add_admin"]["ru"], TEXTS["btn_add_admin"]["en"]]))
async def ask_new_admin_username(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    await message.answer(TEXTS["ask_admin_username"][lang], reply_markup=back_kb(lang))
    await state.set_state(AdminManageState.ask_username_add)

@router.message(AdminManageState.ask_username_add)
async def add_new_admin(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, True))
        await state.clear()
        return

    username = message.text
    user = await db.get_user_by_username(username)
    
    if user:
        await db.update_user_role(user["telegram_id"], "admin")
        await message.answer(TEXTS["admin_added"][lang].format(username=username), reply_markup=main_admin_kb(lang, True))
    else:
        await message.answer(TEXTS["user_not_found"][lang])
        
    await state.clear()

@router.message(F.text.in_([TEXTS["btn_del_admin"]["uz"], TEXTS["btn_del_admin"]["ru"], TEXTS["btn_del_admin"]["en"]]))
async def ask_start_del_admin(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    if role != "super_admin": return
    
    await message.answer(TEXTS["ask_del_admin_username"][lang], reply_markup=back_kb(lang))
    await state.set_state(AdminManageState.ask_username_remove)

@router.message(AdminManageState.ask_username_remove)
async def remove_admin_action(message: types.Message, state: FSMContext):
    lang, role = await get_admin_info(message.from_user.id)
    
    if message.text and message.text in [TEXTS["btn_back"]["uz"], TEXTS["btn_back"]["ru"], TEXTS["btn_back"]["en"]]:
        await message.answer(TEXTS["menu_main_admin"][lang], reply_markup=main_admin_kb(lang, True))
        await state.clear()
        return

    username = message.text
    success = await db.downgrade_admin(username)
    
    if success:
        await message.answer(TEXTS["admin_deleted"][lang].format(username=username), reply_markup=main_admin_kb(lang, True))
    else:
        await message.answer(TEXTS["user_not_found"][lang])
        
    await state.clear()
