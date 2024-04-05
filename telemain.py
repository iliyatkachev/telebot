import asyncio
import logging
from aiogram.enums import ParseMode
from app.admin import mailing_clik
from app.admin import admin_menu
from app.admins import managing_administrators
from aiogram import Bot, Dispatcher, Router
from app.config.config_py import bot_token
from app.comands import commands
from app.start import start_button
from app.SQL import sql
from app.film import search
from app.film import get
from app.film import random


bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_routers(admin_menu.admin_router, commands.commands_router,
                   start_button.start_router, sql.sql_router,
                   mailing_clik.mailing_router,
                   mailing_clik.form_router, admin_menu.form_channel,
                   managing_administrators.admin_router, search.film_command,
                   get.get_command, random.random_command)
router = Router


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

