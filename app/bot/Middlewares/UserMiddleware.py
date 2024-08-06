from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, ChatMemberOwner

from app.utils import clear_text
from typing import Callable, Awaitable, Any, Dict
from app.DataBase.database import Database

db = Database()


class Middleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        get_user = event.from_user
        user_first_name = get_user.first_name
        user_last_name = get_user.last_name
        user_username = get_user.username
        user_id = get_user.id

        user_first_name = await clear_text(user_first_name) if user_first_name is not None else ''
        user_last_name = await clear_text(user_last_name) if user_last_name is not None else ''
        user_model = event.from_user.model_copy(update={'first_name': user_first_name, 'last_name': user_last_name})
        new_event = event.model_copy(update={'from_user': user_model})

        user = await db.query('SELECT * FROM users WHERE user_id=?', (user_id,))
        if user:
            if (user[0][1] != user_username) or (user[0][2] != f'{user_first_name} {user_last_name}'):
                await db.query('UPDATE users SET user_full_name=?, user_username=? WHERE user_id=?',
                               (f'{user_first_name} {user_last_name}', user_username, user_id,))
        else:
            await db.query('INSERT INTO users VALUES(?, ?, ?)',
                           (user_id, user_username, f'{user_first_name} {user_last_name}'))

        # Продолжаем обработку следующих обработчиков.
        return await handler(new_event, data)
