import telebot

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()

@bot.message_handler(commands=['start', 'admin'])
def main_handler(message):
    # ID ni tekshirish
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, f"Siz admin emassiz! Sizning ID: {message.from_user.id}")
        return

    # Agar admin bo'lsa
    if message.text == '/admin':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("➕ Anime qo'shish")
        bot.send_message(message.chat.id, "Admin panel faol:", reply_markup=markup)
    else:
        bot.reply_to(message, "Salom admin! /admin deb yozing.")

bot.infinity_polling()
