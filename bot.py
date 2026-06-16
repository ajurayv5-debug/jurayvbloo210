import telebot
import os
from flask import Flask, request

TOKEN = "8320449341:AAHqt8d26UcoOe4dVbFiXnPG1RF0Cxu8SeM"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def index():
    return "Bot ishlamoqda!"

# Webhookni faqat bir marta o'rnatish uchun kichik shart
if __name__ == "__main__":
    # Webhookni bir marta o'rnatamiz
    bot.remove_webhook()
    bot.set_webhook(url='https://jurayvbloo210-21.onrender.com/' + TOKEN)
    
    # Serverni ishga tushiramiz
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))