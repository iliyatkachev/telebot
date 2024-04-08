from aiogram import F, types, Router
from app.SQL.sql import fetch_all_users, find_public_ids
from app.click.keybort import menu_button, admin_button
from app.channel.channel_funk import channels_add
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


commands_router = Router()


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
        await callback.message.answer(text=
                                         f'<b>Вы попали в главное меню!</b>\nДля того, чтобы вам было проще понять бот,'
                                         f'вот пример как им пользоваться\n<b>Правильно:</b>\n✅ бесстыжие\n✅ Довод'
                                         f'\n✅ Обитель зла\n✅ ЗВЕРОПОЛИС'
                                         f'\n\n<b>Неправильно:</b>\n'
                                         f'❌ бесстыжие 3 сезон\n❌ kp571335\n❌ https://www.kinopoisk.ru\n'
                                         f'❌ https://www.kinopoisk.ru/series\n\n'
                                         f'<i>Для точного поиска отправь боту точное название фильма</i>',
                                      reply_markup=reply_markup)


@commands_router.callback_query(F.data == "s_full_users")
async def s_full_users(callback: types.CallbackQuery):
    await callback.answer('Вы перешли во вкладку пользователи')
    await callback.message.delete()
    all_users = str(fetch_all_users())
    await callback.message.answer(f'<b>Пользователи:</b>{all_users}')


@commands_router.callback_query(F.data == "videogaid")
async def videogaid(callback: types.CallbackQuery):
    back_button_non = [
        [
            InlineKeyboardButton(text='Вернуться назад', callback_data='back_back_back')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=back_button_non)
    url = "https://drive.google.com/uc?export=download&id=1aw5xnktqOgGq6U7OF-R3ykJkYLc6tQT7"
    await callback.message.delete()
    await callback.message.answer_video(video=url, caption='Это видео поможет вам понять,'
                                                           'как работать с ботом', reply_markup=reply_markup)



@commands_router.callback_query(F.data == "back_a_m")
async def a_menu(callback: types.CallbackQuery):
    reply_markup = InlineKeyboardMarkup(inline_keyboard=admin_button)
    await callback.message.delete()
    await callback.message.answer(text='Вы перешли в админ меню', reply_markup=reply_markup)


@commands_router.callback_query(F.data == "check_me")
async def check_me(callback: types.CallbackQuery):
    return await menu(callback)
