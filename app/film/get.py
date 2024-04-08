from urllib.parse import quote
from uuid import uuid4
from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup
from app.click.keybort import again
from app.click.keybort import menu_button
import aiohttp


get_command = Router()


@get_command.inline_query()
async def inline_films(inline_query: types.InlineQuery):
    base_url = "https://apivb.info/api/videos.json?title={}&token=30c9ab7fcdf48b3b3d2eda889b6637cd"
    search_query = quote(inline_query.query)

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
                my_site_url = f"{iframe_url}"
                unique_id = str(uuid4())

                keyboard_buttons = [
                    [types.InlineKeyboardButton(text="🤗 Начать просмотр", url=my_site_url)]
                ]

                if trailer_url:
                    keyboard_buttons.append([types.InlineKeyboardButton(text="🎬 Посмотреть трейлер",
                                                                        url=trailer_url)])

                keyboard_buttons.append(
                    [types.InlineKeyboardButton(text='♻️ Повторить поиск', switch_inline_query_current_chat=""),
                     types.InlineKeyboardButton(text="меню↩️", callback_data="g_menu")])

                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

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
                    input_message_content=types.InputTextMessageContent(message_text=
                                                                        f'<b>Вы попали в главное меню!</b>\n'
                                                                        f'Для того, чтобы вам было проще понять бот,'
                                                                        f'вот пример как им пользоваться\n'
                                                                        f'<b>Правильно:</b>\n✅ бесстыжие\n✅ Довод'
                                                                        f'\n✅ Обитель зла\n✅ ЗВЕРОПОЛИС'
                                                                        f'\n\n<b>Неправильно:</b>\n'
                                                                        f'❌ бесстыжие 3 сезон\n'
                                                                        f'❌ kp571335\n❌ https://www.kinopoisk.ru\n'
                                                                        f'❌ https://www.kinopoisk.ru/series\n\n'
                                                                        f'<i>Для точного поиска '
                                                                        f'отправь боту точное название фильма</i>',),

                    description="Нажми на меня, чтобы узнать почему",
                    reply_markup=ag_but
                    ))

            await inline_query.answer(results, cache_time=1, is_personal=True)


@get_command.callback_query(F.data == "g_menu")
async def get_menu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    reply_markup = InlineKeyboardMarkup(inline_keyboard=menu_button)
    await callback.bot.send_message(chat_id=user_id,
                                    text=f'<b>Вы попали в главное меню!</b>\nДля того, чтобы вам было проще понять бот,'
                                         f'вот пример как им пользоваться\n<b>Правильно:</b>\n✅ бесстыжие\n✅ Довод'
                                         f'\n✅ Обитель зла\n✅ ЗВЕРОПОЛИС'
                                         f'\n\n<b>Неправильно:</b>\n'
                                         f'❌ бесстыжие 3 сезон\n❌ kp571335\n❌ https://www.kinopoisk.ru\n'
                                         f'❌ https://www.kinopoisk.ru/series\n\n'
                                         f'<i>Для точного поиска отправь боту точное название фильма</i>',
                                    reply_markup=reply_markup)



