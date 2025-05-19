from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import asyncio
from .email_queue import enqueue_email, process_queue
from .logger import logger


class EmailSchema(BaseModel):
    to: EmailStr
    subject: str
    body: str

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting email queue processing task")
    asyncio.create_task(process_queue())

@app.post("/send-email/")
async def send_email_view(email: EmailSchema):
    await enqueue_email(email.to, email.subject, email.body)
    logger.info(f"Received email request for {email.to}")
    return {"message": "Email added to queue"}
