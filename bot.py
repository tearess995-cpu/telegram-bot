import asyncio
from datetime import datetime

DEADLINE = datetime(2026, 4, 23, 18, 50,)

def get_time_left():
    now = datetime.now
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8696969569:AAEVwgdATX26oI3SAU5I-rLI0Fr7yTSvg9Y"

DEADLINE = datetime(2026, 4, 23, 18, 50)

def get_time_left():
    now = datetime.now()
    diff = DEADLINE - now

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    return f"{days} д {hours} ч {minutes} мин"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text(
        f"⏳ До события осталось:\n\n{get_time_left()}"
    )

    while True:
        await asyncio.sleep(60)
        try:
            await message.edit_text(
                f"⏳ До события осталось:\n\n{get_time_left()}"
            )
        except:
            break

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
