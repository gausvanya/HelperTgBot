from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from app.DataBase.database import Database
from app.utils import get_user

router = Router()
db = Database()


@router.message(Command('агент', prefix='+', ignore_case=True))
async def add_agent(message: Message):
    admin_id = message.from_user.id
    if admin_id not in [6571256315, 5858412531]:
        return

    user = await get_user(message)
    user_id, user_username, user_full_name = user[0], user[1], user[2]

    result = await db.query('SELECT * FROM agents WHERE user_id=?', (user_id,))

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    if result:
        return await message.reply(f"❌ Пользователь {user_mention} уже агент.")

    await db.query('INSERT INTO agents VALUES(?, ?)', (user_id, admin_id))
    await message.reply(f'✅ Пользователь {user_mention} назначен агентом.')


@router.message(Command('агент', prefix='-', ignore_case=True))
async def remove_agent(message: Message):
    admin_id = message.from_user.id
    if admin_id not in [6571256315, 5858412531]:
        return

    user = await get_user(message)
    user_id, user_username, user_full_name = user[0], user[1], user[2]

    result = await db.query('SELECT * FROM agents WHERE user_id=?', (user_id,))

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')
    if not result:
        return await message.reply(f"❌ пользователь {user_mention} не агент.")

    await db.query('DELETE FROM agents WHERE user_id=?', (user_id,))
    await message.reply(f"✅ Агент {user_mention} разжалован.")


@router.message(Command('агенты', prefix='!/.', ignore_case=True))
async def agent_list(message: Message):
    admin_id = message.from_user.id
    if admin_id not in [6571256315, 5858412531]:
        return

    result = await db.query('SELECT * FROM agents')
    text_agents = '<b>📜 Список агентов бота:</b>\n'
    if not result:
        return await message.reply(f"{text_agents + 'Пуст.'}")
    for row in result:
        user_id = row[0]
        admin_id = row[1]
        user = await db.query('SELECT * FROM users WHERE user_id=?', (user_id,))
        user_id, user_username, user_full_name = user[0], user[1], user[2]
        admin = await db.query('SELECT * FROM users WHERE user_id=?', (admin_id,))
        admin_id, admin_username, admin_full_name = admin[0], admin_id[1], admin_id[2]

        user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                        else f'[{user_full_name}](tg://user?id={user_id})')

        admin_mention = (f'[{admin_full_name}](https://t.me/{admin_username})' if admin_username
                         else f'[{admin_full_name}](tg://user?id={admin_id})')

        text_agents += f"🔸 Агент {user_mention}, назначил: {admin_mention}\n"
    await message.reply(text_agents)
