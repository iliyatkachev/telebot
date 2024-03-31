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

import aiohttp


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


                unique_id = str(uuid4())

                # Создание клавиатуры для фильма
                keyboard_buttons = [
                    [types.InlineKeyboardButton(text="🤗 Начать просмотр", url=iframe_url)]
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




@commands_router.callback_query(F.data == "Compilation")
async def compilation(callback: types.CallbackQuery, page=1):
    films_URL = f"http://api.kinopoisk.dev/v1.4/movie?page={page}&limit=10&lists=top250"
    headers = {
        "accept": "application/json",
        "X-API-KEY": "R3ZHKRH-HXV4BW8-JSDD6W9-CZX102N"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=films_URL, headers=headers) as response:
                if response.status == 200:
                    data = await response.json(content_type=None)
                    films = data.get('docs', [])

                    messages = []
                    for index, film in enumerate(films, start=1 + (page - 1) * 10):
                        name = film.get('name', 'Название не указано')
                        shortDescription = film.get('shortDescription', 'Описание отсутствует')
                        year = film.get('year', 'Дата отсутствует')
                        message = f"{index}. <b>{name}:</b>\n{shortDescription}\n<b>{year}</b>"
                        messages.append(message)

                    keyboard = [
                        [
                            types.InlineKeyboardButton(text="Далее", callback_data=f"next_page_{page + 1}")
                        ]
                    ]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

                    if messages:
                        await callback.message.answer('\n\n'.join(messages), parse_mode='HTML', reply_markup=keyboard)
                    else:
                        await callback.message.answer("Фильмы не найдены.")
                else:
                    await callback.message.answer("Произошла ошибка при запросе к API.")
    except Exception as e:
        print(callback.message.answer(f"Произошла ошибка: {str(e)}"))

