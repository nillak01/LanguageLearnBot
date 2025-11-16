from dataclasses import dataclass
from typing import List, Optional, Union
from environs import Env
import logging


logging.basicConfig(
    level='INFO'
)

logger = logging.getLogger(__name__)



@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db_url: str
    dpseek_api: str


def load_config(path: Optional[str] = None):
    # Создаем эксемпляр класса Env
    env: Env = Env()

    # Пробуем загрузить данные из .env
    try:
        # Добавляем в переменное окружение данные из .env
        env.read_env(path)

        # Возвращаем созданный эксемпляр класса Config
        return Config(
            tg_bot=TgBot(
                token=env('BOT_TOKEN'),
                admin_ids=list(map(int, (env.list('ADMIN_ID'))))
            ),
            db_url=env('DB_URL'),
            dpseek_api=env('DEEP_SEEK_API')

        )
    except Exception:
        logger.error("Cant read env")
