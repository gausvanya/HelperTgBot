import typing

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.DataBase.database import Database
from app.bot import handlers
from app.lib.wiki_api import WikiAPI

if typing.TYPE_CHECKING:
    from app.config import Config


async def start_bot(config: 'Config') -> None:
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN,
            link_preview_is_disabled=True
        )
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp['wiki_api'] = WikiAPI()
    await Database().connect()
    dp.include_router(handlers.root_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
