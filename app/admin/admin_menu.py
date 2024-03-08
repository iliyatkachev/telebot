import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types, Router,F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_token
from aiogram.filters import CommandStart, Command
from app.click.keybort import button, menu_button, films_button, serials_button, admin_button, a_opportunities_button
from config import admins



logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()
admin_router = Router()



@admin_router.message(Command("admin_start"))
async def admin_start(message: types.Message):
    user = message.from_user.first_name
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=admin_button)
    await message.answer(text=f"Привет {user}, тебе доступна админ.панель!", reply_markup=reply_markup)

@admin_router.callback_query(F.data == "a_menu")
async def a_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=menu_button)
    await callback.message.answer(text=f'Вы попали в главное меню! Здесь вы можете выбрать жанр фильма,'
                                       f' просмотреть подробную информацию и многое другое🫠', reply_markup=reply_markup)



@admin_router.callback_query(F.data == "a_opportunities")
async def a_opportunities(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=a_opportunities_button)
    await callback.message.answer(text=f'Тут вы можете управлять админ персоналдом!', reply_markup=reply_markup)