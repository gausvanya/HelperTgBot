from slugify import slugify
from app.DataBase.database import Database
from datetime import datetime, timedelta
import re

db = Database()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


async def check_admins(message):
    admins = await db.query("SELECT * FROM chat_admins WHERE user_id=? AND chat_id=?",
                            (message.from_user.id, message.chat.id))

    if not admins:
        await message.reply("🔒 У вас недостаточно прав для выполнения данной команды.")
        return False
    else:
        return True


async def get_user(message):
    UserFilter = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_username = message.reply_to_message.from_user.username
        user_full_name = message.reply_to_message.from_user.full_name
    else:
        user = message.html_text.split(maxsplit=1)[1].split('\n')[0]
        object_remove = ['@', 'https://t.me/', 't.me/', 'tg://openmessage?user_id=', 'tg://user?id=', '<a href="']
        for obj in object_remove:
            user = user.replace(obj, '')
            UserFilter = user.split('">', 1)[0]

        if UserFilter.isdigit():
            result = await db.query('SELECT * FROM users WHERE user_id=?', (UserFilter,))
        else:
            result = await db.query('SELECT * FROM users WHERE user_username=?', (UserFilter,))

        if result:
            user_id, user_username, user_full_name = result[0][0], result[0][1], result[0][2]
        else:
            await message.answer('❌ Данные пользователя не найдены в моей базе данных.')
            return False
    return [user_id, user_username, user_full_name]


async def get_timestamp(message):
    try:
        if message.reply_to_message:
            if len(message.text.split('\n', 1)[0]) == 3:
                time_int = message.text.lower().split()[1]
                time_type = message.text.lower().split()[2]
            else:
                time_int = None
                time_type = message.text.lower().split()[1]
        else:
            if len(message.text.split('\n', 1)[0]) == 4:
                time_int = message.text.lower().split()[1]
                time_type = message.text.lower().split()[2]
            else:
                time_int = None
                time_type = message.text.split()[1].lower()

        if time_type in ['минут', 'минута', 'минуты']:
            dt = datetime.now() + timedelta(minutes=float(time_int))
        elif time_type in ['час', 'часа', 'часов']:
            dt = datetime.now() + timedelta(hours=float(time_int))
        elif time_type in ['день', 'дня', 'дней']:
            dt = datetime.now() + timedelta(days=float(time_int))
        elif time_type in ['неделя', 'недели', 'недель']:
            dt = datetime.now() + timedelta(weeks=float(time_int))
        elif time_type == 'навсегда':
            dt = None
        else:
            await message.answer('Указано неверное время бана.')
            return False

        return [dt, time_int, time_type]
    except Exception:
        return False


async def clear_text(text: str):
    cleared_text = re.sub(r'<[^>]+>', '', text)
    cleared_text = slugify(
        text=cleared_text,
        lowercase=False,
        separator=" ",
        allow_unicode=True
    )
    return cleared_text
