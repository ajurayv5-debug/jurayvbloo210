import telebot
import json
import os

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
bot = telebot.TeleBot(TOKEN)

# ESKI WEBHOOKNI O'CHIRISH (Mana shu qator xatoni yo'qotadi)
bot.delete_webhook()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot muvaffaqiyatli uyg'ondi! 😊")

print("Bot ishga tushdi...")
bot.infinity_polling()
