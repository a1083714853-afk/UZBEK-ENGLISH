import os
from flask import Flask
from threading import Thread
import telebot
from googletrans import Translator

TOKEN = "8988660751:AAHXs9TWJgdFTULUC_0wxpnq8mxLQEFFku4"
bot = telebot.TeleBot(TOKEN)
translator = Translator()

# --- 1. 12 TA ZAMON VA GRAMMATIKA QOIDALARI BAZASI ---
grammar_rules = {
    "tenses_menu": (
        "⏳ <b>Ingliz tilining 12 ta zamoni bo'limi:</b>\n\n"
        "Qaysi zamonni o'rganmoqchisiz? Quyidagi buyruqlardan birini bosing:\n\n"
        "<b>Hozirgi zamonlar (Present):</b>\n"
        "• /present_simple - Hozirgi oddiy zamon\n"
        "• /present_continuous - Hozirgi davomiy zamon\n"
        "• /present_perfect - Hozirgi tugallangan zamon\n"
        "• /present_perfect_continuous - Hozirgi tugallangan-davomiy zamon\n\n"
        "<b>O'tgan zamonlar (Past):</b>\n"
        "• /past_simple - O'tgan oddiy zamon\n"
        "• /past_continuous - O'tgan davomiy zamon\n"
        "• /past_perfect - O'tgan tugallangan zamon\n"
        "• /past_perfect_continuous - O'tgan tugallangan-davomiy zamon\n\n"
        "<b>Kelasi zamonlar (Future):</b>\n"
        "• /future_simple - Kelasi oddiy zamon\n"
        "• /future_continuous - Kelasi davomiy zamon\n"
        "• /future_perfect - Kelasi tugallangan zamon\n"
        "• /future_perfect_continuous - Kelasi tugallangan-davomiy zamon\n\n"
        "👥 <b>Boshqa qoidalar:</b>\n"
        "• /pronouns - Olmoshlar"
    ),
    "present_simple": "🟢 <b>1. Present Simple (Hozirgi oddiy zamon)</b>\n\n<b>Qachon ishlatiladi?</b> Doimiy takrorlanadigan, odat tusiga kirgan harakatlar uchun.\n<b>Formulasi:</b> Ega + V1 (-s/-es)\n<i>Misol:</i> I work every day.",
    "present_continuous": "🟢 <b>2. Present Continuous (Hozirgi davomiy zamon)</b>\n\n<b>Qachon ishlatiladi?</b> Ayni paytda bo'layotgan jarayonlar uchun.\n<b>Formulasi:</b> Ega + am/is/are + V(-ing)\n<i>Misol:</i> I am reading a book.",
    "present_perfect": "🟢 <b>3. Present Perfect (Hozirgi tugallangan zamon)</b>\n\n<b>Qachon ishlatiladi?</b> Harakat tugallangan, natijasi muhim.\n<b>Formulasi:</b> Ega + have/has + V3\n<i>Misol:</i> I have finished my homework.",
    "present_perfect_continuous": "🟢 <b>4. Present Perfect Continuous</b>\n\n<b>Formulasi:</b> Ega + have/has + been + V(-ing)\n<i>Misol:</i> I have been living here for 5 years.",
    "past_simple": "🟠 <b>5. Past Simple (O'tgan oddiy zamon)</b>\n\n<b>Formulasi:</b> Ega + V2 (-ed)\n<i>Misol:</i> I went to Tashkent yesterday.",
    "past_continuous": "🟠 <b>6. Past Continuous</b>\n\n<b>Formulasi:</b> Ega + was/were + V(-ing)\n<i>Misol:</i> I was reading a book.",
    "past_perfect": "🟠 <b>7. Past Perfect</b>\n\n<b>Formulasi:</b> Ega + had + V3\n<i>Misol:</i> The train had left.",
    "past_perfect_continuous": "🟠 <b>8. Past Perfect Continuous</b>\n\n<b>Formulasi:</b> Ega + had + been + V(-ing)",
    "future_simple": "🔵 <b>9. Future Simple (Kelasi oddiy zamon)</b>\n\n<b>Formulasi:</b> Ega + will + V1\n<i>Misol:</i> I will help you.",
    "future_continuous": "🔵 <b>10. Future Continuous</b>\n\n<b>Formulasi:</b> Ega + will be + V(-ing)",
    "future_perfect": "🔵 <b>11. Future Perfect</b>\n\n<b>Formulasi:</b> Ega + will have + V3",
    "future_perfect_continuous": "🔵 <b>12. Future Perfect Continuous</b>\n\n<b>Formulasi:</b> Ega + will have been + V(-ing)",
    "pronouns": "👥 <b>Olmoshlar:</b> I, You, He, She, It, We, They"
}

# --- 2. RENDER UCHUN FLASK SERVERI ---
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 3. BOT BUYRUQLARI ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 🌟 Ingliz tili tarjima botiga xush kelibsiz.\n\n"
        "🔍 So'z yozing:\n"
        "• O'zbekcha ➔ Inglizchaga 🇬🇧\n"
        "• Inglizcha ➔ O'zbekchaga 🇺🇿\n\n"
        "📖 Zamonlar uchun /tenses ni bosing.",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['tenses', 'grammar'])
def send_tenses_menu(message):
    bot.send_message(message.chat.id, grammar_rules["tenses_menu"], parse_mode="HTML")

# Qolgan buyruqlar uchun qisqa yo'l
for cmd in ["present_simple", "present_continuous", "present_perfect", "present_perfect_continuous",
            "past_simple", "past_continuous", "past_perfect", "past_perfect_continuous",
            "future_simple", "future_continuous", "future_perfect", "future_perfect_continuous", "pronouns"]:
    @bot.message_handler(commands=[cmd])
    def handle_tenses(message, c=cmd):
        bot.send_message(message.chat.id, grammar_rules[c], parse_mode="HTML")

# --- 4. ANIQ TARJIMA QILISH QISMI ---
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    user_text = message.text.strip()

    try:
        # Avtomatik tilni aniqlash
        detected = translator.detect(user_text)
        lang = detected.lang

        # Agar til o'zbekcha (uz) yoki shunga o'xshash bo'lsa -> Inglizchaga tarjima qilamiz
        if lang == 'uz':
            translation = translator.translate(user_text, dest='en').text
            target_lang = "🇬🇧 Inglizcha"
        else:
            # Aks holda -> O'zbekchaga tarjima qilamiz
            translation = translator.translate(user_text, dest='uz').text
            target_lang = "🇺🇿 O'zbekcha"

        bot.reply_to(
            message,
            f"🌐 <b>Google Translate ({target_lang}):</b>\n<code>{translation}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Tarjima qilishda xatolik yuz berdi.")

# --- 5. BOTNI ISHGA TUSHIRISH ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(none_stop=True)
