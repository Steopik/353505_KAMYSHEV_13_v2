import asyncio
from .email_utils import send_email
from .logger import logger


email_queue = asyncio.Queue()

async def enqueue_email(to_email: str, subject: str, body: str):
    await email_queue.put((to_email, subject, body))
    logger.info(f"Email enqueued for {to_email}")

async def process_queue():
    logger.info("Email queue processor started")
    while True:
        to_email, subject, body = await email_queue.get()
        logger.info(f"Processing email to {to_email}")
        try:
            await send_email(to_email, subject, body)
            logger.info(f"Email successfully sent to {to_email}")
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
        finally:
            email_queue.task_done()
