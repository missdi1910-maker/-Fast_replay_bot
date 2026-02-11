import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я онлайн ✅ Напиши мне что-нибудь.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Простой ответ: повторяет сообщение
    await update.message.reply_text(update.message.text)

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Add it in Railway Variables.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()
