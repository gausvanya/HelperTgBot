from aiogram.filters import Command
from aiogram import types, Router

from deep_translator import GoogleTranslator
import randfacts

router = Router()


@router.message(Command('факт', prefix='!./', ignore_case=True))
async def send_random_fact(message: types.Message):
    fact = randfacts.get_fact(filter_enabled=True)
    translated_fact = GoogleTranslator(source='auto', target='ru').translate(fact)
    await message.answer(f'🤔 **Интересный факт:**\n{translated_fact}')
