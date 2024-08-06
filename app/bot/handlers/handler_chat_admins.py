from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message

from app.DataBase.database import Database
from app.utils import get_user, check_admins

router = Router()
db = Database()


@router.message(Command('модер', 'админ', prefix='+', ignore_case=True), F.chat.type != 'private')
@router.message(Command('повысить', prefix='!./', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split()[0] == 'повысить', F.chat.type != 'private')
async def add_moder(message: Message):
    chat_id = message.chat.id

    agents = await db.query('SELECT * FROM agents WHERE user_id=?', (message.from_user.id,))
    if not agents:
        if not await check_admins(message):
            return

    user = await get_user(message)
    user_id, user_username, user_full_name = user[0], user[1], user[2]

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    admins = await db.query('SELECT * FROM chat_admins WHERE chat_id=? AND user_id=?', (chat_id, user_id))
    if admins:
        return await message.answer(f'❎ Пользователь {user_mention} уже является модератором бота.')

    await db.query('INSERT INTO chat_admins VALUES(?, ?)', (chat_id, user_id))
    await message.answer(f'✅ Пользователь {user_mention} назначен модератором бота.')


@router.message(Command('модер', 'админ', prefix='-', ignore_case=True), F.chat.type != 'private')
@router.message(Command('снять', 'разжаловать', prefix='!./', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split()[0] == 'снять', F.chat.type != 'private')
async def remove_moder(message: Message):
    chat_id = message.chat.id

    agents = await db.query('SELECT * FROM agents WHERE user_id=?', (message.from_user.id,))
    if not agents:
        if not await check_admins(message):
            return

    user = await get_user(message)
    user_id, user_username, user_full_name = user[0], user[1], user[2]

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    admins = await db.query('SELECT * FROM chat_admins WHERE user_id=? AND chat_id=?', (user_id, chat_id))
    if not admins:
        return await message.answer(f'❌ Пользователь {user_mention} не является модератором.')

    await db.query('DELETE FROM chat_admins WHERE user_id=? AND chat_id=?', (user_id, chat_id))
    await message.answer(f'✅ Модератор {user_mention} разжалован.')


@router.message(Command('модеры', 'админы', prefix='!/.', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split('\n', 1)[0].in_(['модеры', 'админы', 'кто админ'], F.chat.type != 'private'))
async def chat_moder_list(message: Message):
    admins = await db.query('SELECT * FROM chat_admins WHERE chat_id=?', (message.chat.id,))
    if not admins:
        return await message.answer(f'В чате царит анархия.')

    text = '**Список модераторов бота:**\n'
    for row in admins:
        user_id = row[1]
        users = await db.query('SELECT * FROM chat_admins WHERE chat_id=?', (user_id,))
        user_username, user_full_name = users[0][1], users[0][2]
        user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                        else f'[{user_full_name}](tg://user?id={user_id})')
        text += f"🔸 {user_mention}\n"

    await message.answer(text)
