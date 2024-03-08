from aiogram import F, types, Router
from aiogram.types import InlineKeyboardMarkup

from app.click.keybort import menu_button, serials_button, films_button, anime_button, back_button

commands_router = Router()


#command menu
@commands_router.callback_query(F.data == "menu")
async def menu(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=menu_button)
    await callback.message.answer(text=f'Вы попали в главное меню! Здесь вы можете выбрать жанр фильма,'
                                       f' просмотреть подробную информацию и многое другое🫠', reply_markup=reply_markup)



#command serials
@commands_router.callback_query(F.data == "serials")
async def serials(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=serials_button)
    await callback.message.answer(text=f'Вы попали в главное меню! Здесь вы можете выбрать жанр фильма,'
                                       f' просмотреть подробную информацию и многое другое🫠', reply_markup=reply_markup)



#command faims
@commands_router.callback_query(F.data == "films")
async def films(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=films_button)
    await callback.message.answer(text=f'Выберите жанр, который хотите посмотреть📺', reply_markup=reply_markup)



#command anime
@commands_router.callback_query(F.data == "anime")
async def anime(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=anime_button)
    await callback.message.answer(text=f'Выберите жанр, который хотите посмотреть📺', reply_markup=reply_markup)



#command profile
@commands_router.callback_query(F.data == "profile")
async def profile(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f'Имя пользователя: {callback.from_user.full_name}\n\n'
                                  f'ID ussers: {callback.from_user.id}')



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
    await callback.message.delete()
    await callback.message.answer(text="В этом боте вы сможете найти фильмы и сериалы которые так давно хотели посмотреть!")


