
import logging
import os
import asyncio
from .config import Config
_notifier_callback = None

def set_notifier_callback(callback):
    global _notifier_callback
    _notifier_callback = callback


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s"
    )

    # Консольный логгер
    console_level = getattr(logging, Config.LOG_LEVEL_CONSOLE)
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Файловый логгер
    file_level = getattr(logging, Config.LOG_LEVEL_FILE)
    
    log_dir = os.path.dirname(Config.LOGS_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    fh = logging.FileHandler(Config.LOGS_PATH, encoding='utf-8')  # ✅ UTF-8 для русских символов
    fh.setLevel(file_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger