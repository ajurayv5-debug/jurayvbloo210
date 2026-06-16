import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
bot = telebot.TeleBot(TOKEN)

# Bazani yuklash uchun oddiy funksiya
def load_db():
    if not os.path.exists('anime_db.json'): return {}
    with open('anime_db.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# /start komandasi orqali bot tirikligini tekshiramiz
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot uyg‘ondi va ishlashga tayyor. 😊")

# Barcha xabarlarni eshitish
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Bu qism bot ishlayotganini bilish uchun
    bot.reply_to(message, f"Siz yozdingiz: {message.text}")

print("Bot ishga tushdi...")
bot.infinity_polling()
