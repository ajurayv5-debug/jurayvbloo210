import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
DB_FILE = 'anime_db.json'
bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()

# BAZANI YUKLASH VA SAQLASH
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

# --- START ---
@bot.message_handler(commands=['start', 'admin'])
def admin_menu(message):
    if message.from_user.id != ADMIN_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Anime qo'shish")
    bot.send_message(message.chat.id, "Admin panel:", reply_markup=markup)

# --- ANIME QO'SHISH JARAYONI ---
temp_data = {}

@bot.message_handler(func=lambda message: message.text == "➕ Anime qo'shish")
def ask_name(message):
    msg = bot.send_message(message.chat.id, "Anime nomini yuboring:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    temp_data['name'] = message.text
    msg = bot.send_message(message.chat.id, "Endi anime kodini (raqam) yuboring:")
    bot.register_next_step_handler(msg, get_code)

def get_code(message):
    code = message.text
    db = load_db()
    db[code] = {"name": temp_data['name']}
    save_db(db)
    bot.send_message(message.chat.id, f"✅ Muvaffaqiyatli saqlandi!\nNomi: {temp_data['name']}\nKodi: {code}")

# --- QIDIRUV ---
@bot.message_handler(func=lambda message: message.text.isdigit())
def search(message):
    db = load_db()
    code = message.text
    if code in db:
        bot.reply_to(message, f"🎬 Nomi: {db[code]['name']}")
    else:
        bot.reply_to(message, "❌ Bunday kodli anime topilmadi.")

print("Bot ishga tushdi...")
bot.infinity_polling()
