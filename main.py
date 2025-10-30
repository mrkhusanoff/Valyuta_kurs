import requests
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

# Bot tokeni va chat_id (kanal yoki foydalanuvchi)
TOKEN = "BOT_TOKENINGIZNI_BU_YERGA_QO'YING"
CHAT_ID = "CHAT_ID_YOZING"  # Masalan: @kanalingiz yoki user id

bot = Bot(TOKEN)

# Valyuta kursini olish funksiyasi
def get_exchange_rate_to_uzs(currency_code):
    url = f"https://api.exchangerate.host/latest?base={currency_code}&symbols=UZS"
    response = requests.get(url)
    data = response.json()
    if "rates" in data and "UZS" in data["rates"]:
        return data["rates"]["UZS"]
    return None

# Kursni yuboradigan funksiya
async def send_daily_rate():
    usd_rate = get_exchange_rate_to_uzs("USD")
    rub_rate = get_exchange_rate_to_uzs("RUB")
    if usd_rate and rub_rate:
        message = f"💰 Bugungi kurs:\n\nUSD → UZS: {usd_rate:.2f} UZS\nRUB → UZS: {rub_rate:.2f} UZS"
    else:
        message = "Valyuta kursini olishda xatolik yuz berdi."
    await bot.send_message(chat_id=CHAT_ID, text=message)

# /start komandasi
async def start(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Har kuni soat 9:00 da kurslarni yuboraman.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # /start komandasi
    app.add_handler(CommandHandler("start", start))

    # Scheduler
    scheduler = AsyncIOScheduler()
    # Har kuni soat 9:00 da ishga tushadi
    scheduler.add_job(send_daily_rate, 'cron', hour=9, minute=0)
    scheduler.start()

    print("Bot ishga tushdi va har kuni soat 9:00 da kurslarni yuboradi...")
    app.run_polling()
