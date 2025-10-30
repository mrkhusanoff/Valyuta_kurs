import os
import requests
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# .env fayldan BOT_TOKEN ni olish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Markaziy bank API manzili
CBU_API = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

@dp.message_handler(commands=['start', 'help'])
async def start_cmd(message: types.Message):
    text = (
        "👋 Assalomu alaykum!\n"
        "Men sizga O‘zbekiston Respublikasi Markaziy bankining bugungi valyuta kurslarini ko‘rsataman.\n\n"
        "💱 Quyidagi komandalarni sinab ko‘ring:\n"
        "• /kurs — Asosiy valyutalar (USD, EUR, RUB)\n"
        "• /kurs USD — faqat dollar kursi\n"
        "• /kurs EUR — faqat yevro kursi\n"
        "• /kurs RUB — faqat rubl kursi"
    )
    await message.answer(text)

@dp.message_handler(commands=['kurs'])
async def kurs_cmd(message: types.Message):
    args = message.get_args().upper()  # foydalanuvchi kiritgan valyuta kodi, masalan USD

    try:
        response = requests.get(CBU_API)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        await message.answer("⚠️ Ma’lumotlarni olishda xatolik yuz berdi.")
        print("Xato:", e)
        return

    if args:
        # Agar foydalanuvchi /kurs USD deb yozsa
        for valyuta in data:
            if valyuta["Ccy"] == args:
                await message.answer(
                    f"💵 <b>{valyuta['CcyNm_UZ']}</b>\n"
                    f"1 {valyuta['Ccy']} = {valyuta['Rate']} so‘m\n"
                    f"📅 Sana: {valyuta['Date']}",
                    parse_mode="HTML"
                )
                return
        await message.answer("❌ Bunday valyuta topilmadi. Masalan: /kurs USD")
    else:
        # Asosiy valyutalar: USD, EUR, RUB
        asosiy = ['USD', 'EUR', 'RUB']
        text = "💱 <b>Bugungi valyuta kurslari:</b>\n\n"
        for valyuta in data:
            if valyuta["Ccy"] in asosiy:
                text += f"{valyuta['Ccy']}: {valyuta['Rate']} so‘m\n"
        text += f"\n📅 Sana: {data[0]['Date']}"
        await message.answer(text, parse_mode="HTML")

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
