from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from AIService.DeepSeekApi import speak
from API.definition import get_word_definition_from_html

other_router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@other_router.message()
async def send_answer(message: Message, get_word_definition_from_html):
    await message.answer(text=get_word_definition_from_html)


# Хэндлер для сообщений, которые не попали в другие хэндлеры
# @other_router.message()
# async def send_answer(message: Message, dpseek_api):
#     await message.answer(message.text)
