@server.route("/")
def webhook():
    # Eski webhookni butunlay o'chiramiz
    bot.remove_webhook()
    # Yangisini o'rnatamiz (URLni o'z manzilingizga almashtiring!)
    url = 'https://sizning-botingiz-nomi.onrender.com/' + TOKEN
    if bot.set_webhook(url=url):
        return "Webhook muvaffaqiyatli o'rnatildi!", 200
    else:
        return "Webhook o'rnatishda xatolik!", 500
