from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.database import create_table, add_homework, get_all_homework

import asyncio
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent


router = Router()  # router = Dispatcher



# Обработчик inline запросов
@router.inline_query()
async def inline_query_handler(query: InlineQuery):
    results = [
        InlineQueryResultArticle(
            id="1",
            title="физика",
            input_message_content=InputTextMessageContent(
                message_text="/list"
            )
        ),
        InlineQueryResultArticle(
            id="2",
            title="Пример 2",
            input_message_content=InputTextMessageContent(
                message_text="Это пример 2"
            )
        )
    ]
    await query.answer(results=results, cache_time=1)