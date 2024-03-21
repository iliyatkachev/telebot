import asyncio
import logging
import sqlite3

from aiogram.enums import ParseMode
from app.admin import mailing_clik
from app.admin import admin_menu
from aiogram import Bot, Dispatcher, types, Router
from config import bot_token
from aiogram.filters import Command
from app.comands import commands
from app.start import start_button
from app.SQL import sql

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_routers(admin_menu.admin_router, commands.commands_router,start_button.start_router, sql.sql_router,
                   mailing_clik.mailing_router, mailing_clik.form_router, admin_menu.form_channel, )
router = Router

#command opportunities
@dp.message(Command("opportunities", prefix="/!"))
async def opportunities(message: types.Message):
    await message.answer(text="В этом боте вы сможете найти фильмы и сериалы которые так давно хотели посмотреть!")

#start project
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())

