import os
from dotenv import load_dotenv


load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("EMAIL_HOST_USER")
SMTP_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")
LOG_EMAIL_LEVEL = os.getenv("LOG_EMAIL_LEVEL", "CRITICAL")


ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")