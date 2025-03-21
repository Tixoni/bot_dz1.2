import asyncio
import sqlite3
import logging #для отображения информации с ботом через терминал (только при дебадинге )
from aiogram import Bot, Dispatcher, types

from config import TOKEN
from app.handlers import router

#1.1 - изменение внешнего вида команды /list для лучшего восприятия,добавление inline клавиатуры для более быстрого и удобного добвления дз



bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt: #чтобы отключать бота комбинацией cntr + c 
        print("Exit")
