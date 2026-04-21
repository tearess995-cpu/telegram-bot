from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
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

async def update_timer(message):
    while True:
        await asyncio.sleep(60)
        try:
            await message.edit_text(
                f"⏳ До события осталось:\n\n{get_time_left()}"
            )
        except:
            break


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # если это личка
    if update.effective_chat.type == "private":
        if user_id in user_messages:
            try:
                await user_messages[user_id].edit_text(
                    f"⏳ До события осталось:\n\n{get_time_left()}"
                )
                return
            except:
                pass

        message = await update.message.reply_text(
            f"⏳ До события осталось:\n\n{get_time_left()}"
        )

        user_messages[user_id] = message
        asyncio.create_task(update_timer(message))

    else:
        # если группа
        if chat_id in chat_messages:
            try:
                await chat_messages[chat_id].edit_text(
                    f"⏳ До события осталось:\n\n{get_time_left()}"
                )
                return
            except:
                pass

        message = await update.message.reply_text(
            f"⏳ До события осталось:\n\n{get_time_left()}"
        )

        chat_messages[chat_id] = message
        asyncio.create_task(update_timer(message))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
