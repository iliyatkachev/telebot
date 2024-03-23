import sqlite3

from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup

from app.SQL.sql import add_admin
from app.admin.admin_menu import form_channel
from app.click.keybort import admin_menu_button



admin_router = Router()

class Admin(StatesGroup):
    name_admin = State()
    id_admin = State()
    full_admin = State()


@admin_router.callback_query(F.data == 'add_admin')
async def channel(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Admin.name_admin)
    await callback.answer(text='Вы першли во вкладку возможност!')
    await callback.message.delete()
    await callback.message.answer(text='Введите имя администратора')


@admin_router.message(Admin.name_admin)
async def name_admin(message: Message, state: FSMContext):
    await state.update_data(name_admin=message.text)
    await state.set_state(Admin.id_admin)
    await message.answer(text='Отлично!\nТеперь напишите ID нового администратора')


@admin_router.message(Admin.id_admin)
async def id_admin(message: Message, state: FSMContext):
    await state.update_data(id_admin=message.text)
    await state.set_state(Admin.full_admin)
    await message.answer(text='Хорошо!\n Данные собранны, напиши "ОК" для продолжения')


@admin_router.message(Admin.full_admin)
async def full_admin(message: Message, state: FSMContext):
    if F.text.lower() == "ОК":
        data = await state.get_data()
        name = data.get('name_admin', '')
        id_admin = data.get('id_admin', '')
        await add_admin(name=name, id_admin=id_admin)
        reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
        await message.answer(text="Админ успешно добавлен!", reply_markup=reply_markup)


@admin_router.callback_query(F.data == 'delete_admin')
async def delete_admin(callback: types.CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM admin WHERE id_admin = ?", (user_id,))
    connect.commit()
    cursor.close()
    connect.close()

    await state.clear()
    await callback.answer('Админ удалён!')


@admin_router.callback_query(F.data == 'list_admin')
async def display_all_admins(callback: types.CallbackQuery):
    all_admins = fetch_all_admins()
    if all_admins:
        response_message = "Список администраторов:\n\n" + "\n".join(
            [f"ID: {admin[0]}, Имя: {admin[1]}" for admin in all_admins])
    else:
        response_message = "Администраторы отсутствуют."
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_menu_button)
    await callback.message.answer((response_message), reply_markup=reply_markup)


def fetch_all_admins():
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("SELECT id_admin, name FROM admin")
    all_admins = cursor.fetchall()

    cursor.close()
    connect.close()

    return all_admins