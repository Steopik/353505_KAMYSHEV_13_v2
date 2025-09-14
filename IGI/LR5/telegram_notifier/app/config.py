import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    NOTIFICATION_SERVER_URL = os.getenv("NOTIFICATION_SERVER_URL")

    LOGS_PATH = os.getenv("LOGS_PATH", "logs/bot.log")
    LOG_LEVEL_CONSOLE = os.getenv("LOG_LEVEL_CONSOLE", "INFO")
    LOG_LEVEL_FILE = os.getenv("LOG_LEVEL_FILE", "DEBUG")
    ERROR_NOTIFICATION_LEVEL = os.getenv("ERROR_NOTIFICATION_LEVEL", "WARNING")

    QUEUE_PROCESS_INTERVAL = int(os.getenv("QUEUE_PROCESS_INTERVAL", "5"))
