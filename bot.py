import os
import json
import telebot
from telebot import types
from flask import Flask
import threading

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
KANAL_ID = "@Anibassrasmiy"
bot = telebot.TeleBot(TOKEN)
DB_FILE = 'anime_db.json'

# Bazani yuklash va saqlash
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Admin uchun menu
@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    if message.from_user.id != ADMIN_ID: return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Anime qo'shish", "🔄 Ongoing", "✏️ Tahrirlash")
    bot.send_message(message.chat.id, "Admin panel:", reply_markup=markup)

# Guruh va lichka uchun global qidiruv
@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def global_search(message):
    db = load_db()
    code = message.text
    if code in db:
        anime = db[code]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📺 Qismlarni ko'rish", callback_data=f"list_{code}"))
        bot.send_photo(message.chat.id, anime['photo'], caption=f"🎬 {anime['name']}", reply_markup=markup)
    else:
        bot.reply_to(message, "Anime topilmadi.")

# CALLBACK TIZIMI (Sahifalash va video)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data.split('_')
    action = data[0]
    code = data[1]
    db = load_db()

    if action == "list": # Qismlar ro'yxatini chiqarish
        anime = db[code]
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i, vid in enumerate(anime['videos']):
            markup.add(types.InlineKeyboardButton(f"{i+1}-qism", callback_data=f"play_{code}_{i}"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif action == "play": # Videoni yuborish
        idx = int(data[2])
        bot.send_video(call.message.chat.id, db[code]['videos'][idx])

# WEB SERVER (Render uchun)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot ishlamoqda!"

if __name__ == '__main__':
    # Threading orqali botni va web serverni birga yuritish
    threading.Thread(target=lambda: bot.infinity_polling(timeout=60, long_polling_timeout=60), daemon=True).start()
    
    # Flask serverini ishga tushirish
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
