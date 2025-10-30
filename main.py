import os
from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv

# .env dan tokenni olish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Bank ma'lumotlari (statik)
BANK_DATA = {
    "anor": {"USD_buy": 12080, "USD_sell": 12215, "RUB_buy": 135, "RUB_sell": 140},
    "agro": {"USD_buy": 12480, "USD_sell": 12570, "RUB_buy": 130, "RUB_sell": 138},
    "xalq": {"USD_buy": 12140, "USD_sell": 12250, "RUB_buy": 132, "RUB_sell": 139},
    "qishloq": {"USD_buy": 12070, "USD_sell": 12160, "RUB_buy": 129, "RUB_sell": 136},
    "kapital": {"USD_buy": 12070, "USD_sell": 12170, "RUB_buy": 128, "RUB_sell": 134},
    "hamkor": {"USD_buy": 12640, "USD_sell": 12730, "RUB_buy": 137, "RUB_sell": 143},
}

# /start komandasi
@dp.message_handler(commands=['start', 'banklar'])
async def start_cmd(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🏦 Anor Bank", callback_data="anor"),
        types.InlineKeyboardButton("🌾 Agrobank", callback_data="agro"),
        types.InlineKeyboardButton("👨‍💼 Xalq Bank", callback_data="xalq"),
        types.InlineKeyboardButton("🏗 Qishloq Qurilish Bank", callback_data="qishloq"),
        types.InlineKeyboardButton("💰 Kapitalbank", callback_data="kapital"),
        types.InlineKeyboardButton("🤝 Hamkorbank", callback_data="hamkor"),
    ]
    keyboard.add(*buttons)

    text = "💱 Quyidagi banklardan birini tanlang:"
    await message.answer(text, reply_markup=keyboard)

# Inline tugmalar bosilganda ishlovchi handler
@dp.callback_query_handler(lambda c: c.data in BANK_DATA.keys())
async def bank_callback(callback_query: types.CallbackQuery):
    bank = callback_query.data
    data = BANK_DATA[bank]

    text = (
        f"🏦 <b>{bank.capitalize()} Bank</b> valyuta kurslari:\n\n"
        f"💵 <b>USD</b>:\n"
        f"  • Sotib olish: {data['USD_buy']} so‘m\n"
        f"  • Sotish: {data['USD_sell']} so‘m\n\n"
        f"💴 <b>RUB</b>:\n"
        f"  • Sotib olish: {data['RUB_buy']} so‘m\n"
        f"  • Sotish: {data['RUB_sell']} so‘m"
    )

    await callback_query.answer()  # "loading..." ni to‘xtatadi
    await bot.send_message(callback_query.from_user.id, text, parse_mode="HTML")

if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)