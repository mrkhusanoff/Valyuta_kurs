import os
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

# .env dan tokenni o'qish
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN topilmadi. .env faylni tekshiring!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

URL_USD = "https://bank.uz/uz/currency/USD"
URL_RUB = "https://bank.uz/uz/currency/RUB"

def get_currency_data(url):
    """Berilgan valyuta sahifasidan (USD yoki RUB) kurslarni olish"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        rows = table.find("tbody").find_all("tr")
        data = []

        for row in rows:
            cols = [col.get_text(strip=True) for col in row.find_all("td")]
            if len(cols) >= 4:
                buy_bank = cols[0]
                buy_rate = cols[1]
                sell_bank = cols[2]
                sell_rate = cols[3]
                data.append({
                    "buy_bank": buy_bank,
                    "buy_rate": buy_rate,
                    "sell_bank": sell_bank,
                    "sell_rate": sell_rate
                })
        return data
    except Exception as e:
        print("❌ Xatolik:", e)
        return []

def merge_usd_rub(usd_data, rub_data):
    """USD va RUB ma'lumotlarini bank nomi bo‘yicha birlashtirish"""
    merged = {}
    for item in usd_data:
        bank = item["buy_bank"]
        merged[bank] = {
            "USD_buy": item["buy_rate"],
            "USD_sell": item["sell_rate"]
        }

    for item in rub_data:
        bank = item["buy_bank"]
        if bank not in merged:
            merged[bank] = {}
        merged[bank]["RUB_buy"] = item["buy_rate"]
        merged[bank]["RUB_sell"] = item["sell_rate"]

    return merged


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📊 Bugungi bank kurslari (USD + RUB)")
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Men sizga O‘zbekiston banklaridagi bugungi USD va RUB kurslarini ko‘rsataman.\n\n"
        "Quyidagi tugmani bosing 👇",
        reply_markup=keyboard
    )


@dp.message_handler(lambda msg: msg.text == "📊 Bugungi bank kurslari (USD + RUB)")
async def show_rates(message: types.Message):
    await message.answer("⏳ Ma’lumotlar yuklanmoqda, iltimos kuting...")

    usd_data = get_currency_data(URL_USD)
    rub_data = get_currency_data(URL_RUB)

    if not usd_data or not rub_data:
        await message.answer("⚠️ Ma’lumotlarni olishda xatolik yuz berdi.")
        return

    merged = merge_usd_rub(usd_data, rub_data)

    text = "🏦 <b>Bugungi banklar bo‘yicha USD va RUB kurslari</b>\n\n"

    for bank, rates in merged.items():
        usd_buy = rates.get("USD_buy", "—")
        usd_sell = rates.get("USD_sell", "—")
        rub_buy = rates.get("RUB_buy", "—")
        rub_sell = rates.get("RUB_sell", "—")

        text += (
            f"🏦 <b>{bank}</b>\n"
            f"💵 <b>USD:</b>\n"
            f"  • Sotib olish: {usd_buy}\n"
            f"  • Sotish: {usd_sell}\n"
            f"💴 <b>RUB:</b>\n"
            f"  • Sotib olish: {rub_buy}\n"
            f"  • Sotish: {rub_sell}\n\n"
        )

    if len(text) > 4000:
        for i in range(0, len(text), 4000):
            await message.answer(text[i:i+4000], parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")


if __name__ == "__main__":
    print("🤖 Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
