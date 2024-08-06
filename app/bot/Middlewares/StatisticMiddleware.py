from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, ChatMemberOwner

from typing import Callable, Awaitable, Any, Dict
from datetime import datetime
from app.DataBase.database import Database

db = Database()


class Middleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        chat_id = event.chat.id
        today = datetime.now().strftime('%d.%m.%Y')

        statistic = await db.query('SELECT * FROM chat_statistic WHERE user_id=? AND chat_id=? AND date=?',
                                   (user_id, chat_id, today))

        if statistic:
            await db.query('UPDATE chat_statistic SET coint_msg=? WHERE chat_id=? AND user_id=? AND date=?',
                           (statistic[0][2] + 1, chat_id, user_id, today))
        else:
            await db.query('INSERT INTO chat_statistic VALUES(?, ?, ?, ?)', (chat_id, user_id, 1, today))

        return await handler(event, data)
