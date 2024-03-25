from aiogram import F, types, Router
from aiogram.types import InlineKeyboardMarkup
from app.SQL.sql import fetch_user_date, ferch_all_users, find_public_ids
from app.click.keybort import menu_button, back_button, admin_button
from app.channel.channel_funk import channels_add
from aiogram.utils.markdown import hlink
from urllib.parse import quote

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
    base_url = "https://apivb.info/api/videos.json?title={}&token=0befa987b7d85bcdad0b31e2e7c3f4ec"
    search_query = quote(inline_query.query)  # Кодирование запроса пользователя для использования в URL

    # Формирование URL с учетом поискового запроса
    url = base_url.format(search_query)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            results = []

            if response.status == 200:
                movies = await response.json(content_type=None)
                for index, movie in enumerate(movies, start=1):
                    title = movie.get("title_ru", "Название не указано")
                    iframe_url = movie.get("iframe_url", "#")
                    text = f'Название: {title}\nURL: {hlink("Смотреть фильм", iframe_url)}'

                    result = types.InlineQueryResultArticle(
                        id=str(index),
                        title=title,
                        input_message_content=types.InputTextMessageContent(
                            message_text=text, parse_mode="HTML"
                        ),
                        description="Нажмите для просмотра информации о фильме",
                    )
                    results.append(result)

            # Ответ пользователю с результатами поиска
            await inline_query.answer(results, cache_time=1)


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



