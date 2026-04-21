import asyncio
from datetime import datetime, timezone, timedelta

UZB_TZ = timezone(timedelta(hours=5))

DEADLINE = datetime(2026, 4, 23, 23, 50, tzinfo=UZB_TZ)

def get_time_left():
    now = datetime.now(UZB_TZ)
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8696969569:AAEVwgdATX26oI3SAU5I-rLI0Fr7yTSvg9Y"

DEADLINE = datetime(2026, 4, 23, 23, 50)

def get_time_left():
    now = datetime.now(UZB_TZ)
    diff = DEADLINE - now

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    return f"СЕЙЧАС: {now}\n\n⏳ Осталось:\n{days} д {hours} ч {minutes} мин"

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
