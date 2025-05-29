# app/notifications.py

import aiohttp
from .config import Config
from .logger_config import get_logger, set_notifier_callback

logger = get_logger(__name__)

async def send_notification_to_server(data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(Config.NOTIFICATION_SERVER_URL, json=data) as resp:
                if resp.status != 200:
                    logger.warning(f"Неудачная отправка уведомления: {resp.status}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления на сервер: {e}")

set_notifier_callback(send_notification_to_server)