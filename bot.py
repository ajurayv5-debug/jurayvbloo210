import telebot
import os
from flask import Flask, request

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Barcha kerakli handlerlar shu yerda bo'ladi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot Webhook orqali muvaffaqiyatli ishga tushdi!")

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # Quyidagi URLni o'z Render URL manzilingizga o'zgartiring
    bot.set_webhook(url='https://anime-bot-name.onrender.com/' + TOKEN)
    return "Webhook sozlandi!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
