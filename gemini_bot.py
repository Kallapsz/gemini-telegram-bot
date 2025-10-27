import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

# === Настройки (используем переменные окружения Render) ===
BOT_TOKEN = os.getenv("8366778971:AAF93pSknWi8n641oSQ9gqC_R6sitgt5Jb0")
GEMINI_API_KEY = os.getenv("AIzaSyD00Ct0fyuFakJDMR4YH8FvQd3E6UMRRAg")

# Инициализация Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# === Функция генерации ответа ===
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text or "🤖 (Пустой ответ от Gemini)"
    except Exception as e:
        return f"⚠️ Ошибка Gemini: {e}"

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    bot_username = context.bot.username

    # Реагируем только на упоминание бота
    if message.text and f"@{bot_username}" in message.text:
        user_prompt = message.text.replace(f"@{bot_username}", "").strip()
        reply = ask_gemini(user_prompt or "Привет! Чем могу помочь?")
        await message.reply_text(reply)

# === Запуск бота ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Gemini бот запущен!")
app.run_polling()



