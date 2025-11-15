import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers.other import other_router
from handlers.admin import admin_router
from handlers.user import user_router
from keyboards.set_menu import set_main_menu
from middlewares.outer import (
    AdminCheckMiddleware,
    FirstOuterMiddleware
)
from middlewares.inner import (
    FirstInnerMiddleware
)


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.workflow_data.update({'db_url': config.db_url, 'dpseek_api': config.dpseek_api, 'admins': config.tg_bot.admin_ids})

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(other_router)

    # Здесь будем регистрировать миддлвари
    user_router.message.outer_middleware(FirstOuterMiddleware())
    admin_router.message.outer_middleware(AdminCheckMiddleware())

    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, _admins_list=config.tg_bot.admin_ids)


asyncio.run(main())
