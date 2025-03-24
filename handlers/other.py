from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from AIService.DeepSeekApi import speak

other_router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@other_router.message()
async def send_answer(message: Message, dpseek_api):
    await message.answer(message.text)
