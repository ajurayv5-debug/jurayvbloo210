import telebot
import json
import os

# YANGI TOKENNI SHU YERGA YOZING
TOKEN = "8320449341:AAFQsSl_cmoJLE7qVkNPTeWHjACMnufMLZI"
ADMIN_ID = 8910933168
DB_FILE = 'anime_db.json'

bot = telebot.TeleBot(TOKEN)

# 1. Eski webhookni tozalash va yangi ulanishni himoyalash
bot.remove_webhook()

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

# Boshqa funksiyalar (admin, qo'shish, qidirish) avvalgidek qoladi...

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot yangi token bilan ishga tushdi va faqat shu yerda faol!")

# BOTNI ISHGA TUSHIRISH
if __name__ == '__main__':
    print("Bot ishga tushdi...")
    # drop_pending_updates=True eski "Conflict"larni butunlay o'chiradi
    bot.infinity_polling(timeout=10, long_polling_timeout=5, drop_pending_updates=True)
