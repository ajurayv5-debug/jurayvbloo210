import os
import subprocess
import sys

# --- 🚀 KUTUBXONALARNI AVTOMATIK O'RNATISH ---
# Render requirements.txt ni ko'rmasa ham, mana shu kod kutubxonalarni baribir o'rnatadi!
try:
    import telebot
    from flask import Flask
except ImportError:
    print("Kutubxonalar topilmadi. Avtomatik o'rnatish boshlanmoqda...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "flask"])
    import telebot
    from flask import Flask

from telebot import types
import json
import threading

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168  
KANAL_ID = "@Anibassrasmiy" 

bot = telebot.TeleBot(TOKEN)
DB_FILE = 'anime_db.json'

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

@bot.message_handler(commands=['start'])
def start(message):
    db = load_db()
    if not db:
        bot.reply_to(message, "Hozircha bazada anime yo'q.")
        return
    markup = types.InlineKeyboardMarkup(row_width=2)
    for code, info in db.items():
        markup.add(types.InlineKeyboardButton(info['name'], callback_data=f"view_{code}"))
    bot.send_message(message.chat.id, "Anime tanlang:", reply_markup=markup)

# Render uchun Flask server
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    print("Bot Render serverida faollashmoqda...")
    bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
