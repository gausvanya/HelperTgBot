from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command

from app.DataBase.database import Database
from app.utils import check_admins

db = Database()
router = Router()


@router.message(Command('заметка', prefix='+', ignore_case=True), F.chat.type != 'private')
async def add_note(message: Message):
    chat_id = message.chat.id

    if not check_admins(message):
        return

    try:
        note_name = message.text.lower().split('\n', 1)[0].split(maxsplit=1)[1]
        note_text = message.md_text.split('\n', 1)[1]
    except IndexError:
        return await message.reply('❗️ Используйте команду правильно:\n`+заметка [название]\nТекст с новой строки.`')

    notes_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=? AND note_name', (chat_id, note_name))

    if notes_db:
        return await message.reply('❎ Заметка с таким названием уже существует.')

    max_note_number = await db.query('SELECT MAX(number_note) FROM chat_notes WHERE chat_id=?', (chat_id,))
    note_number = max_note_number[0][0] or 0

    await db.query('INSERT INTO chat_notes VALUES(?, ?, ?, ?)', (chat_id, note_name, note_text, note_number + 1))
    await message.reply(f'✅ Заметка **{note_name} (#{note_number + 1})** создана')


@router.message(Command('заметка', prefix='-', ignore_case=True), F.chat.type != 'private')
async def remove_note(message: Message):
    chat_id = message.chat.id

    if not check_admins(message):
        return

    try:
        note_name = message.text.lower().split('\n', 1)[0].split(maxsplit=1)[1]
    except IndexError:
        return await message.reply('❗️ Используйте команду правильно:\n`-заметка [название | номер]`')

    if note_name.isdigit():
        note_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=? AND number_note=?', (chat_id, int(note_name)))
    else:
        note_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=? AND note_name=?', (chat_id, note_name))

    if not note_db:
        return await message.reply(f'❎ Заметка **{note_name}** не найдена.')

    await db.query('DELETE FROM chat_notes WHERE chat_id=? AND note_name=?', (chat_id, note_name))
    await message.reply(f'✅ Заметка **{note_db[0][1]}** удалена.')


@router.message(Command('заметки', prefix='!/.', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split('\n', 1)[0] == 'заметки')
async def get_note_list(message: Message):
    note_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=?', (message.chat.id,))
    if not note_db:
        return await message.reply('❌ Заметок пока нету.\n\n💬 Для создания заметки пропишите:\n'
                                   '`+заметка [название]\nтекст с новой строки`')

    note_text = '📝 **Заметки чата:**\n'
    for note in note_db:
        note_text += f'#{note[3]}. `{note[1]}`'

    await message.reply(note_text + '\n\n💬 Чтобы открыть заметку пропишите: `!заметка [название | номер]`')


@router.message(Command('заметка', prefix='/.!', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split('\n', 1)[0].split()[0] == 'заметка')
async def get_note(message: Message):
    chat_id = message.chat.id
    try:
        note_name = message.text.lower().split('\n', 1)[0].split(maxsplit=1)[1]
    except IndexError:
        return await message.reply('️ Используйте команду правильно:\n`!заметка [название | номер]`')

    if note_name.isdigit():
        note_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=? AND number_note=?', (chat_id, int(note_name)))
    else:
        note_db = await db.query('SELECT * FROM chat_notes WHERE chat_id=? AND note_name=?', (chat_id, note_name))

    if not note_db:
        return await message.reply(f'❎ Заметка **{note_name}** не найдена.')

    await message.answer(f'📝 Заметка **{note_db[0][1]}**:\n{note_db[0][2]}')
