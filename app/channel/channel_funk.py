from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.SQL.sql import add_admin
from app.SQL.sql import add_channel, delete_all_channels, fetch_urls_and_ids
from app.admin.admin_menu import form_channel
from app.click.keybort import admin_menu_button


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


async def channels_add(callback: types.CallbackQuery):
    public_urls = fetch_urls_and_ids()

    if public_urls:
        keyboard_publics = [
                [InlineKeyboardButton(text="Подпишись👈", url=url)]
                for url in public_urls
            ]
        keyboard_publics.append([InlineKeyboardButton(text="Проверить подписку", callback_data='check_me')])
        buttons = InlineKeyboardMarkup(inline_keyboard=keyboard_publics)
        await callback.message.answer('⚠️ Пожалуйста, подпишитесь на все паблики для использования бота.',
                                      reply_markup=buttons)
        await callback.message.delete()
    else:
        await callback.message.answer("Извините, у вас ещё нет пабликов")



class Admin(StatesGroup):
    name_admin = State()
    id_admin = State()
    full_admin = State()

@form_channel.callback_query(F.data == 'add_admin')
async def channel(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Admin.name_admin)
    await callback.answer(text='Вы першли во вкладку возможност!')
    await callback.message.delete()
    await callback.message.answer(text='Введите имя администратора')

@form_channel.message(Admin.name_admin)
async def name_admin(message: Message, state: FSMContext):
    await state.update_data(name_admin=message.text)
    await state.set_state(Admin.id_admin)
    await message.answer(text='Отлично!\nТеперь напишите ID нового администратора')


@form_channel.message(Admin.id_admin)
async def id_admin(message: Message, state: FSMContext):
    await state.update_data(id_admin=message.text)
    await state.set_state(Admin.full_admin)
    await message.answer(text='Хорошо!\n Данные собранны, напиши "ОК" для продолжения')

@form_channel.message(Admin.full_admin)
async def full_admin(message: Message, state: FSMContext):
    if F.text.lower() == "ОК":
        data = await state.get_data()
        name = data.get('name_admin', '')
        id_admin = data.get('id_admin', '')
        await add_admin(name=name, id_admin=id_admin)
        reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
        await message.answer(text="Админ успешно добавлен!", reply_markup=reply_markup)


@form_channel.callback_query(F.data == 'admin_delete')
async def delete_admin(message: Message):
    await delete_admin(message)
    reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
    await message.answer(text="Все админы были удаленны!", reply_markup=reply_markup)
