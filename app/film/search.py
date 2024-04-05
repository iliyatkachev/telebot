import aiohttp
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from app.comands.commands import menu

film_command = Router()


class Pages(StatesGroup):
    page = State()


@film_command.callback_query(F.data == "Compilation")
async def compilation(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    page = data.get('page', 1)

    url = f"https://api.kinopoisk.dev/v1.4/movie?page={page}&limit=1&lists=top250"
    headers = {
        "accept": "application/json",
        "X-API-Key": "VBZ63SW-PFHMYEM-M3384F6-X6BXVSY"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    await callback.message.delete()
                    data = await response.json(content_type=None)
                    films = data.get('docs', [])

                    messages = []
                    for index, film in enumerate(films, start=1 + (page - 1) * 1):
                        name = film.get('name', 'Название не указано')
                        shortDescription = film.get('shortDescription', 'Описание отсутствует')
                        year = film.get('year', 'Дата отсутствует')
                        poster_url = film.get('poster', {}).get('url')
                        message = (f"{index}. <b>Название фильма:</b> <b>{name}</b>, <b>{year}</b>\n<b>Описание:</b> "
                                   f"<i>{shortDescription}\n</i>")
                        messages.append(message)

                        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [
                                types.InlineKeyboardButton(text="Смотреть фильм",
                                                           switch_inline_query_current_chat=f"{name}")
                            ],
                            [
                                types.InlineKeyboardButton(text="◀️", callback_data="back"),
                                types.InlineKeyboardButton(text='▶️', callback_data="next")
                            ],
                            [
                                types.InlineKeyboardButton(text="Меню📖", callback_data="menu_clear")
                            ]
                        ])

                        try:
                            if poster_url:
                                await callback.message.answer_photo(photo=poster_url, caption='\n\n'.join(messages),
                                                                    reply_markup=keyboard, parse_mode='HTML')
                                break
                        except Exception as photo_error:
                            await callback.message.answer('\n\n'.join(messages), reply_markup=keyboard,
                                                          parse_mode='HTML')

                    if not messages:
                        await callback.message.answer("Фильмы не найдены.")
                    elif not poster_url:
                        await callback.message.answer('\n\n'.join(messages), reply_markup=keyboard, parse_mode='HTML')
                else:
                    await callback.message.answer("Операция не возможна")
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")


@film_command.callback_query(F.data == "next")
async def check(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get('page', 1)

    new_page = current_page + 1

    await state.update_data(page=new_page)

    await compilation(callback, state)


@film_command.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_page = data.get('page', -1)

    new_page = current_page - 1

    await state.update_data(page=new_page)

    await compilation(callback, state)


@film_command.callback_query(F.data == "menu_clear")
async def clear(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await menu(callback)