import telebot
import os
from flask import Flask, request

TOKEN = "8320449341:AAHbrGME24j5ojTtH7URuNMeKlRdA9e2NkI"
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

# Webhookni bir marta o'rnatish
if __name__ == "__main__":
    bot.remove_webhook()
    # URL: Render sizga bergan havola (masalan: https://anime-bot.onrender.com/)
    # O'z manzilingizni shunga moslab yozing:
    bot.set_webhook(url='https://YOUR-RENDER-APP-NAME.onrender.com/' + TOKEN)
    
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
