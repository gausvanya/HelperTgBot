from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram import Router, F

from app.DataBase.database import Database
from app.utils import check_admins

db = Database()
router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def add_bot(message: ChatMemberUpdated):
    bot_url = ('https://t.me/SupHlpBot?startgroup=Sup&admin=change_info+restrict_members+delete_messages+'
               'pin_messages+invite_users+promote_members+manage_voice_chats+ban_members+view_members')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⭐️ Назначить администратором', url=bot_url)]])

    await message.answer(
        '**👋 Приветствую чат!**\nℹ️Выдать права администратора мне можно по кнопке ниже или по гайду:\n'
        'Переходим в настройки чата -> переходим в раздел «Администраторы» -> нажимаете «Добавить администратора» -> '
        'ищите в участниках бота -> кликаете на него -> выдаёте **ВСЕ** права кроме анонимности.\n\n'
        '📝 [Мой список команд](https://teletype.in/@support_bot/suuportcommands)\n'
        '📣 [Официальный канал](https://t.me/chann_support)', reply_markup=keyboard)


@router.chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def leave_user(message: ChatMemberUpdated):
    user_id = message.old_chat_member.user.id
    user_full_name = message.old_chat_member.user.full_name
    user_username = message.old_chat_member.user.username
    admin_id = message.from_user.id
    admin_full_name = message.from_user.full_name
    admin_username = message.from_user.username

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    admin_mention = (f'[{admin_full_name}](https://t.me/{admin_username})' if admin_username
                     else f'[{admin_full_name}](tg://user?id={admin_id})')

    if admin_id:
        await message.answer(f'🛑 Пользователь {user_mention} исключен администратором {admin_mention}')
    else:
        await message.answer(f'👋 Пользователь {user_mention} покинул чат.')


@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def join_user(message: ChatMemberUpdated):
    user_id = message.old_chat_member.user.id
    user_full_name = message.old_chat_member.user.full_name
    user_username = message.old_chat_member.user.username
    admin_id = message.from_user.id
    admin_full_name = message.from_user.full_name
    admin_username = message.from_user.username
    chat_id = message.chat.id

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    admin_mention = (f'[{admin_full_name}](https://t.me/{admin_username})' if admin_username
                     else f'[{admin_full_name}](tg://user?id={admin_id})')

    if admin_id:
        await message.answer(f'👋 {user_mention} присоединился к чату.\nДобавил: {admin_mention}')
    else:
        await message.answer(f'👋 {user_mention} присоединился к чату.')

    antispam_db = await db.query('SELECT * FROM antispam WHERE user_id=? AND activity=?', (user_id, 'да'))
    spam_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')
    if antispam_db:
        get_chat_member = await message.bot.get_chat_member(chat_id, admin_id)

        if get_chat_member.status in ['creator', 'administrator']:
            await message.answer(f'📛 Внимание!\nВы пригласили {spam_mention} в чат.\n'
                                 f'Он находится в базе АнтиСпам\n'
                                 f'💬 Причина: {antispam_db[0][4]}')
        else:
            await message.bot.ban_chat_member(chat_id, user_id)
            return await message.answer(f'📛 Внимание!\nПользователь {spam_mention} '
                                        f'находится в базе АнтиСпам\n'
                                        f'💬 Причина: {antispam_db[0][4]}\nИсключаю...')

    result = await db.query('SELECT * FROM chat_welcome WHERE chat_id=?', (chat_id,))
    if not result:
        return

    welcome_text = result[0][2].replace('{имя}', user_mention)
    if result[0][1]:
        await message.reply_photo(photo=result[0][1], caption=welcome_text)
    else:
        await message.reply(welcome_text)


@router.message(Command('приветствие', prefix='+', ignore_case=True), F.chat.type != 'private')
async def add_welcome(message: Message):
    chat_id = message.chat.id

    if not check_admins(message):
        return

    try:
        welcome_text = message.md_text.split('\n', 1)[1]
    except IndexError:
        return await message.reply('❗️ Используйте команду правильно:\n`+приветствие\nТекст с новой строки.`')

    photo_id = message.photo[-1].file_id if message.photo else None

    welcome_db = await db.query('SELECT * FROM welcome_chat WHERE chat_id=?', (chat_id,))
    if welcome_db:
        await db.query('UPDATE chat_welcome SET welcome_text=?, photo_id=? WHERE chat_id=?',
                       (welcome_text, photo_id, chat_id))
    else:
        await db.query('INSERT INTO chat_welcome VALUES(?, ?, ?)', (chat_id, photo_id, welcome_text))

    await message.reply('✅ Приветствие новых пользователей чата установлено.')


@router.message(Command('приветствие', prefix='-', ignore_case=True), F.chat.type != 'private')
async def remove_welcome(message: Message):
    chat_id = message.chat.id

    if not await check_admins(message):
        return

    welcome = await db.query('SELECT * FROM chat_welcome WHERE chat_id=?', (chat_id,))
    if welcome:
        await db.query('DELETE FROM chat_welcome WHERE chat_id=?', (chat_id,))

    await message.reply('✅ Приветствие новых пользователей чата удалено.')


@router.message(Command('приветствие', prefix='!/.', ignore_case=True), F.chat.type != 'private')
@router.message(F.text.lower().split('\n', 1)[0] == 'приветствие')
async def get_welcome(message: Message):
    chat_id = message.chat.id

    if not await check_admins(message):
        return

    welcome_db = await db.query('SELECT * FROM chat_welcome WHERE chat_id=?', (chat_id,))
    if not welcome_db:
        return await message.reply('Приветствие новых пользователей пока не установлено.')

    welcome_text, photo_id = welcome_db[0][2], welcome_db[0][1]
    if photo_id:
        await message.reply_photo(photo_id, welcome_text)
    else:
        await message.reply(welcome_text)
