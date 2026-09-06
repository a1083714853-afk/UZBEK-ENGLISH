import os
from flask import Flask
from threading import Thread
import telebot
from googletrans import Translator

TOKEN = "8988660751:AAEVxSose38VxX6v0XhjajzbJEjejre50Ps"
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

    # --- PRESENT (HOZIRGI ZAMONLAR) ---
    "present_simple": (
        "🟢 <b>1. Present Simple (Hozirgi oddiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Doimiy takrorlanadigan, odat tusiga kirgan, umumiy haqiqat bo'lgan harakatlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: I/We/You/They + V1 | He/She/It + V1(-s/-es)\n"
        "• So'roq gap: Do / Does + Ega + V1?\n"
        "• Inkor gap: Do not (don't) / Does not (doesn't) + V1\n\n"
        "<i>Misollar:</i>\n"
        "• I work every day. (Men har kuni ishlayman.)\n"
        "• She speaks English well. (U yaxshi inglizcha gaplashadi.)"
    ),
    "present_continuous": (
        "🟢 <b>2. Present Continuous (Hozirgi davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Ayni paytda (nutq so'zlanayotgan vaqtda) bo'layotgan jarayonlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + am/is/are + V(-ing)\n"
        "• So'roq gap: Am/Is/Are + Ega + V(-ing)?\n"
        "• Inkor gap: Ega + am/is/are + not + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• I am reading a book now. (Men hozir kitob o'qiyapman.)\n"
        "• They are playing football. (Ular futbol o'ynashyapti.)"
    ),
    "present_perfect": (
        "🟢 <b>3. Present Perfect (Hozirgi tugallangan zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Harakat tugallangan, lekin uning natijasi hozirgi paytda muhim bo'lsa.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: I/We/You/They + have + V3 | He/She/It + has + V3\n"
        "• So'roq gap: Have / Has + Ega + V3?\n"
        "• Inkor gap: Have / Has + not + V3\n\n"
        "<i>Misollar:</i>\n"
        "• I have already finished my homework. (Men uy vazifamni allaqachon tugatdim.)\n"
        "• She has lost her keys. (U kalitlarini yo'qotib qo'ygan - hozir ham yo'q.)"
    ),
    "present_perfect_continuous": (
        "🟢 <b>4. Present Perfect Continuous (Hozirgi tugallangan-davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> O'tmishda boshlanib, hozirgi kunga qadar davom etayotgan va hali ham davom etayotgan jarayonlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + have/has + been + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• I have been living here for 5 years. (Men bu yerda 5 yildan beri yashayapman.)\n"
        "• It has been raining since morning. (Ertalabdan beri yomg'ir yog'yapti.)"
    ),

    # --- PAST (O'TGAN ZAMONLAR) ---
    "past_simple": (
        "🟠 <b>5. Past Simple (O'tgan oddiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> O'tgan zamonda aniq bir vaqtda sodir bo'lgan va tugagan harakatlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + V2 (noto'g'ri fe'llarning 2-shakli yoki -ed qo'shimchasi)\n"
        "• So'roq gap: Did + Ega + V1?\n"
        "• Inkor gap: Did not (didn't) + V1\n\n"
        "<i>Misollar:</i>\n"
        "• I went to Tashkent yesterday. (Men kecha Toshkentga bordim.)\n"
        "• She watched a movie. (U kino ko'rdi.)"
    ),
    "past_continuous": (
        "🟠 <b>6. Past Continuous (O'tgan davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> O'tgan zamonda ma'lum bir aniq paytda davom etib turgan jarayon uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + was/were + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• I was reading a book at 5 PM yesterday. (Kecha soat 5 da kitob o'qiyotgan edim.)\n"
        "• They were sleeping when I came. (Men kelganimda ular uxlab yotishgandi.)"
    ),
    "past_perfect": (
        "🟠 <b>7. Past Perfect (O'tgan tugallangan zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> O'tgan zamondagi boshqa bir harakatdan oldinroq tugagan ish-harakat uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + had + V3\n\n"
        "<i>Misollar:</i>\n"
        "• When I arrived, the train had already left. (Men kelganimda, poyezd allaqachon jo'nab ketgandi.)"
    ),
    "past_perfect_continuous": (
        "🟠 <b>8. Past Perfect Continuous (O'tgan tugallangan-davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> O'tgan zamonda ma'lum bir vaqtgacha davom etib kelgan va o'shanda tugagan jarayon.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + had + been + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• He had been working for 3 hours before I met him. (Men u bilan uchrashgunimcha u 3 soatdan beri ishlab turgandi.)"
    ),

    # --- FUTURE (KELASI ZAMONLAR) ---
    "future_simple": (
        "🔵 <b>9. Future Simple (Kelasi oddiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Kelajakda sodir bo'ladigan ish-harakatlar (rejalashtirilmagan, to'satdan qilingan qarorlar) uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + will + V1\n"
        "• So'roq gap: Will + Ega + V1?\n"
        "• Inkor gap: Will not (won't) + V1\n\n"
        "<i>Misollar:</i>\n"
        "• I will help you tomorrow. (Men senga ertaga yordam beraman.)\n"
        "• It will rain tomorrow. (Ertaga yomg'ir yog'adi.)"
    ),
    "future_continuous": (
        "🔵 <b>10. Future Continuous (Kelasi davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Kelajakda ma'lum bir vaqtda davom etib turadigan jarayonlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + will be + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• At this time tomorrow, I will be flying to London. (Ertaga bu vaqtda men Londonga uchib ketayotgan bo'laman.)"
    ),
    "future_perfect": (
        "🔵 <b>11. Future Perfect (Kelasi tugallangan zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Kelajakdagi ma'lum bir vaqtgacha tugallangan bo'ladigan harakatlar uchun.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + will have + V3\n\n"
        "<i>Misollar:</i>\n"
        "• I will have finished this book by tomorrow. (Men ertagacha bu kitobni o'qib tugatgan bo'laman.)"
    ),
    "future_perfect_continuous": (
        "🔵 <b>12. Future Perfect Continuous (Kelasi tugallangan-davomiy zamon)</b>\n\n"
        "<b>Qachon ishlatiladi?</b> Kelajakdagi ma'lum bir vaqtgacha boshlanib, o'sha paytgacha davom etib kelayotgan bo'ladigan jarayon.\n"
        "<b>Formulasi:</b>\n"
        "• Darak gap: Ega + will have been + V(-ing)\n\n"
        "<i>Misollar:</i>\n"
        "• By next year, I will have been living here for 10 years. (Kelgusi yilga kelib, bu yerda yashayotganimga 10 yil bo'ladi.)"
    ),

    # --- OLMOSHLAR ---
    "pronouns": (
        "👥 <b>Olmoshlar (Pronouns):</b>\n\n"
        "• I — Men\n"
        "• You — Sen / Siz\n"
        "• He — U (o'g'il bola)\n"
        "• She — U (qiz bola)\n"
        "• It — U (narsalar va hayvonlar uchun)\n"
        "• We — Biz\n"
        "• They — Ular"
    )
}

