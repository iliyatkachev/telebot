import logging
from aiogram import Bot, Dispatcher, types, Router,F
from aiogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton, CallbackQuery
from config import bot_token
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from app.SQL.sql import add_channel, delete_all_channels
from app.click.keybort import (menu_button, admin_button, a_opportunities_button,
                               a_stat_button, a_channels_button,admin_menu_button)

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
                                       f' просмотреть подробную информацию и многое другое🫠', reply_markup=reply_markup)



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

class Form(StatesGroup):
    name = State()
    url = State()
    id_channel = State()
    full_channel = State()

@form_channel.callback_query(F.data == "a_c_add")
async def channels(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.name)
    await callback.answer('Вы перешли во вкладку каналы')
    await callback.message.delete()
    await callback.message.answer(text='Добавить название канала')


@form_channel.message(Form.name)
async def name_com(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.url)
    await message.answer(text='Отлично!\nТеперь напишите URL нового канала')

@form_channel.message(Form.url)
async def url_com(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(Form.id_channel)
    await message.answer(text='Хорошо!\nТеперь введите ID канала')


@form_channel.message(Form.id_channel)
async def id_com(message: Message, state: FSMContext):
    await state.update_data(id_channel=message.text)
    await state.set_state(Form.full_channel)
    await message.answer(text='Готово!\nТеперь вам нужно написать ОК для продолжения добавления')

@form_channel.message(Form.full_channel)
async def full_channel(message: Message, state: FSMContext):
    if F.text.lower() == "ОК":
        data = await state.get_data()
        name = data.get('name', '')
        url = data.get('url', '')
        id_channel = data.get('id_channel', '')
        await add_channel(name=name, url=url, id_channel=id_channel)
        reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
        await message.answer(text="Канал успешно добавлен!", reply_markup=reply_markup)



@form_channel.callback_query(F.data == 'a_c_delete')
async def delete_channel(message: Message):
    await delete_all_channels(message)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
    await message.answer(text="Все каналы были удаленны!", reply_markup=reply_markup)

