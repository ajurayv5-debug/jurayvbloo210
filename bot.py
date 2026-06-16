import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
DB_FILE = 'anime_db.json'
bot = telebot.TeleBot(TOKEN)

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id != ADMIN_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("➕ Anime qo'shish")
    bot.send_message(message.chat.id, "Admin panel faol:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "➕ Anime qo'shish")
def ask_name(message):
    if message.from_user.id != ADMIN_ID: return
    msg = bot.send_message(message.chat.id, "Anime nomini yuboring:")
    bot.register_next_step_handler(msg, lambda m: get_name(m))

def get_name(message):
    name = message.text
    msg = bot.send_message(message.chat.id, "Endi kodini yuboring:")
    bot.register_next_step_handler(msg, lambda m: get_code(m, name))

def get_code(message, name):
    code = message.text
    db = load_db()
    db[code] = {"name": name}
    save_db(db)
    bot.send_message(message.chat.id, f"✅ Saqlandi: {name} (Kod: {code})")

bot.remove_webhook()
print("Bot ishga tushdi...")
bot.infinity_polling()
