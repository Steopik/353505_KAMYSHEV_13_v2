import httpx
from typing import List
from .logger_config import get_logger
from .config import Config


logger = get_logger(__name__)


async def route_email(emails: List[str], subject: str, message: str):
    payload = {
        "to": ", ".join(emails),
        "subject": subject,
        "body": message
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(Config.EMAIL_SERVICE_URL, json=payload)
            logger.debug(f"Email отправлен на {', '.join(emails)}")
        except Exception as e:
            logger.error(f"Ошибка при отправке email: {e}")


async def route_telegram(chat_ids: List[int], message: str):
    payload = {
        "message": message,
        "chats_id": chat_ids
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(Config.TELEGRAM_BOT_URL, json=payload)
            logger.debug(f"Telegram-сообщение отправлено в чаты {chat_ids}")
        except Exception as e:
            logger.error(f"Ошибка при отправке в Telegram: {e}")