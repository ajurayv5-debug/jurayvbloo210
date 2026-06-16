import telebot

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
bot = telebot.TeleBot(TOKEN)

# Eski ulanishlarni uzish (409 xatosini yo'qotish uchun)
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Bot ishlamoqda! 😊")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Bot xabarni qabul qildi!")

print("Bot polling rejimida ishga tushdi...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)