# --- 2. RENDER UCHUN FLASK SERVERI ---
app = Flask('')


@app.route('/')
def home():
    return "Ingliz tili boti ishlayapti va uyg'oq!"


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
        "Assalomu alaykum! 🌟 Ingliz tili tarjima va grammatika botiga xush kelibsiz.\n\n"
        "🔍 Istalgan so'z yoki matnni yozing — Google Translate orqali tarjima qilaman.\n"
        "📖 12 ta zamon va qoidalarni ko'rish uchun /tenses buyrug'ini yuboring.",
        parse_mode="HTML"
    )


# Asosiy zamonlar menyusi
@bot.message_handler(commands=['tenses', 'grammar'])
def send_tenses_menu(message):
    bot.send_message(message.chat.id, grammar_rules["tenses_menu"], parse_mode="HTML")


# Har bir zamon uchun alohida buyruqlar
@bot.message_handler(commands=['present_simple'])
def p_simple(message): bot.send_message(message.chat.id, grammar_rules["present_simple"], parse_mode="HTML")


@bot.message_handler(commands=['present_continuous'])
def p_cont(message): bot.send_message(message.chat.id, grammar_rules["present_continuous"], parse_mode="HTML")


@bot.message_handler(commands=['present_perfect'])
def p_perf(message): bot.send_message(message.chat.id, grammar_rules["present_perfect"], parse_mode="HTML")


@bot.message_handler(commands=['present_perfect_continuous'])
def p_perf_cont(message): bot.send_message(message.chat.id, grammar_rules["present_perfect_continuous"],
                                           parse_mode="HTML")


@bot.message_handler(commands=['past_simple'])
def past_simp(message): bot.send_message(message.chat.id, grammar_rules["past_simple"], parse_mode="HTML")


@bot.message_handler(commands=['past_continuous'])
def past_cont(message): bot.send_message(message.chat.id, grammar_rules["past_continuous"], parse_mode="HTML")


@bot.message_handler(commands=['past_perfect'])
def past_perf(message): bot.send_message(message.chat.id, grammar_rules["past_perfect"], parse_mode="HTML")


@bot.message_handler(commands=['past_perfect_continuous'])
def past_perf_cont(message): bot.send_message(message.chat.id, grammar_rules["past_perfect_continuous"],
                                              parse_mode="HTML")


@bot.message_handler(commands=['future_simple'])
def fut_simp(message): bot.send_message(message.chat.id, grammar_rules["future_simple"], parse_mode="HTML")


@bot.message_handler(commands=['future_continuous'])
def fut_cont(message): bot.send_message(message.chat.id, grammar_rules["future_continuous"], parse_mode="HTML")


@bot.message_handler(commands=['future_perfect'])
def fut_perf(message): bot.send_message(message.chat.id, grammar_rules["future_perfect"], parse_mode="HTML")


@bot.message_handler(commands=['future_perfect_continuous'])
def fut_perf_cont(message): bot.send_message(message.chat.id, grammar_rules["future_perfect_continuous"],
                                             parse_mode="HTML")


@bot.message_handler(commands=['pronouns'])
def pronouns(message): bot.send_message(message.chat.id, grammar_rules["pronouns"], parse_mode="HTML")


# --- 4. GOOGLE TRANSLATE ORQALI AVTOMATIK TARJIMA QILISH ---
@bot.message_handler(func=lambda message: True)
def translate_text(message):
    user_text = message.text.strip()

    try:
        detected = translator.detect(user_text)

        if detected.lang == 'en':
            translation = translator.translate(user_text, src='en', dest='uz')
            target_lang = "🇺🇿 O'zbekcha"
        else:
            translation = translator.translate(user_text, dest='en')
            target_lang = "🇬🇧 Inglizcha"

        bot.reply_to(
            message,
            f"🌐 <b>Google Translate ({target_lang}):</b>\n<code>{translation.text}</code>",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, tarjima qilishda xatolik yuz berdi. Qaytadan urinib ko'ring 😔.")


# --- 5. BOTNI ISHGA TUSHIRISH ---
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
