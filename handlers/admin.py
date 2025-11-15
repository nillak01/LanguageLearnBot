from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_RU
from AIService.DeepSeekApi import speak

admin_router = Router()


# Этот хэндлер срабатывает на команду /assistant
@admin_router.message(Command(commands='assistant'))
async def process_assistant(message: Message):
    await message.answer(text=LEXICON_RU['/assistant'])


# Этот хэндлер срабатывает на команду /assistant
@admin_router.message(Command(commands='boss'))
async def test_for_admin(message: Message):
    await message.answer(text='Привет босс')


# Этот хэндлер срабатывает на команду /assistant
@admin_router.message(Command(commands='admin'))
async def test_for_admin_2(message: Message):
    await message.answer(text='Привет admin, это должен видеть только админ')


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@admin_router.message()
async def send_answer(message: Message, dpseek_api):
    await message.answer(text=speak(word=message.text, api_key=dpseek_api))
