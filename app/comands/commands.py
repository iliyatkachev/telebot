from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.SQL.sql import fetch_user_date, ferch_all_users, find_public_ids
from app.click.keybort import menu_button, back_button, admin_button
from app.channel.channel_funk import channels_add
from aiogram.utils.markdown import hlink
from urllib.parse import quote
from uuid import uuid4
from app.click.keybort import again
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State

import aiohttp
import random

commands_router = Router()


#command menu
@commands_router.callback_query(F.data == "menu")
async def menu(callback: types.CallbackQuery):
    public_ids = find_public_ids()

    user_id = callback.from_user.id
    sub = True

    for chat_id in public_ids:
        try:
            status = await callback.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if status.status not in ['creator', 'administrator', 'member']:
                sub = False
                break
        except Exception as e:
            print(f"Ошибка при проверке подписки пользователя {user_id} на паблик {chat_id}: {e}")
            sub = False
            break

    if not sub:
        return await channels_add(callback)
    else:

        await callback.answer('Вы перешли во вкладку меню')
        await callback.message.delete()
        reply_markup = InlineKeyboardMarkup(inline_keyboard=menu_button)
        await callback.message.answer(text=f'Вы попали в главное меню! Здесь вы можете выбрать жанр фильма,'
                                           f' просмотреть подробную информацию и многое другое🫠',
                                      reply_markup=reply_markup)






#command faims
@commands_router.inline_query()
async def inline_films(inline_query: types.InlineQuery):
    base_url = "https://apivb.info/api/videos.json?title={}&token=30c9ab7fcdf48b3b3d2eda889b6637cd"
    search_query = quote(inline_query.query)  # Кодирование запроса пользователя для использования в URL

    url = base_url.format(search_query)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            results = []
            if response.status == 200:
                response = await response.json(content_type=None)
            if isinstance(response, list):
                films = response[:50]
            elif isinstance(response, dict):
                films = response.get('data', [])[:50]
            else:
                films = []

            for film in films:
                title = film.get('title_ru') or film.get('title_en')
                description = f"{film.get('year', 'Год не указан')}"
                trailer_url = film.get('trailer', '').replace('\\/', '/')
                poster_url = film.get('poster', '').replace('\\/', '/')
                quality = film.get('quality', '')
                iframe_url = film.get('iframe_url', '').replace('\\/', '/')
                my_site_url = f"https://kinodomvideo.ru/video.php?video_token={iframe_url}"


                unique_id = str(uuid4())

                # Создание клавиатуры для фильма
                keyboard_buttons = [
                    [types.InlineKeyboardButton(text="🤗 Начать просмотр", url=my_site_url)]
                ]

                # Добавление кнопки трейлера, если он доступен
                if trailer_url:
                    keyboard_buttons.append([types.InlineKeyboardButton(text="🎬 Посмотреть трейлер", url=trailer_url)])

                # Добавление кнопки для повторения поиска в конец списка кнопок
                keyboard_buttons.append(
                    [types.InlineKeyboardButton(text='♻️ Повторить поиск', switch_inline_query_current_chat=""),
                     types.InlineKeyboardButton(text='👈 В меню', callback_data='back_user_now')])

                # Создание клавиатуры с кнопками
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

                # Сообщение в результате поиска

                result_text = types.InputTextMessageContent(
                    message_text=f"📽️ <b> Название: {film.get('title_ru')}</b>\n({film.get('title_en')})\n\n"
                                 f"🕥 <b>Дата выхода:</b> {description}\n\n"
                                 f"📷 <b>Качество:</b> {quality}\n\n Приятного просмотра! 🍿"
                )

                results.append(types.InlineQueryResultArticle(
                    id=unique_id,
                    title=title,
                    input_message_content=result_text,
                    description=description,
                    thumbnail_url=poster_url,
                    reply_markup=keyboard,
                ))

            if not films:
                unique_id = str(uuid4())

                ag_but = InlineKeyboardMarkup(inline_keyboard=again)

                results.append(types.InlineQueryResultArticle(
                    id=unique_id,
                    title="Результаты не обнаружены 🫣",
                    input_message_content=types.InputTextMessageContent(message_text='инструкция в разработке'),
                    description="Нажми на меня, чтобы узнать почему",
                    reply_markup=ag_but
                ))

            await inline_query.answer(results, cache_time=1, is_personal=True)


#command profile
@commands_router.callback_query(F.data == "profile")
async def profile(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку профиль')
    await callback.message.delete()
    user_id = callback.from_user.id
    date = fetch_user_date(user_id)
    await callback.message.answer(f'<b>Имя пользователя</b>: {callback.from_user.full_name}\n'
                                  f'<b>Дата регистрации</b>: {date}\n'
                                  f'<b>ID users</b>: <code>{callback.from_user.id}</code>')

@commands_router.callback_query(F.data == "s_full_users")
async def s_full_users(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку пользователи')
    await callback.message.delete()
    all_users = str(ferch_all_users())
    await callback.message.answer(f'<b>Пользователи:</b>{all_users}')


#command videogiad
@commands_router.callback_query(F.data == "videogaid")
async def videogaid(callback: types.CallbackQuery):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=back_button)
    url = "https://drive.google.com/uc?export=download&id=1aw5xnktqOgGq6U7OF-R3ykJkYLc6tQT7"
    await callback.message.delete()
    await callback.message.answer_video(video=url, caption='Это видео поможет вам понять,'
                                                         'как работать с ботом', reply_markup=reply_markup)



#command opportunities
@commands_router.callback_query(F.data == "opportunities")
async def opportunities(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку возможности')
    await callback.message.delete()
    await callback.message.answer(text="В этом боте вы сможете найти фильмы и сериалы которые так давно хотели "
                                       "посмотреть!")

@commands_router.callback_query(F.data == "back_a_m")
async def a_menu(callback: types.CallbackQuery):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_button)
    await callback.message.delete()
    await callback.message.answer(text='Вы перешли в админ меню', reply_markup=reply_markup)

@commands_router.callback_query(F.data == "check_me")
async def check_me(callback: types.CallbackQuery):
    return await menu(callback)




class Pages(StatesGroup):
    page = State()


@commands_router.callback_query(F.data == "Compilation")
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
                        message = (f"{index}. <b>Название фильма:</b> <i>{name}</i>, <i>{year}</i>\n<b>Описание:</b> "
                                   f"<b>{shortDescription}\n</b>")
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
                    await callback.message.answer("Произошла ошибка при запросе к API.")
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")



@commands_router.callback_query(F.data == "next")
async def check(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_page = data.get('page', 1)

    new_page = current_page + 1

    await state.update_data(page=new_page)

    await compilation(callback, state)

@commands_router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    current_page = data.get('page', -1)

    new_page = current_page - 1


    await state.update_data(page=new_page)

    await compilation(callback, state)

@commands_router.callback_query(F.data == "menu_clear")
async def clear(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await menu(callback)


@commands_router.callback_query(F.data == "random")
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
                    await callback.message.answer('\n\n'.join(messages), reply_markup=keyboard, parse_mode='HTML')

    except Exception as e:
        await callback.message.answer(f"Произошла ошибка: {str(e)}")
