import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = "8696969569:AAEVwgdATX26oI3SAU5I-rLI0Fr7yTSvg9Y"

DEADLINE = datetime(2026, 4, 23, 18, 50)
START_TIME = datetime(2026, 2, 28, 0, 0)

timer_messages = []


def get_progress_bar():
    now = datetime.now()

    total = (DEADLINE - START_TIME).total_seconds()
    passed = (now - START_TIME).total_seconds()

    progress = max(0, min(1, passed / total if total > 0 else 0))

    bars = 16
    filled = int(progress * bars)

    bar = ""
    for i in range(bars):
        if i < filled:
            bar += "█"
        elif i == filled:
            bar += "●"
        else:
            bar += "░"

    percent = int(progress * 100)

    return f"{bar} {percent}%"


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
        "✈️ <b>Поездка в Таиланд</b>\n\n"
        "━━━━━━━━━━━━━━━\n"
        "🔄 Обновляется каждые 10 секунд\n\n"
        f"📅 <b>Осталось:</b>\n"
        f"{days} д {hours} ч {minutes} мин {seconds} сек\n\n"
        f"📊 <b>Прогресс (от покупки билетов до полета):</b>\n"
        f"{progress}\n"
        "━━━━━━━━━━━━━━━"
    )


async def update_timer():
    while True:
        await asyncio.sleep(10)

        text = get_time_left()

        for msg in timer_messages[:]:
            try:
                await msg.edit_text(text, parse_mode="HTML")
            except BadRequest as e:
                if "message to edit not found" in str(e).lower():
                    timer_messages.remove(msg)
            except:
                pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = await update.message.reply_text(
        get_time_left(),
        parse_mode="HTML"
    )

    timer_messages.append(message)

    if chat.type != "private":
        try:
            await context.bot.pin_chat_message(chat.id, message.message_id)
        except:
            pass


async def on_startup(app):
    asyncio.create_task(update_timer())


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
