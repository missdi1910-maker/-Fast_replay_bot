import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# ===== VARIABLES =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ===== OPENAI =====
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a friendly, human-like Telegram assistant. "
    "Reply naturally and helpfully. Keep answers concise."
)

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("אני אונליין 🤍 כתבי לי מה שבא לך.")

async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    if not OPENAI_API_KEY:
        await update.message.reply_text("שגיאה: אין מפתח OPENAI_API_KEY")
        return

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )

        answer = response.output_text
        if not answer:
            answer = "…"

        await update.message.reply_text(answer[:3500])

    except Exception as e:
        await update.message.reply_text(f"שגיאה: {e}")

# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))
    app.run_polling()

if __name__ == "__main__":
    main()
