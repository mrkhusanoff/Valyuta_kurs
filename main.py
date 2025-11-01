import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# 🔑 Telegram tokeningizni shu yerga yozing
TOKEN = "YOUR_BOT_TOKEN_HERE"

# 🏦 Banklar va ularning kurslari (misol uchun)
BANK_RATES = {
    "Kapitalbank": {"USD": 12170, "RUB": 155},
    "Hamkorbank": {"USD": 12090, "RUB": 150},
    "Ipak Yo‘li Bank": {"USD": 12100, "RUB": 152},
    "Agrobank": {"USD": 12050, "RUB": 148},
    "Asia Alliance Bank": {"USD": 12080, "RUB": 151},
    "TBC Bank": {"USD": 12120, "RUB": 153},
    "Xalq Bank": {"USD": 12040, "RUB": 149},
    "Anorbank": {"USD": 12110, "RUB": 154},
}

# 🎬 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Bank kurslari", callback_data="kurslar")],
        [InlineKeyboardButton("🧮 Kalkulyator", callback_data="kalkulyator")]
    ]
    await update.message.reply_text(
        "👋 Assalomu alaykum!\nValyuta botiga xush kelibsiz.\n\nBo‘limni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 📲 Inline tugmalarni ishlovchi
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "kurslar":
        text = (
            "🏦 Iltimos, bank nomini kiriting:\n"
            "(Masalan: Kapitalbank, Hamkorbank, Xalq Bank, Anorbank ...)"
        )
        context.user_data["kurs_mode"] = True
        context.user_data["calc_mode"] = False
        await query.edit_message_text(text=text)

    elif query.data == "kalkulyator":
        text = (
            "🧮 Kalkulyator rejimi yoqildi.\n\n"
            "Masalan:\n"
            "👉 `100 USD @ Kapitalbank`\n"
            "👉 `5000 RUB @ Anorbank`"
        )
        context.user_data["calc_mode"] = True
        context.user_data["kurs_mode"] = False
        await query.edit_message_text(text=text)

# 💬 Xabarlar uchun handler
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # 🏦 Bank kursini ko‘rsatish
    if context.user_data.get("kurs_mode"):
        for bank in BANK_RATES:
            if text.lower() in bank.lower():
                rates = BANK_RATES[bank]
                reply = (
                    f"🏦 {bank}\n\n"
                    f"💵 1 USD = {rates['USD']} so‘m\n"
                    f"₽ 1 RUB = {rates['RUB']} so‘m"
                )
                await update.message.reply_text(reply)
                return
        await update.message.reply_text("❌ Bunday bank topilmadi. Iltimos, to‘liq nomini yozing.")

    # 🧮 Kalkulyator funksiyasi
    elif context.user_data.get("calc_mode"):
        try:
            amt_str, cur_bank = text.split("@")
            amt_str = amt_str.strip()
            cur_bank = cur_bank.strip()
            amount, currency = amt_str.split()
            amount = float(amount)
            currency = currency.upper()

            if cur_bank not in BANK_RATES:
                await update.message.reply_text("❌ Bunday bank topilmadi.")
                return

            if currency not in ("USD", "RUB"):
                await update.message.reply_text("⚠️ Faqat USD yoki RUB ishlaydi.")
                return

            rate = BANK_RATES[cur_bank][currency]
            result = amount * rate
            await update.message.reply_text(
                f"{amount} {currency} @ {cur_bank} = {result:,.2f} so‘m"
            )
        except Exception:
            await update.message.reply_text(
                "❌ Format xato.\nTo‘g‘ri yozish misollari:\n"
                "`100 USD @ Xalq Bank`\n`5000 RUB @ Anorbank`"
            )
    else:
        await update.message.reply_text("ℹ️ Avval /start buyrug‘ini yuboring.")

# 🚀 Botni ishga tushirish
def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
