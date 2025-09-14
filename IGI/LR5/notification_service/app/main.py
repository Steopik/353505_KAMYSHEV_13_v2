# app/main.py
from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .notification_router import route_email, route_telegram
from .logger_config import get_logger
from .config import Config

logger = get_logger(__name__)
app = FastAPI()


class NotificationRequest(BaseModel):
    channels: List[str]
    emails: List[EmailStr] = []
    telegram_chats: List[int] = []
    message: str


@app.post("/notify")
async def notify(notification: NotificationRequest):
    logger.info(f"Получено уведомление: {notification.message[:30]}...")

    if "email" in notification.channels and not notification.emails:
        notification.emails = [Config.ADMIN_EMAIL]

    if "telegram" in notification.channels and not notification.telegram_chats:
        notification.telegram_chats = Config.TELEGRAM_CHAT_IDS

    if not notification.telegram_chats and not notification.emails:
        raise HTTPException(status_code=400, detail="Не указаны получатели")

    if "email" in notification.channels:
        await route_email(notification.emails, "Уведомление", notification.message)

    if "telegram" in notification.channels:
        await route_telegram(notification.telegram_chats, notification.message)

    return {"status": "sent"}