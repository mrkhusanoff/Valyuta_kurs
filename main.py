import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# .env fayldan tokenni o'qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

BANK_DATA = {
    "anor": {"USD_buy": 12080, "USD_sell": 12215, "RUB_buy": 135, "RUB_sell": 140},
    "agro": {"USD_buy": 12480, "USD_sell": 12570, "RUB_buy": 130, "RUB_sell": 138},
    "xalq": {"USD_buy": 12140, "USD_sell": 12250, "RUB_buy": 132, "RUB_sell": 139},
    "qishloq": {"USD_buy": 12070, "USD_sell": 12160, "RUB_buy": 129, "RUB_sell": 136},
    "kapital": {"USD_buy": 12070, "USD_sell": 12170, "RUB_buy": 128, "RUB_sell": 134},
    "hamkor": {"USD_buy": 12640, "USD_sell": 12730, "RUB_buy": 137, "RUB_sell": 143},
}

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    text = (
        "👋 Assalomu alaykum!\n"
        "Men sizga O‘zbekiston banklaridagi valyuta kurslarini ko‘rsataman.\n\n"
        "Quyidagi komandalarni tanlang:\n"
        "/anor - Anor Bank\n"
        "/agro - Agrobank\n"
        "/xalq - Xalq Bank\n"
        "/qishloq - Qishloq Qurilish Bank\n"
        "/kapital - Kapitalbank\n"
        "/hamkor - Hamkorbank"
    )
    await message.answer(text)

@dp.message_handler(commands=['anor', 'agro', 'xalq', 'qishloq', 'kapital', 'hamkor'])
async def bank_currency(message: types.Message):
    bank = message.text[1:].lower()
    data = BANK_DATA.get(bank)

    if not data:
        await message.answer("❌ Ma’lumot topilmadi.")
        return

    text = (
        f"🏦 {bank.capitalize()} Bank valyuta kurslari:\n\n"
        f"💵 USD:\n"
        f"  • Sotib olish: {data['USD_buy']} so‘m\n"
        f"  • Sotish: {data['USD_sell']} so‘m\n\n"
        f"💴 RUB:\n"
        f"  • Sotib olish: {data['RUB_buy']} so‘m\n"
        f"  • Sotish: {data['RUB_sell']} so‘m"
    )
    await message.answer(text)

if __name__ == '__main__':
    print("✅ Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
