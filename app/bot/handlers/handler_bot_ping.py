from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram import Router, F

from datetime import datetime

router = Router()


@router.message(Command('пинг', 'ping', prefix='!./', ignore_case=True))
@router.message(F.text.lower().split('\n', 1)[0].in_(['пинг', 'ping']))
async def get_ping_bot(message: Message):
    start_time = datetime.now()
    ping_msg = await message.reply('❗️ Проверка пинга, сообщение измениться для получения.')
    end_time = datetime.now()
    ping_time = (end_time - start_time).microseconds // 1000

    if ping_time < 50:
        ping_status = "скоростной"
        emoji = "🚀"
    elif 50 <= ping_time < 200:
        ping_status = "быстрый"
        emoji = "🏎"
    elif 200 <= ping_time < 500:
        ping_status = "медленный"
        emoji = "🏃‍♂‍➡️"
    else:
        ping_status = "ужасный"
        emoji = "🚶‍♂‍➡️"

    await ping_msg.edit_text(f'🏓 Пинг **{ping_status}**\n{emoji}Скорость: **{ping_time} мс.**')

