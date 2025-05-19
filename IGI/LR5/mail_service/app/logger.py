import logging
from logging.handlers import SMTPHandler
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL, LOG_LEVEL, LOG_FILE_PATH, ADMIN_EMAIL, LOG_EMAIL_LEVEL

logger = logging.getLogger("mail_service")
logger.setLevel(LOG_LEVEL.upper())

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Обработчик записи в файл
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(LOG_LEVEL.upper())
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Обработчик отправки email (только если заданы почтовые настройки и email админа)
if ADMIN_EMAIL and FROM_EMAIL:
    mail_handler = SMTPHandler(
        mailhost=(SMTP_HOST, SMTP_PORT),
        fromaddr=FROM_EMAIL,
        toaddrs=[ADMIN_EMAIL],
        subject='[Mail Service] Log Alert',
        credentials=(SMTP_USER, SMTP_PASSWORD),
        secure=()  # для STARTTLS
    )
    mail_handler.setLevel(LOG_EMAIL_LEVEL.upper())
    mail_handler.setFormatter(formatter)
    logger.addHandler(mail_handler)
else:
    logger.warning("ADMIN_EMAIL or FROM_EMAIL not set — email logging disabled")
