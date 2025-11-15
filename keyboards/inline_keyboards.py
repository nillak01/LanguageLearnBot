from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config_data.config import Config, load_config
from lexicon.lexicon_ru import LEXICON


# Создаем config
config: Config = load_config()

# Создаем объекты инлайн-кнопок
group_name = 'aiogram_stepik_course'
url_button_1 = InlineKeyboardButton(
    text='Группа "Телеграм-боты на AIOgram"',
    url=f'https://t.me/resolve?domain={group_name}'
)
user_id = config.tg_bot.admin_ids[0]
url_button_2 = InlineKeyboardButton(
    text='Автор курса на Степике по телеграм-ботам',
    url=f'https://t.me/user?id={user_id}'
)


# Создаем объекты инлайн-кнопок
big_button_1 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed'
)

big_button_2 = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed'
)

# Создаем объект инлайн-клавиатуры
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1],
                     [url_button_2],
                     [big_button_1],
                     [big_button_2]]
)


# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
