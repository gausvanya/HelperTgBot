from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION
from aiogram.types import ChatMemberUpdated

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def add_bot(event: ChatMemberUpdated):
    chat_id = event.chat.id
    get_admins = await event.bot.get_chat_administrators(chat_id)

    for admin in get_admins:
        print(admin)
        if admin.status == 'creator':
            owner_id = admin.user.id
            # Запись в бд

















import asyncio
from app import config, logging_config, bot


async def main():
    cfg = config.get_config()

    logging_config.setup(
        log_format=cfg.logging.log_format,
        level=cfg.logging.log_level,
    )

    await bot.start_bot(cfg)


if __name__ == '__main__':
    asyncio.run(main())
