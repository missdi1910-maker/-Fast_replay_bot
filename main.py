import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a friendly, helpful Telegram assistant. "
    "Answer naturally like a human. Keep replies concise."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("אני אונליין 🤍 כתבי לי מה שתרצי.")

async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    if not OPENAI_API_KEY:
        await update.message.reply_text("שגיאה: חסר OPENAI_API_KEY")
        return

    try:
        resp = client.responses.create(
            model="gpt-5",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        answer = (resp.output_text or "").strip()
        if not answer:
            answer = "…"
        await update.message.reply_text(answer[:3500])
    except Exception as e:
        await update.message.reply_text("משהו השתבש, נסי שוב.")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set. Add it in Railway Variables.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    app.run_polling()

if __name__ == "__main__":
    main()
