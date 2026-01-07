# Barcha matnlar shu yerda saqlanadi
# Tillar: uz, ru, en

TEXTS = {
    # --- START & REGISTRATION ---
    "start_welcome": {
        "uz": "Assalomu alaykum! Iltimos, tilni tanlang:",
        "ru": "Здравствуйте! Пожалуйста, выберите язык:",
        "en": "Hello! Please select your language:"
    },
    "language_selected": {
        "uz": "🇺🇿 O'zbek tili tanlandi. Xush kelibsiz!",
        "ru": "🇷🇺 Русский язык выбран. Добро пожаловать!",
        "en": "🇬🇧 English language selected. Welcome!"
    },
    "greeting_registered": {
        "uz": "Assalomu alaykum! Yaxshi kayfiyat tilayman 😊",
        "ru": "Здравствуйте! Желаю хорошего настроения 😊",
        "en": "Hello! Have a great mood 😊"
    },

    # --- MENUS ---
    "menu_main_user": {
        "uz": "Asosiy menyu:",
        "ru": "Главное меню:",
        "en": "Main menu:"
    },
    "menu_main_admin": {
        "uz": "Admin panel:",
        "ru": "Панель администратора:",
        "en": "Admin panel:"
    },

    # --- BUTTONS ---
    "btn_anon_msg": {
        "uz": "🕵️ Anonim xabar yuborish",
        "ru": "🕵️ Отправить анонимное сообщение",
        "en": "🕵️ Send anonymous message"
    },
    "btn_profile": {
        "uz": "👤 Profil",
        "ru": "👤 Профиль",
        "en": "👤 Profile"
    },
    "btn_settings": {
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
        "en": "⚙️ Settings"
    },
    # User Settings Sub-buttons
    "btn_donate": {
        "uz": "💰 Donat (Xayriya)",
        "ru": "💰 Донат (Пожертвование)",
        "en": "💰 Donate"
    },
    "btn_contact_admin": {
        "uz": "👨‍💻 Admin bilan bog'lanish",
        "ru": "👨‍💻 Связь с админом",
        "en": "👨‍💻 Contact Admin"
    },
    "btn_feedback": {
        "uz": "✍️ Botga fikr qoldirish",
        "ru": "✍️ Оставить отзыв о боте",
        "en": "✍️ Leave feedback"
    },

    # Admin Buttons
    "btn_users": {
        "uz": "👥 Bot foydalanuvchilari",
        "ru": "👥 Пользователи бота",
        "en": "👥 Bot users"
    },
    "btn_broadcast": {
        "uz": "📢 Broadcast",
        "ru": "📢 Рассылка",
        "en": "📢 Broadcast"
    },
    "btn_comments": {
        "uz": "💬 Commentlar",
        "ru": "💬 Комментарии",
        "en": "💬 Comments"
    },
    "btn_anon_admin_view": {
        "uz": "🔐 Anonim xabarlar",
        "ru": "🔐 Анонимные сообщения",
        "en": "🔐 Anonymous messages"
    },

    # Admin Settings Sub-buttons
    "btn_add_admin": {
        "uz": "➕ Admin qo'shish",
        "ru": "➕ Добавить админа",
        "en": "➕ Add admin"
    },
    "btn_del_admin": {
        "uz": "➖ Admin o'chirish",
        "ru": "➖ Удалить админа",
        "en": "➖ Remove admin"
    },
    "btn_list_admin": {
        "uz": "📋 Adminlar ro'yxati",
        "ru": "📋 Список админов",
        "en": "📋 List of admins"
    },

    # Common Buttons
    "btn_back": {
        "uz": "🔙 Orqaga",
        "ru": "🔙 Назад",
        "en": "🔙 Back"
    },
    "btn_change_lang": {
        "uz": "🌍 Tilni o'zgartirish",
        "ru": "🌍 Изменить язык",
        "en": "🌍 Change language"
    },

    # --- FEATURES MESSAGES ---

    # Profile
    "profile_info": {
        "uz": "<b>Sizning profilingiz:</b>\n🆔 ID: {id}\n👤 Ism: {name}\n🔗 Username: {username}\n🌍 Til: {lang}\n🔰 Rol: {role}",
        "ru": "<b>Ваш профиль:</b>\n🆔 ID: {id}\n👤 Имя: {name}\n🔗 Юзернейм: {username}\n🌍 Язык: {lang}\n🔰 Роль: {role}",
        "en": "<b>Your Profile:</b>\n🆔 ID: {id}\n👤 Name: {name}\n🔗 Username: {username}\n🌍 Lang: {lang}\n🔰 Role: {role}"
    },

    # Anon Message (User)
    "ask_anon_msg": {
        "uz": "Anonim xabaringizni yozing...",
        "ru": "Напишите ваше анонимное сообщение...",
        "en": "Write your anonymous message..."
    },
    "anon_msg_sent": {
        "uz": "✅ Xabaringiz yuborildi!",
        "ru": "✅ Ваше сообщение отправлено!",
        "en": "✅ Your message has been sent!"
    },

    # Anon Message (Super Admin View)
    "anon_msg_received": {
        "uz": "<b>📩 Yangi anonim xabar!</b>\n\n📄 Matn: {msg}\n👤 Yuboruvchi: {username}",
        "ru": "<b>📩 Новое анонимное сообщение!</b>\n\n📄 Текст: {msg}\n👤 Отправитель: {username}",
        "en": "<b>📩 New anonymous message!</b>\n\n📄 Text: {msg}\n👤 Sender: {username}"
    },
    "no_anon_msgs": {
        "uz": "Hozircha anonim xabarlar yo'q.",
        "ru": "Пока нет анонимных сообщений.",
        "en": "No anonymous messages yet."
    },
    "anon_msg_format": {
        "uz": "<b>📩 Anonim xabar</b> (ID: {id})\n📅 Vaqt: {date}\n👤 Yuboruvchi: {sender}\n\n📝 Xabar: {msg}",
        "ru": "<b>📩 Анонимное сообщение</b> (ID: {id})\n📅 Время: {date}\n👤 Отправитель: {sender}\n\n📝 Сообщение: {msg}",
        "en": "<b>📩 Anonymous Message</b> (ID: {id})\n📅 Time: {date}\n👤 Sender: {sender}\n\n📝 Message: {msg}"
    },

    # Reply to Anon
    "btn_reply_inline": {
        "uz": "✍️ Javob berish",
        "ru": "✍️ Ответить",
        "en": "✍️ Reply"
    },
    "ask_reply": {
        "uz": "Javob matnini yozing (faqat shu userga boradi):",
        "ru": "Напишите текст ответа (уйдет только этому пользователю):",
        "en": "Write the reply text (sent only to this user):"
    },
    "reply_sent": {
        "uz": "✅ Javob muvaffaqiyatli yuborildi!",
        "ru": "✅ Ответ успешно отправлен!",
        "en": "✅ Reply sent successfully!"
    },
    "reply_received": {
        "uz": "<b>📩 Admin javobi:</b>\n\n{msg}",
        "ru": "<b>📩 Ответ администратора:</b>\n\n{msg}",
        "en": "<b>📩 Admin reply:</b>\n\n{msg}"
    },
    "error_user_not_found": {
        "uz": "❌ Xatolik: User topilmadi yoki botni bloklagan.",
        "ru": "❌ Ошибка: Пользователь не найден или заблокировал бота.",
        "en": "❌ Error: User not found or blocked the bot."
    },

    # Broadcast
    "select_broadcast_target": {
        "uz": "Kimga xabar yubormoqchisiz?",
        "ru": "Кому вы хотите отправить сообщение?",
        "en": "Who do you want to send the message to?"
    },
    "broadcast_all": {
        "uz": "🌐 Barcha foydalanuvchilarga",
        "ru": "🌐 Всем пользователям",
        "en": "🌐 To all users"
    },
    "broadcast_admins": {
        "uz": "👮 Faqat Adminlarga",
        "ru": "👮 Только админам",
        "en": "👮 Only to Admins"
    },
    "ask_broadcast_msg": {
        "uz": "Xabar matnini yozing (rasm, video, audio yoki matn):",
        "ru": "Напишите текст сообщения (фото, видео, audio или текст):",
        "en": "Write the message text (photo, video, audio or text):"
    },
    "broadcast_started": {
        "uz": "🚀 Xabar yuborish boshlandi...",
        "ru": "🚀 Рассылка началась...",
        "en": "🚀 Broadcast started..."
    },
    "broadcast_ended": {
        "uz": "✅ Xabar yuborish tugadi.\n📊 Natija: {total} ta userga yuborildi.",
        "ru": "✅ Рассылка завершена.\n📊 Итог: Отправлено {total} пользователям.",
        "en": "✅ Broadcast finished.\n📊 Result: Sent to {total} users."
    },

    # Comments / Feedback
    "ask_feedback": {
        "uz": "Bot haqida fikringizni yozib qoldiring:",
        "ru": "Оставьте свой отзыв о боте:",
        "en": "Leave your feedback about the bot:"
    },
    "feedback_saved": {
        "uz": "✅ Fikringiz uchun rahmat! Adminga yetkazildi.",
        "ru": "✅ Спасибо за отзыв! Передано админу.",
        "en": "✅ Thanks for your feedback! Sent to admin."
    },
    "no_comments": {
        "uz": "Hozircha izohlar yo'q.",
        "ru": "Пока нет комментариев.",
        "en": "No comments yet."
    },
    "comment_format": {
        "uz": "<b>🗣 Izoh</b> ({role})\n👤 User: {username}\n📝 Matn: {msg}\n📅 {date}",
        "ru": "<b>🗣 Комментарий</b> ({role})\n👤 User: {username}\n📝 Текст: {msg}\n📅 {date}",
        "en": "<b>🗣 Comment</b> ({role})\n👤 User: {username}\n📝 Text: {msg}\n📅 {date}"
    },

    # Admin Management
    "ask_admin_username": {
        "uz": "Admin qilmoqchi bo'lgan foydalanuvchi username-ni yuboring (masalan: @username):",
        "ru": "Отправьте юзернейм пользователя для админки (например: @username):",
        "en": "Send username to promote to admin (e.g. @username):"
    },
    "ask_del_admin_username": {
        "uz": "Adminlikdan olmoqchi bo'lgan username-ni yuboring (masalan: @username):",
        "ru": "Отправьте юзернейм для удаления из админов (например: @username):",
        "en": "Send username to remove from admins (e.g. @username):"
    },
    "admin_added": {
        "uz": "✅ Foydalanuvchi ADMIN qilindi: {username}",
        "ru": "✅ Пользователь назначен АДМИНОМ: {username}",
        "en": "✅ User promoted to ADMIN: {username}"
    },
    "admin_deleted": {
        "uz": "✅ Adminlikdan olindi: {username}",
        "ru": "✅ Удален из админов: {username}",
        "en": "✅ Removed from admins: {username}"
    },
    "user_not_found": {
        "uz": "❌ Foydalanuvchi bazada topilmadi. Avval botga start bosgan bo'lishi kerak.",
        "ru": "❌ Пользователь не найден. Он должен сначала запустить бота.",
        "en": "❌ User not found. They must start the bot first."
    },
    "admin_list_empty": {
        "uz": "❌ Adminlar mavjud emas.",
        "ru": "❌ Админов нет.",
        "en": "❌ No admins found."
    },
    "admin_list_header": {
        "uz": "<b>📋 Adminlar ro'yxati:</b>\n\n",
        "ru": "<b>📋 Список админов:</b>\n\n",
        "en": "<b>📋 List of Admins:</b>\n\n"
    },

    # Stats
    "stats_info": {
        "uz": "<b>📊 Statistika:</b>\n\n👤 Bot foydalanuvchilari: {users}\n👮 Adminlar: {admins}\n🌐 Jami: {total}",
        "ru": "<b>📊 Статистика:</b>\n\n👤 Пользователи: {users}\n👮 Админы: {admins}\n🌐 Всего: {total}",
        "en": "<b>📊 Statistics:</b>\n\n👤 Users: {users}\n👮 Admins: {admins}\n🌐 Total: {total}"
    },

    # Donate & Contact Info
    "donate_info": {
        "uz": "<b>💳 Donat uchun:</b>\n\nKarta: <code>5614 6820 0417 7210</code>\nEgasi: Jumatov X.\n\nBot rivojiga qo‘shgan hissangiz uchun katta rahmat!\nBiz buni juda qadrlaymiz 🙏",
        "ru": "<b>💳 Для доната:</b>\n\nКарта: <code>5614 6820 0417 7210</code>\nВладелец: Jumatov X.\n\nБольшое спасибо за ваш вклад в развитие бота.\nМы искренне это ценим! 🙏",
        "en": "<b>💳 For Donate:</b>\n\nCard: <code>5614 6820 0417 7210</code>\nOwner: Jumatov X.\n\nThank you very much for your contribution to the development of the bot.\nWe truly appreciate it! 🙏"
    },
    "contact_info": {
        "uz": "<b>👨‍💻 Admin bilan aloqa:</b> @jumatov_afu\nSavol va takliflar uchun yozishingiz mumkin.",
        "ru": "<b>👨‍💻 Связь с админом:</b> @jumatov_afu\nПишите по вопросам и предложениям.",
        "en": "<b>👨‍💻 Contact Admin:</b> @jumatov_afu\nYou can write for questions and suggestions."
    },

    # --- TECHNICAL WORKS ---
    "btn_tech_works": {
        "uz": "🔧 Texnik ishlar",
        "ru": "🔧 Технические работы",
        "en": "🔧 Technical works"
    },
    "tech_menu_title": {
        "uz": "🔧 Texnik ishlar bo'limi\n\nTanlang:",
        "ru": "🔧 Раздел технических работ\n\nВыберите:",
        "en": "🔧 Technical works section\n\nChoose:"
    },
    "btn_tech_news": {
        "uz": "📢 Botga yangiliklar kiritildi",
        "ru": "📢 Введены новости в бота",
        "en": "📢 Bot news update"
    },
    "btn_tech_maintenance_on": {
        "uz": "🔴 Bot vaqtinchalik ishlamaydi",
        "ru": "🔴 Бот временно не работает",
        "en": "🔴 Bot temporarily down"
    },
    "btn_tech_maintenance_off": {
        "uz": "🟢 Texnik ishlar tugallandi",
        "ru": "🟢 Технические работы завершены",
        "en": "🟢 Technical works finished"
    },
    "maintenance_active_msg": {
        "uz": "<b>⚠️ Diqqat!</b>\nHozirda botda texnik ishlar olib borilmoqda. Bot yana ishlashni boshlaganda sizga xabar beramiz.",
        "ru": "<b>⚠️ Внимание!</b>\nВ данный момент проводятся технические работы. Мы уведомим вас, когда бот снова начнет работать.",
        "en": "<b>⚠️ Attention!</b>\nTechnical maintenance is currently in progress. We will notify you when the bot is back online."
    },
    "maintenance_enabled": {
        "uz": "✅ Texnik ishlar rejimi yoqildi\nFoydalanuvchilar botdan vaqtinchalik foydalana olmaydi.",
        "ru": "✅ Режим технических работ включен\nПользователи временно не могут пользоваться ботом.",
        "en": "✅ Maintenance mode enabled\nUsers temporarily cannot use the bot."
    }
    ,

    "maintenance_disabled": {
        "uz": "✅ Texnik ishlar rejimi o‘chirildi.\nBot yana ishlamoqda.",
        "ru": "✅ Режим технических работ выключен.\nБот снова работает.",
        "en": "✅ Maintenance mode disabled.\nThe bot is running again."
    },
    "maintenance_deactive_msg": {
        "uz": "Bot yana ishlashda davom etmoqda 😊",
        "ru": "Бот снова работает в обычном режиме 😊",
        "en": "The bot is back and running smoothly 😊"
    },
    "ask_tech_broadcast_msg": {
        "uz": "📢 Yangilik haqida xabar matnini yozing (barchaga yuboriladi):",
        "ru": "📢 Напишите текст новости (будет отправлено всем):",
        "en": "📢 Write the news text (will be sent to all):"
    },

    # --- ADVANCED COMMENTS ---
    "btn_filter_1_day": {
        "uz": "1️⃣ 1 kunlik yangi",
        "ru": "1️⃣ 1 день (новые)",
        "en": "1️⃣ 1 day (new)"
    },
    "btn_filter_1_week": {
        "uz": "2️⃣ 1 haftalik",
        "ru": "2️⃣ 1 неделя",
        "en": "2️⃣ 1 week"
    },
    "btn_filter_1_month": {
        "uz": "3️⃣ 1 oylik",
        "ru": "3️⃣ 1 месяц",
        "en": "3️⃣ 1 month"
    },
    "btn_del_read_comments": {
        "uz": "4️⃣ O'qilganlarni o'chirish",
        "ru": "4️⃣ Удалить прочитанные",
        "en": "4️⃣ Delete read"
    },
    "comments_filter_title": {
        "uz": "Izohlarni saralash:",
        "ru": "Фильтрация комментариев:",
        "en": "Filter comments:"
    },
    "comments_deleted": {
        "uz": "✅ Barcha o'qilgan izohlar o'chirildi.",
        "ru": "✅ Все прочитанные комментарии удалены.",
        "en": "✅ All read comments deleted."
    },

    # --- MEDIA FORMATS ---
    "media_type_caption": {
        "uz": "<b>📎 Fayl turi:</b> {type}",
        "ru": "<b>📎 Тип файла:</b> {type}",
        "en": "<b>📎 File type:</b> {type}"
    },
    
    # --- ANON FILTERS (FINAL) ---
    "anon_menu_title": {
        "uz": "🔐 Anonim xabarlar bo'limi\n\nKerakli vaqt oralig'ini tanlang:",
        "ru": "🔐 Раздел анонимных сообщений\n\nВыберите период:",
        "en": "🔐 Anonymous messages section\n\nChoose period:"
    },
    "anon_1_day": {
        "uz": "1️⃣ 1 kunlik yangi",
        "ru": "1️⃣ 1 день (новые)",
        "en": "1️⃣ 1 day (new)"
    },
    "anon_1_week": {
        "uz": "2️⃣ 1 haftalik",
        "ru": "2️⃣ 1 неделя",
        "en": "2️⃣ 1 week"
    },
    "anon_1_month": {
        "uz": "3️⃣ 1 oylik",
        "ru": "3️⃣ 1 месяц",
        "en": "3️⃣ 1 month"
    },
    "anon_delete_read": {
        "uz": "🗑 O'qilganlarni o'chirish",
        "ru": "🗑 Удалить прочитанные",
        "en": "🗑 Delete read"
    },
    "anon_back": {
        "uz": "🔙 Orqaga",
        "ru": "🔙 Назад",
        "en": "🔙 Back"
    },
    "anon_no_messages": {
        "uz": "📭 Bu davrda xabarlar topilmadi.",
        "ru": "📭 Сообщений за этот период не найдено.",
        "en": "📭 No messages found for this period."
    },
    "anon_deleted_success": {
        "uz": "✅ Barcha o'qilgan anonim xabarlar muvaffaqiyatli o'chirildi!",
        "ru": "✅ Все прочитанные анонимные сообщения успешно удалены!",
        "en": "✅ All read anonymous messages successfully deleted!"
    }
}
