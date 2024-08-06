from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.DataBase.database import Database
from app.utils import check_admins

db = Database()
router = Router()


@router.message(Command('правила', prefix='+', ignore_case=True), F.chat.type != 'private')
async def add_rules(message: Message):
    chat_id = message.chat.id

    if not check_admins(message):
        return

    try:
        rules_text = message.md_text.split('\n', 1)[1]
    except IndexError:
        return await message.reply('❗️ Используйте команду правильно:\n`+правила\nТекст с новой строки.`')

    rules_db = await db.query('SELECT * FROM chat_rules WHERE chat_id=?', (chat_id,))
    if rules_db:
        await db.query('UPDATE chat_rules SET rules_text=? WHERE chat_id=?', (rules_text, chat_id))
    else:
        await db.query('INSERT INTO chat_rules VALUES(?, ?)', (chat_id, rules_text))

    await message.reply('✅ Правила чата обновлены.')


@router.message(Command('правила', prefix='-', ignore_case=True), F.chat.type != 'private')
async def remove_rules(message: Message):
    chat_id = message.chat.id

    if not check_admins(message):
        return

    rules_db = await db.query('SELECT * FROM chat_rules WHERE chat_id=?', (chat_id,))
    if rules_db:
        await db.query('DELETE FROM chat_rules WHERE chat_id=?', (chat_id,))

    await message.reply('✅ Правила чата удалены.')


@router.message(Command('правила', prefix='!/.', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split('\n', 1)[0] == 'правила', F.chat.type != 'private')
async def get_rules(message: Message):
    rules_db = await db.query('SELECT * FROM chat_rules WHERE chat_id=?', (message.chat.id,))
    if not rules_db:
        return await message.reply('❎ Правила чата не установлены.')

    await message.reply(f'📝 **Правила чата:**\n{rules_db[0][1]}')
