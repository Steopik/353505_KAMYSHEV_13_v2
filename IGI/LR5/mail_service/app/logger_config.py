# app/logger_config.py
import logging
import os
from logging.handlers import SMTPHandler
from .config import Config

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s"
    )

    # Консольный логгер
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, Config.LOG_LEVEL_CONSOLE.upper()))
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Файловый логгер
    log_dir = os.path.dirname(Config.LOG_FILE_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    fh = logging.FileHandler(Config.LOG_FILE_PATH)
    fh.setLevel(getattr(logging, Config.LOG_LEVEL_FILE.upper()))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Логирование ошибок по email
    if Config.ADMIN_EMAIL and Config.SMTP_USER and Config.SMTP_PASSWORD:
        try:
            mail_handler = SMTPHandler(
                mailhost=(Config.SMTP_HOST, Config.SMTP_PORT),
                fromaddr=Config.FROM_EMAIL,
                toaddrs=[Config.ADMIN_EMAIL],
                subject="[EMAIL SERVICE ALERT]",
                credentials=(Config.SMTP_USER, Config.SMTP_PASSWORD),
                secure=()
            )
            mail_handler.setLevel(getattr(logging, Config.LOG_EMAIL_LEVEL.upper()))
            mail_handler.setFormatter(formatter)
            logger.addHandler(mail_handler)
        except Exception as e:
            logger.warning(f"Не удалось настроить email-логирование: {e}")

    return logger