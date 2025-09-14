from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .notifications import send_notification_to_server
from .queue_manager import add_to_queue
from .logger_config import get_logger
import asyncio

logger = get_logger(__name__)
app = FastAPI()

class OutgoingMessage(BaseModel):
    message: str
    chats_id: List[int]

@app.post("/send-message/")
async def send_message(data: OutgoingMessage):
    logger.info(f"Получено сообщение для рассылки: {data.message}")
    for chat_id in data.chats_id:
        add_to_queue(chat_id, data.message)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)