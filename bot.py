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
    ContextTypes,
    CallbackQueryHandler
)
from telegram.error import BadRequest

TOKEN = "ТВОЙ_ТОКЕН"

DEADLINE = datetime(2026, 4, 23, 18, 50)
START_TIME = datetime.now()

timer_messages = []


def get_progress_bar():
    now = datetime.now()

    total = (DEADLINE - START_TIME).total_seconds()
    passed = (now - START_TIME).total_seconds()

    progress = max(0, min(1, passed / total if total > 0 else 0))

    bars = 10
    filled = int(progress * bars)
    empty = bars - filled

    return f"[{'█' * filled}{'░' * empty}] {int(progress * 100)}%"


def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Обновить сейчас", callback_data="refresh")]
    ])


def get_time_left():
    now = datetime.now()
    diff = DEADLINE - now

    total_seconds = int(diff.total_seconds())

    if total_seconds <= 0:
        return "🎉 Событие началось!"

    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    progress = get_progress_bar()

    return (
        f"⏳ До события осталось:\n\n"
        f"{days} д {hours} ч {minutes} мин {seconds} сек\n\n"
        f"{progress}"
    )


async def update_timer():
    while True:
        await asyncio.sleep(10)

        text = get_time_left()

        for msg in timer_messages[:]:
            try:
                await msg.edit_text(
                    text,
                    reply_markup=get_keyboard()
                )
            except BadRequest as e:
                if "message to edit not found" in str(e).lower():
                    timer_messages.remove(msg)
            except:
                pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = await update.message.reply_text(
        get_time_left(),
        reply_markup=get_keyboard()
    )

    timer_messages.append(message)

    if chat.type != "private":
        try:
            await context.bot.pin_chat_message(chat.id, message.message_id)
        except:
            pass


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


async def on_startup(app):
    asyncio.create_task(update_timer())


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
