import aiohttp
from aiogram import F, types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

random_command = Router()


@random_command.callback_query(F.data == "random")
async def random_film(callback: types.CallbackQuery):
    url = "https://api.kinopoisk.dev/v1.4/movie/random?lists=top250"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "R3ZHKRH-HXV4BW8-JSDD6W9-CZX102N"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    await callback.message.delete()
                    films = await response.json(content_type=None)
                    messages = []

                    name = films.get('name', 'Название не указано')
                    shortDescription = films.get('shortDescription', 'Описание отсутствует')
                    year = films.get('year', 'Дата отсутствует')
                    poster_url = films.get('poster', {}).get('url')
                    message = (f"<b>Название фильма:</b> <i>{name}</i>, <i>{year}</i>\n<b>Описание:</b> "
                               f"<b>{shortDescription}\n</b>")
                    messages.append(message)

                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [
                            types.InlineKeyboardButton(text="Смотреть фильм",
                                                       switch_inline_query_current_chat=f"{name}")
                        ],
                        [
                            InlineKeyboardButton(text="меню↩️", callback_data="menu_clear"),
                            types.InlineKeyboardButton(text="Ещё фильм🔄", callback_data="random")
                        ]

                    ])

                    try:
                        if poster_url:
                            await callback.message.answer_photo(photo=poster_url, caption='\n\n'.join(messages),
                                                                reply_markup=keyboard, parse_mode='HTML')

                    except Exception as photo_error:
                        await callback.message.answer('\n\n'.join(messages),
                                                      reply_markup=keyboard,
                                                      parse_mode='HTML')

                if not messages:
                    await callback.message.answer("Фильмы не найдены.")
                elif not poster_url:
                    await callback.message.answer('\n\n'.join(messages), reply_markup=keyboard,
                                                  parse_mode='HTML')

    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")
