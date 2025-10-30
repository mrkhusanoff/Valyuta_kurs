import os
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# .env dan tokenni o'qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN topilmadi. .env faylni tekshiring!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# CBU API manzili
CBU_API = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

def get_cbu_rates():
    """CBU API'dan bugungi kurslarni olish."""
    try:
        response = requests.get(CBU_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Xatolik:", e)
        return None

def format_rates(data):
    """Valyuta kurslarini chiroyli formatda chiqaradi."""
    if not data:
        return "⚠️ Kurslarni olishda xatolik yuz berdi."
    lines = []
    date = data[0].get("Date") if data else "—"
    lines.append(f"💱 <b>Bugungi valyuta kurslari</b>\n📅 Sana: {date}\n")
    for v in data:
        ccy = v.get("Ccy")
        name = v.get("CcyNm_UZ")
        rate = v.get("Rate")
        nominal = v.get("Nominal")
        lines.append(f"<b>{ccy}</b> — {name}\n1 × {nominal} {ccy} = {rate} so‘m\n")
    return "\n".join(lines)

# /start komandasi — tugmali menyu bilan
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📊 Bugungi kurslar")
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Men sizga O‘zbekiston Markaziy Bankining bugungi valyuta kurslarini ko‘rsataman.\n\n"
        "Quyidagi tugmani bosing 👇",
        reply_markup=keyboard
    )

# Tugma bosilganda — kurslarni ko‘rsatish
@dp.message_handler(lambda msg: msg.text == "📊 Bugungi kurslar")
async def show_all_rates(message: types.Message):
    await message.answer("⏳ Kurslar yuklanmoqda...")
    data = get_cbu_rates()
    text = format_rates(data)
    MAX_LEN = 4000
    if len(text) <= MAX_LEN:
        await message.answer(text, parse_mode="HTML")
    else:
        # agar matn uzun bo‘lsa, bo‘lib yuborish
        for i in range(0, len(text), MAX_LEN):
            await message.answer(text[i:i+MAX_LEN], parse_mode="HTML")

if __name__ == '__main__':
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)