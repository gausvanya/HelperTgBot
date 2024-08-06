from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.DataBase.database import Database
from app.utils import get_user
db = Database()
router = Router()


@router.message(Command('ид', prefix='/.!', ignore_case=True))
async def get_user_id(message: Message):
    if len(message.text.split('\n', 1)[0].split()) == 1 and not message.reply_to_message:
        user_id = message.from_user.id
        user_username = message.from_user.username
        user_full_name = message.from_user.full_name
    else:
        user = await get_user(message)
        user_id, user_username, user_full_name = user[0], user[1], user[2]

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    await message.reply(f'🆔 пользователя {user_mention}: `@{user_id}`')

