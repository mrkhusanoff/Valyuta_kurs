# 💱 O‘zbekiston Bank Valyuta Kurslari Telegram Boti

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Framework-Aiogram-lightgrey)](https://docs.aiogram.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

🇺🇿 Ushbu bot **O‘zbekiston Respublikasi Markaziy Banki API** orqali valyuta kurslarini olib,
Telegram foydalanuvchilariga qulay tarzda taqdim etadi.

---

## ✨ Asosiy imkoniyatlar

- 💵 USD, EUR, RUB, GBP va boshqa valyutalarning hozirgi kurslarini olish  
- 📅 Sana bo‘yicha tarixiy kurslarni so‘rash  
- ⚙️ `.env` fayli orqali tokenni xavfsiz saqlash  
- ☁️ Railway yoki Render kabi platformalarda deploy qilishga tayyor  
- 🧩 Aiogram yordamida asinxron ishlov

---

## 🧰 Texnologiyalar

- **Python 3.10+**  
- **Aiogram** — Telegram bot framework  
- **Requests** — tashqi API’lardan ma’lumot olish uchun  
- **python-dotenv** — muhit o‘zgaruvchilarini boshqarish uchun  

---

## 🧾 Ishga tushirish (qisqa)

```bash
git clone https://github.com/mrkhusanoff/valyuta_kurs.git
cd valyuta_kurs
pip install -r requirements.txt
echo "BOT_TOKEN=YOUR_BOT_TOKEN_HERE" > .env
python main.py
