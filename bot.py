import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
bot = telebot.TeleBot(TOKEN)

# Eskisini o'chirish
bot.delete_webhook()

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot uyg'ondi va ishga tayyor. 😊")

# --- ADMIN PANEL ---
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if message.from_user.id != ADMIN_ID:
        return
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Anime qo'shish", "🗑 O'chirish", "📊 Statistika")
    bot.send_message(message.chat.id, "Admin panel faol:", reply_markup=markup)

# --- ADMIN BOSQICHLARI (Step Handler) ---
@bot.message_handler(func=lambda message: message.text == "➕ Anime qo'shish")
def start_add_anime(message):
    if message.from_user.id != ADMIN_ID: return
    msg = bot.send_message(message.chat.id, "Anime nomini yuboring:")
    bot.register_next_step_handler(msg, get_anime_name)

def get_anime_name(message):
    anime_name = message.text
    # Hozircha shunchaki tasdiqlash uchun
    bot.send_message(message.chat.id, f"Anime nomi: {anime_name}. Endi kodini yuboring:")
    # Keyingi qadamlar uchun shu yerda state saqlash kerak bo'ladi
    
# --- POLING ---
print("Bot ishga tushdi...")
bot.infinity_polling()
