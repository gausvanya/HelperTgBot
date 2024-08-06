from aiogram import Router

from app.bot.Middlewares import UserMiddleware

from . import (handler_chat_admins, handler_agents, handler_fact, handler_user_id, handler_notes, handler_bot_ping,
               handler_rules, handler_start, handler_welcome, handler_wiki)


root_router = Router(name='root router')
root_router.message.outer_middleware(UserMiddleware.Middleware())
root_router.include_routers(handler_chat_admins.router, handler_agents.router, handler_fact.router,
                            handler_user_id.router, handler_notes.router, handler_rules.router,
                            handler_start.router, handler_welcome.router, handler_wiki.router)
