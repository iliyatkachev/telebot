import logging
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.types import InlineKeyboardMarkup
from app.config.config_py import bot_token
from aiogram.filters import Command
from app.click.keybort import (menu_button, admin_button, a_opportunities_button,
                               a_stat_button, a_channels_button)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()
admin_router = Router()
form_channel = Router()



@admin_router.message(Command("admin_start"))
async def admin_start(message: types.Message):
    user = message.from_user.first_name
    reply_markup = types.InlineKeyboardMarkup(inline_keyboard=admin_button)
    await message.answer(text=f"Привет {user}, тебе доступна админ.панель!", reply_markup=reply_markup)

@admin_router.callback_query(F.data == "a_menu")
async def a_menu(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку меню')
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=menu_button)
    await callback.message.answer(text=f'Вы попали в главное меню! Здесь вы можете выбрать жанр фильма,'
                                       f' просмотреть подробную информацию и многое другое🫠',
                                  reply_markup=reply_markup)



@admin_router.callback_query(F.data == "a_opportunities")
async def a_opportunities(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку возможности')
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=a_opportunities_button)
    await callback.message.answer(text=f'Тут вы можете управлять админ персоналдом!', reply_markup=reply_markup)

@admin_router.callback_query(F.data == "a_stat")
async def a_stat(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку статистика')
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=a_stat_button)
    await callback.message.answer(text=f'Отображение пользователей.\n'
                                       f'Удаление пользователей.\n'
                                       f'Блокировка пользователей.', reply_markup=reply_markup)


@admin_router.callback_query(F.data == "channels")
async def channels(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку каналы')
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=a_channels_button)
    await callback.message.answer(text=f'В этом меню, вы можете добавить или удалить '
                                       f'канал, на который пользователь должен '
                                       f'подписаться', reply_markup=reply_markup)



