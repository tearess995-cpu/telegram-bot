import asyncio
from datetime import datetime, timedelta

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

TOKEN = "ТВОЙ_НОВЫЙ_ТОКЕН"

# Дедлайн (Ташкент)
DEADLINE = datetime(2026, 4, 23, 23, 50)


def get_time_left():
    # UTC +5 (Ташкент)
    now = datetime.utcnow() + timedelta(hours=5)

    diff = DEADLINE - now

    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60

    return (
        f"⏳ <b>До события осталось:</b>\n\n"
        f"📅 <b>Дни:</b> {days}\n"
        f"⏰ <b>Часы:</b> {hours}\n"
        f"🕐 <b>Минуты:</b> {minutes}"
    )


def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Обновить", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text(
        get_time_left(),
        reply_markup=get_keyboard(),
        parse_mode="HTML"
    )

    # автообновление каждую минуту
    while True:
        await asyncio.sleep(60)
        try:
            await message.edit_text(
                get_time_left(),
                reply_markup=get_keyboard(),
                parse_mode="HTML"
            )
        except:
            break


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await query.edit_message_text(
            get_time_left(),
            reply_markup=get_keyboard(),
            parse_mode="HTML"
        )
    except:
        pass


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
