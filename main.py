import os
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# .env dan tokenni o‘qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN topilmadi. .env faylni tekshiring!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Bank.uz sahifalari
URLS = {
    "USD": "https://bank.uz/uz/currency/USD",
    "RUB": "https://bank.uz/uz/currency/RUB",
}


def get_rates(currency):
    """bank.uz sahifasidan kurslarni xavfsiz o‘qish"""
    try:
        url = URLS.get(currency)
        if not url:
            return {}

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            return {}

        rows = table.find("tbody").find_all("tr")
        rates = {}

        for row in rows:
            cols = [col.get_text(strip=True) for col in row.find_all("td")]
            if len(cols) >= 4:
                buy_bank, buy_rate, sell_bank, sell_rate = cols[:4]
                rates[buy_bank] = {
                    "buy": buy_rate,
                    "sell": "—",
                }
                rates[sell_bank] = {
                    "buy": "—",
                    "sell": sell_rate,
                }
        return rates

    except Exception as e:
        print(f"❌ {currency} uchun xato:", e)
        return {}


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📊 Bugungi bank kurslari (USD + RUB)")
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Men sizga O‘zbekiston banklaridagi bugungi USD va RUB kurslarini ko‘rsataman.\n\n"
        "Quyidagi tugmani bosing 👇",
        reply_markup=keyboard,
    )


@dp.message_handler(lambda msg: msg.text == "📊 Bugungi bank kurslari (USD + RUB)")
async def show_rates(message: types.Message):
    await message.answer("⏳ Ma’lumotlar yuklanmoqda...")

    usd = get_rates("USD")
    rub = get_rates("RUB")

    if not usd and not rub:
        await message.answer("⚠️ Kurslarni olishda xatolik yuz berdi.")
        return

    banks = set(usd.keys()) | set(rub.keys())
    text = "🏦 <b>Bugungi USD va RUB kurslari (bank.uz)</b>\n\n"

    for bank in sorted(banks):
        usd_buy = usd.get(bank, {}).get("buy", "—")
        usd_sell = usd.get(bank, {}).get("sell", "—")
        rub_buy = rub.get(bank, {}).get("buy", "—")
        rub_sell = rub.get(bank, {}).get("sell", "—")

        text += (
            f"🏦 <b>{bank}</b>\n"
            f"💵 USD — Sotib olish: {usd_buy} | Sotish: {usd_sell}\n"
            f"💴 RUB — Sotib olish: {rub_buy} | Sotish: {rub_sell}\n\n"
        )

    # Telegram xabar limitidan oshmaslik uchun bo‘lib yuborish
    for i in range(0, len(text), 3500):
        await message.answer(text[i:i+3500], parse_mode="HTML")


if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
