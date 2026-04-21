import asyncio
from datetime import datetime

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "ТВОЙ_ТОКЕН"

DEADLINE = datetime(2026, 4, 23, 18, 50)


def get_time_left():
    now = datetime.now()
    diff = DEADLINE - now

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    return f"⏳ До события осталось:\n\n{days} д {hours} ч {minutes} мин"


def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text(
        get_time_left(),
        reply_markup=get_keyboard()
    )

    # автообновление
    while True:
        await asyncio.sleep(60)
        try:
            await message.edit_text(
                get_time_left(),
                reply_markup=get_keyboard()
            )
        except:
            break


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            get_time_left(),
            reply_markup=get_keyboard()
        )
    except:
        pass


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
