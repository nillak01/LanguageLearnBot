from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.keyboard import game_kb, yes_no_kb
from keyboards.inline_keyboards import create_inline_kb
from lexicon.lexicon_ru import LEXICON_RU, BUTTONS
from services.services import get_bot_choice, get_winner

user_router = Router()


# Этот хэндлер срабатывает на команду /start
# @router.message(CommandStart())
# async def process_start_command(message: Message):
#     await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


# # Этот хэндлер будет срабатывать на команду "/start"
# # и отправлять в чат клавиатуру c url-кнопками
# @router.message(CommandStart())
# async def process_start_command(message: Message):
#     await message.answer(
#         text='Это инлайн-кнопки с параметром "url"',
#         reply_markup=keyboard
#     )


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@user_router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard = create_inline_kb(4, **BUTTONS)
    await message.answer(
        text='Это инлайн-клавиатура, сформированная функцией '
             '<code>create_inline_kb</code>',
        reply_markup=keyboard
    )


# Этот хэндлер срабатывает на команду /help
@user_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)


# Этот хэндлер срабатывает на команду /contacts
@user_router.message(Command(commands='contacts'))
async def process_contacts_command(message: Message):
    await message.answer(text=LEXICON_RU['/contacts'])


# Этот хэндлер срабатывает на команду /assistant
@user_router.message(Command(commands='assistant'))
async def process_assistant(message: Message):
    await message.answer(text=LEXICON_RU['/assistant'])
    await message.answer(text=LEXICON_RU['/assistant'])


# Этот хэндлер срабатывает на согласие пользователя играть в игру
@user_router.message(F.text == LEXICON_RU['yes_button'])
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
@user_router.message(F.text == LEXICON_RU['no_button'])
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


# Этот хэндлер срабатывает на любую из игровых кнопок
@user_router.message(F.text.in_([LEXICON_RU['rock'],
                            LEXICON_RU['paper'],
                            LEXICON_RU['scissors']]))
async def process_game_button(message: Message):
    bot_choice = get_bot_choice()
    await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                              f'- {LEXICON_RU[bot_choice]}')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@user_router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
        await callback.message.edit_text(
            text='Была нажата БОЛЬШАЯ КНОПКА 1',
            reply_markup=callback.message.reply_markup
        )
    else:
        await callback.answer(text='БОЛЬШАЯ КНОПКА 1 нажата')
    await callback.answer(text='БОЛЬШАЯ КНОПКА 1',
                          show_alert=True)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@user_router.callback_query(F.data == 'big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 2':
        await callback.message.edit_text(
            text='Была нажата БОЛЬШАЯ КНОПКА 2',
            reply_markup=callback.message.reply_markup
        )
    else:
        await callback.answer(text='БОЛЬШАЯ КНОПКА 2 уже нажата')
    await callback.answer(text='БОЛЬШАЯ КНОПКА 2 уже нажата',
                          show_alert=True)
