from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from app.click.keybort import a_mailing_button
from app.SQL.sql import ferch_all_users

form_router = Router()
mailing_router = Router()
command = Command
@mailing_router.callback_query(F.data == "mailing")
async def mailing(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладкку рассылка')
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=a_mailing_button)
    await callback.message.answer(text="Вы попали в меню рассылок!\nВам доступна возможность добавить запись."
                                  , reply_markup=reply_markup)


class Form(StatesGroup):
    photo = State()
    caption = State()
    text_clik = State()
    url_clik = State()
    full_post = State()
    send_post = State()


@form_router.callback_query(F.data == "a_m_add")
async def form_com(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.photo)
    await callback.answer('Вы перешли во вкладку добавте фото')
    await callback.message.delete()
    await callback.message.answer(text="Добавте фото!")

@form_router.message(Form.photo)
async def photo_com(message: Message, state: FSMContext):
    media_file_id = message.photo[-1].file_id
    await state.update_data(photo=media_file_id)
    await state.set_state(Form.caption)
    await message.answer(text="Хорошо!\nТеперь напиши ваш текст:")

@form_router.message(Form.caption)
async def text_com(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    await state.set_state(Form.text_clik)
    await message.answer(text="Отлично!\nТеперь добавте название кнопки:")

@form_router.message(Form.text_clik)
async def name_com(message: Message, state: FSMContext):
    await state.update_data(text_clik=message.text)
    await state.set_state(Form.url_clik)
    await message.answer(text="Идем дальше!\nТеперь нужно добавить url.")

@form_router.message(Form.url_clik)
async def url_com(message: Message, state: FSMContext):
    await state.update_data(url_clik=message.text)
    await state.set_state(Form.full_post)
    await message.answer(text=f"Готово\nТеперь введите ОК для продолжения.")

@form_router.message(Form.full_post)
async def full_com(message: Message, state: FSMContext):
    if F.text.lower() == 'ОК':
        data = await state.get_data()
        photo = data.get("photo", "")
        caption = data.get("caption", "")
        text_clik = data.get("text_clik", "")
        url_clik = data.get("url_clik", "")

        button = [
            [
                InlineKeyboardButton(text=text_clik, url=url_clik)
            ]
        ]
        post_data = {
            "photo": photo,
            "caption": caption,
            "button": button
        }

        await state.update_data(full_post=post_data)
        reply = InlineKeyboardMarkup(inline_keyboard=button)
        await message.answer_photo(photo=photo, caption=caption, reply_markup=reply)
        done_button = [
            [
                InlineKeyboardButton(text="Отправить!", callback_data="add_post_button")
            ],
            [
                InlineKeyboardButton(text="Удалить", callback_data="delete_post_button")
            ]
        ]

        done_b = InlineKeyboardMarkup(inline_keyboard=done_button)
        await message.answer(text="Как поступим?", reply_markup=done_b)
        await state.set_state(Form.full_post)

@form_router.callback_query(F.data == "add_post_button")
async def full_com(callback: types.CallbackQuery, state: FSMContext):
    if F.data == "add_post_button":
        data = await state.get_data()
        photo = data.get("photo", "")
        caption = data.get("caption", "")
        text_clik = data.get("text_clik", "")
        url_clik = data.get("url_clik", "")

        button = [
            [
                InlineKeyboardButton(text=text_clik, url=url_clik)
            ]
        ]
        reply = InlineKeyboardMarkup(inline_keyboard=button)

        post_data = {
            "photo": photo,
            "caption": caption,
            "button": button
        }
        await state.update_data(full_post=post_data)

        user_ids = ferch_all_users()
        for user_id in user_ids:
            try:
                await callback.bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=reply)
            except Exception as e:
                print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")



@form_router.callback_query(F.data == "delete_post_button")
async def delete_post(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.get_state()
    await state.clear()
    await callback.answer("Пост удалён!")
