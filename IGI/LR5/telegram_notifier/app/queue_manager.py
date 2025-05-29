import asyncio
from telegram import Bot
from .logger_config import get_logger
from .config import Config

logger = get_logger(__name__)
queue = asyncio.Queue()
bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)

async def send_from_queue():
    while True:
        if not queue.empty():
            chat_id, message = await queue.get()
            try:
                await bot.send_message(chat_id=chat_id, text=message)
                logger.debug(f"Сообщение отправлено в чат {chat_id}: {message}")
            except Exception as e:
                logger.error(f"Ошибка отправки в чат {chat_id}: {e}")
        else:
            await asyncio.sleep(Config.QUEUE_PROCESS_INTERVAL)

def add_to_queue(chat_id, message):
    queue.put_nowait((chat_id, message))