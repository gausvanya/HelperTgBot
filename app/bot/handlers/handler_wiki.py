from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

if TYPE_CHECKING:
    from app.lib.wiki_api import WikiAPI, WikiArticleResponse

router = Router()


@router.message(Command('wiki', 'вики', prefix='!./', ignore_case=True))
async def wiki_command(msg: Message, wiki_api: 'WikiAPI'):
    text_split = msg.text.split()

    if len(text_split) == 1:
        return await msg.reply('Укажите запрос.')

    wiki_request_text = ' '.join(text_split[1:])
    wiki_response: 'WikiArticleResponse' = await wiki_api.get_article(wiki_request_text)

    if not wiki_response:
        return await msg.reply('Ошибка получения запроса\nПопробуйте еще раз позже.')

    title = wiki_response.title
    summary = wiki_response.summary
    wiki_url = wiki_response.article_url

    await msg.reply(f"📝 **{title}**\n\n{summary}\n\n↪️ [Узнать подробнее]({wiki_url})")
