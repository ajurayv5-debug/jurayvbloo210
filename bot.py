import os
import json
import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8320449341:AAEPHiKR2b0jauEY-Sp9o1B0q3i4PijbRiQ"
ADMIN_ID = 8910933168
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
DB_FILE = 'anime_db.json'

def load_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- ADMIN PANEL ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Anime qo'shish", "🔄 Ongoing", "✏️ Tahrirlash")
    bot.send_message(message.chat.id, "Admin panel faol:", reply_markup=markup)

# --- QIDIRUV (Lichka va Guruh) ---
@bot.message_handler(func=lambda message: message.text and message.text.isdigit())
def search(message):
    db = load_db()
    if message.text in db:
        anime = db[message.text]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📺 Qismlarni ko'rish", callback_data=f"list_{message.text}"))
        bot.send_photo(message.chat.id, anime['photo'], caption=f"🎬 {anime['name']}", reply_markup=markup)

# --- SAHIFALASH VA KO'RISH (CALLBACK) ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    data = call.data.split('_')
    action, code, *args = data
    db = load_db()
    
    if action == "list":
        anime = db[code]
        markup = types.InlineKeyboardMarkup(row_width=4)
        for i in range(len(anime['videos'])):
            markup.add(types.InlineKeyboardButton(str(i+1), callback_data=f"play_{code}_{i}"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif action == "play":
        idx = int(args[0])
        bot.send_video(call.message.chat.id, db[code]['videos'][idx])

# --- WEBHOOK (409 Xatosini o'ldiradi) ---
@app.route('/' + TOKEN, methods=['POST'])
def get_msg():
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    return "Running!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
