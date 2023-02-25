from typing import Dict, Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import asyncpg
from booking_core.other.db_request import Request




class DbSession(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool):
        super().__init__()
        self.connector = connector


    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]
                       ) -> Any:

        data['request'] = Request(self.connector)
        return await handler(event, data)

        # async with self.connector.acquire() as connect:
        #     data['request'] = Request(connect)
        #     return await handler(event, data)


