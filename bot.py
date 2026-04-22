import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest

TOKEN = "8696969569:AAEVwgdATX26oI3SAU5I-rLI0Fr7yTSvg9Y"

DEADLINE = datetime(2026, 4, 23, 18, 50)

timer_messages = []


def format_time(n):
    return f"{n:02d}"


def get_time_left():
    now = datetime.now()
    diff = DEADLINE - now

    total_seconds = int(diff.total_seconds())

    if total_seconds <= 0:
        return "✈️ Вылет начался\nХорошей поездки 🇹🇭"

    total_hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    time_str = f"{total_hours}:{format_time(minutes)}:{format_time(seconds)}"

    return (
    f"Осталось {time_str}\n"
    "\n"
    "✈️ Поездка в Таиланд\n"
    "TAS → HKT 🇹🇭\n"
    "\n"
    "Таймер обновляется каждые 10 секунд"
)


async def update_timer():
    while True:
        await asyncio.sleep(10)

        text = get_time_left()

        for msg in timer_messages[:]:
            try:
                await msg.edit_text(text)
            except BadRequest as e:
                if "message to edit not found" in str(e).lower():
                    timer_messages.remove(msg)
            except:
                pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = await context.bot.send_message(
        chat_id=chat.id,
        text=get_time_left()
    )

    timer_messages.append(message)

    # закрепление в группе
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
