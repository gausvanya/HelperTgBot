from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram import types, Router, F

router = Router()


@router.message(CommandStart(), F.chat.type == 'private')
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    user_username = message.from_user.username

    user_mention = (f'[{user_full_name}](https://t.me/{user_username})' if user_username
                    else f'[{user_full_name}](tg://user?id={user_id})')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Добавить бота',
                                  url='https://t.me/SupHlpBot?startgroup=Support&admin=change_info+'
                                      'restrict_members+delete_messages+pin_messages+invite_users')
             ]
        ]
    )
    await message.reply(f"👋 Приветствую, {user_mention}!\nЯ создан, чтобы поддерживать порядок и гармонию.\n"
                        f"⚖️ Мы хотим чтобы наш бот был для вас полезен, так что идеи для развития вы можете "
                        f"предложить в [чате идей](https://t.me/sup)\n"
                        f"🛠 Команды для управления ботом находятся в разработке.\n"
                        f"Следите за обновлениями в [нашем канале](https://t.me/chann_support)! 😉",
                        reply_markup=keyboard)

    keyboard2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Поддержать нас',
                                  url='https://www.donationalerts.com/r/support_helper_bot')]
        ]
    )

    await message.reply(f"Так вы можете нас поддержать донатом для более быстрого сервера саппорта.\n"
                        f"Так же предложите что можно за донат получить в чате для идей.", reply_markup=keyboard2)
