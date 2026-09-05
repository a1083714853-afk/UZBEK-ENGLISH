import os
from flask import Flask
from threading import Thread
import telebot
import requests
import easyocr
from PIL import Image

TOKEN = "8988660751:AAEVxSose38VxX6v0XhjajzbJEjejre50Ps"
bot = telebot.TeleBot(TOKEN)

# Easyocr ni yuklab olish (Ingliz va O'zbek tillari uchun)
# gpu=False serverlarda xatolik bermasligi uchun qo'yilgan
print("EasyOCR yuklanmoqda, iltimos kuting...")
reader = easyocr.Reader(['en', 'uz'], gpu=False)
print("EasyOCR tayyor!")

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
        "Assalomu alaykum! 🌟 Ingliz tili va Manga tarjima botiga xush kelibsiz.\n\n"
        "🔍 Nima qila olaman?\n"
        "• Matn yozing ➔ Tarjima qiladi 🇬🇧 ⇄ 🇺🇿\n"
        "• **Manga (rasm) tashlang** ➔ Rasmdagi inglizcha matnlarni o'qib, o'zbekchaga tarjima qiladi 🖼️\n\n"
        "📖 Zamonlar uchun /tenses ni bosing.",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['tenses', 'grammar'])
def send_tenses_menu(message):
    bot.send_message(message.chat.id, grammar_rules["tenses_menu"], parse_mode="HTML")

for cmd in ["present_simple", "present_continuous", "present_perfect", "present_perfect_continuous",
            "past_simple", "past_continuous", "past_perfect", "past_perfect_continuous",
            "future_simple", "future_continuous", "future_perfect", "future_perfect_continuous", "pronouns"]:
    @bot.message_handler(commands=[cmd])
    def handle_tenses(message, c=cmd):
        bot.send_message(message.chat.id, grammar_rules[c], parse_mode="HTML")

# --- 4. MANGA VA RASMLARNI TARJIMA QILISH (FOTO) ---
@bot.message_handler(content_types=['photo'])
def handle_manga_photo(message):
    try:
        msg = bot.reply_to(message, "🖼️ Manga rasmi qabul qilindi. Matnlar o'qilmoqda, biroz kuting...")
        
        # Rasmni yuklab olish
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        image_path = "manga_temp.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        # EasyOCR orqali matnlarni o'qish
        natijalar = reader.readtext(image_path)
        
        if not natijalar:
            bot.edit_message_text("❌ Rasmdan hech qanday matn topilmadi!", message.chat.id, msg.message_id)
            if os.path.exists(image_path):
                os.remove(image_path)
            return

        response_text = "🌐 <b>Manga Tarjimasi (Inglizcha ➔ O'zbekcha):</b>\n\n"
        
        for i, (koordinata, matn, ishonchlilik) in enumerate(natijalar, 1):
            # MyMemory API orqali tarjima qilish
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(matn)}&langpair=en|uz"
            res = requests.get(url).json()
            translation = res.get('responseData', {}).get('translatedText', matn)
            
            response_text += f"<b>{i}. Asl:</b> {matn}\n<b>   Tarjima:</b> {translation}\n\n"

        # Vaqtinchalik faylni o'chirish
        if os.path.exists(image_path):
            os.remove(image_path)
            
        # Xabar uzunligi Telegram limitidan oshib ketmasligi uchun tekshirish
        if len(response_text) > 4096:
            response_text = response_text[:4090] + "..."
            
        bot.edit_message_text(response_text, message.chat.id, msg.message_id, parse_mode="HTML")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Rasmga ishlov berishda xatolik yuz berdi: {str(e)}")

# --- 5. MATNNI TARJIMA QILISH ---
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    user_text = message.text.strip()

    try:
        english_count = sum(1 for c in user_text if c.lower() in 'abcdefghijklmnopqrstuvwxyz')
        total_alpha = sum(1 for c in user_text if c.isalpha())

        if total_alpha > 0 and (english_count / total_alpha > 0.4):
            lang_pair = "en|uz"
            target_lang = "🇺🇿 O'zbekcha"
        else:
            lang_pair = "uz|en"
            target_lang = "🇬🇧 Inglizcha"

        # MyMemory bepul tarjima API
        url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(user_text)}&langpair={lang_pair}"
        response = requests.get(url)
        data = response.json()
        
        translation = data['responseData']['translatedText']

        bot.reply_to(
            message,
            f"🌐 <b>Tarjima ({target_lang}):</b>\n<code>{translation}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, f"❌ Tarjima qilishda xatolik yuz berdi.")

# --- 6. BOTNI ISHGA TUSHIRISH ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(none_stop=True)
