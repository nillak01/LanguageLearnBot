from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
import logging

# Инициализируем логгер
logger = logging.getLogger(__name__)

class AdminCheckMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        logger.info(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__

        )

        user: User = data.get('event_from_user')
        idmins_list = data.get('_admins_list')

        logger.info(
            'Вот id',
            user.id

        )

        if user is not None:
            if user.id in idmins_list:
                return await handler(event, data)

        logger.info(
            'Вышли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )
        return None


class FirstOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__,
            data.__class__.__name__
        )

        result = await handler(event, data)

        logger.debug('Выходим из миддлвари  %s', __class__.__name__)

        return result
