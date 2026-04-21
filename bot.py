import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8696969569:AAEVwgdATX26oI3SAU5I-rLI0Fr7yTSvg9Y"

DEADLINE = datetime(2026, 4, 23, 18, 50)

# список всех сообщений таймера (один таймер на всех)
timer_messages = []


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

    return (
        f"⏳ До события осталось:\n\n"
        f"{days} д {hours} ч {minutes} мин {seconds} сек"
    )


async def update_timer():
    while True:
        await asyncio.sleep(1)

        text = get_time_left()

        # копию списка, чтобы можно было удалять внутри цикла
        for msg in timer_messages[:]:
            try:
                await msg.edit_text(text)
            except:
                # сообщение удалено или ошибка → убираем
                timer_messages.remove(msg)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = await update.message.reply_text(get_time_left())

    # добавляем в общий список
    timer_messages.append(message)

    # если группа — пытаемся закрепить
    if chat.type != "private":
        try:
            await context.bot.pin_chat_message(chat.id, message.message_id)
        except:
            pass  # нет прав — просто игнорируем


async def on_startup(app):
    # запускаем общий таймер (ОДИН на весь бот)
    asyncio.create_task(update_timer())


app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
