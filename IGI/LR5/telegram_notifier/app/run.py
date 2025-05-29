# app/run.py

import asyncio
from .bot import application
from .queue_manager import send_from_queue
import uvicorn
from .main import app


async def run_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    # Инициализируем бота
    await application.initialize()
    await application.start()

    # Запускаем polling (прослушивание входящих сообщений)
    await application.updater.start_polling(drop_pending_updates=True)

    # Запускаем FastAPI и очередь как фоновые задачи
    api_task = asyncio.create_task(run_api())
    queue_task = asyncio.create_task(send_from_queue())

    # Ждём завершения задач
    await asyncio.gather(api_task, queue_task)


if __name__ == "__main__":
    asyncio.run(main())