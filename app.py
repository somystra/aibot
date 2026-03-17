import os
import requests
from flask import Flask, request
import telebot

# Sozlamalar
TOKEN = "8752755194:AAFPrRtrbF4-t30AZYsdaGtVb2l11lr5SWs"
HF_API_KEY = "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"
MODEL_ID = "mistralai/Mistral-7B-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_ai_response(text):
    payload = {"inputs": f"User: {text}\nAI:", "parameters": {"max_new_tokens": 150}}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        result = response.json()
        # AI javobini tozalab olish
        ai_text = result[0]['generated_text'].split("AI:")[1].strip()
        return ai_text
    except:
        return "Hozircha tizimda yuklama ko'p. Birozdan so'ng urinib ko'ring."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌐 **NetGlobal AI Botiga xush kelibsiz!**\n\n"
        "Men sun'iy intellekt yordamida savollaringizga javob beraman.\n\n"
        "👨‍💻 **Yaratuvchilar:**\n"
        "• Solijon Muhammadkarimov\n"
        "• Ulug'bek Shuxratullayev\n"
        "• Dilmurod Abduvaxobov\n\n"
        "Marhamat, savolingizni yozing!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text
    # Bot "o'ylayapti..." holati
    bot.send_chat_action(message.chat.id, 'typing')
    ai_reply = get_ai_response(user_text)
    
    footer = "\n\n---\n🤖 *NetGlobal AI | Powered by Hugging Face*"
    bot.reply_to(message, ai_reply + footer, parse_mode="Markdown")

# Render uchun webhook yoki polling sozlamasi
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # BU YERGA RENDER_URL_MANZILI QO'YILADI (quyida tushuntirilgan)
    return "NetGlobal AI Bot Ishlamoqda!", 200

if __name__ == "__main__":
    bot.infinity_polling() # Localda tekshirish uchun
