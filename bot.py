import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
DB_FILE = 'anime_db.json'
bot = telebot.TeleBot(TOKEN)

# Bazani boshqarish
def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f: json.dump(data, f, ensure_ascii=False, indent=4)

# Admin panel doimiy tugmalar bilan
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id != ADMIN_ID: return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("➕ Anime qo'shish")
    bot.send_message(message.chat.id, "Admin panel faol:", reply_markup=markup)

# Anime qo'shish jarayoni
temp_data = {}

@bot.message_handler(func=lambda message: message.text == "➕ Anime qo'shish")
def ask_name(message):
    if message.from_user.id != ADMIN_ID: return
    msg = bot.send_message(message.chat.id, "Anime nomini yuboring:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    if message.text.startswith('/'): return
    temp_data['name'] = message.text
    msg = bot.send_message(message.chat.id, "Endi anime kodini (raqam) yuboring:")
    bot.register_next_step_handler(msg, get_code)

def get_code(message):
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "❌ Kod faqat raqam bo'lishi kerak! Qaytadan yuboring:")
        bot.register_next_step_handler(msg, get_code)
        return
    
    code = message.text
    db = load_db()
    db[code] = {"name": temp_data['name']}
    save_db(db)
    bot.send_message(message.chat.id, f"✅ Muvaffaqiyatli saqlandi!\nNomi: {temp_data['name']}\nKodi: {code}")

# Qidiruv tizimi
@bot.message_handler(func=lambda message: message.text.isdigit())
def search(message):
    db = load_db()
    if message.text in db:
        bot.reply_to(message, f"🎬 Topildi: {db[message.text]['name']}")
    else:
        bot.reply_to(message, "❌ Bunday kodli anime yo'q.")

bot.delete_webhook()
print("Bot ishga tushdi...")
bot.infinity_polling()
