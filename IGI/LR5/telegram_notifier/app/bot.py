# app/bot.py
import json
from telegram.ext import ApplicationBuilder, CommandHandler, Updater
from .notifications import send_notification_to_server
from .logger_config import get_logger
from .config import Config

logger = get_logger(__name__)

TOKEN = Config.TELEGRAM_BOT_TOKEN


async def start(update, context):
    user = update.effective_user
    chat_id = update.effective_chat.id
    message = f"user @{user.username} обратился к боту. Id чата {chat_id}"
    logger.info(f"Пользователь начал взаимодействие: {message}")

    notification_data = {
        "channels": ["email", "telegram"],
        "message": message
    }
    await send_notification_to_server(notification_data)

    await update.message.reply_text(f"Ваш ID чата: {chat_id}")


# Создаем application один раз
application = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Получаем updater вручную
updater = Updater(bot=application.bot, update_queue=application.update_queue)
application.updater = updater