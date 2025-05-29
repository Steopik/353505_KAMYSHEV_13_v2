import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EMAIL_SERVICE_URL = os.getenv("EMAIL_SERVICE_URL")
    TELEGRAM_BOT_URL = os.getenv("TELEGRAM_BOT_URL")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    TELEGRAM_CHAT_IDS = [int(x.strip()) for x in os.getenv("TELEGRAM_CHAT_IDS", "").split(",")] if os.getenv("TELEGRAM_CHAT_IDS") else []

    LOG_LEVEL_CONSOLE = os.getenv("LOG_LEVEL_CONSOLE", "INFO")
    LOG_LEVEL_FILE = os.getenv("LOG_LEVEL_FILE", "DEBUG")
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")