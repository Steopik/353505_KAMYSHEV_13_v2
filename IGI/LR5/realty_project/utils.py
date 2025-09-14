import os
from pathlib import Path

def ensure_log_file_path():
    log_path = os.getenv('LOG_FILE_PATH', 'logs/app.log')
    full_log_path = Path(log_path).resolve()
    
    # Получаем директорию файла лога
    log_dir = full_log_path.parent
    
    # Создаём путь, если его нет
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Создана директория для логов: {log_dir}")
    
    return str(full_log_path)