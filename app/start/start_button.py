import random
import sqlite3
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import admins



from app.admin.admin_menu import admin_start
from app.click.keybort import button
from app.comands.commands import menu

name = None
start_router = Router()


#command start
@start_router.message(Command("start"))
async def protect(message: types.Message):
    if message.from_user.id not in admins:

        num1 = random.randint(1, 11)
        num2 = random.randint(1, 11)
        correct_answer = num1 + num2
        buttons = [
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_1'),
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_2'),
            types.InlineKeyboardButton(text=str(random.randint(2, 21)), callback_data='num_3'),
        ]

        correct_position = random.randint(0, len(buttons))

        buttons.insert(correct_position, types.InlineKeyboardButton(text=str(correct_answer), callback_data="correct"))

        protect_buttons = [buttons]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard=protect_buttons)
        await message.answer(text=f"🛡 Для запуска, надо пройти проверку безопасности. Сколько будет {num1} + {num2}?",
                             reply_markup=reply_markup)
    else:
        return await admin_start(message)
def start(message: types.Message):
    conn = sqlite3.connect('bot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(100), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    message.answer( f'Привет {message.from_user}')
    message.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()

    message.answer(f'Продолжим {message.from_user}')
    message.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('bot.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, pass) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    message.answer(message.chat.id, f'Готово  {message.from_user}')

@start_router.callback_query(F.data == "correct")
async def start(callback: types.CallbackQuery):
    await callback.message.delete()
    reply_markup = InlineKeyboardMarkup(inline_keyboard=button)
    await callback.message.answer(text=f"Привет {callback.from_user.full_name}!", reply_markup=reply_markup)


@start_router.callback_query(F.data == "f_menu")
async def f_menu(callback: types.CallbackQuery):
    return await menu(callback)


@start_router.callback_query(F.data.in_({"num_1", "num_2", "num_3"}))
async def back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Попробуй снова!")
    return await protect(callback.message)


@start_router.message(Command("help", prefix="/!"))
async def hendel_help(message: types.Message):
    button = [
        [
            InlineKeyboardButton(text="Служба Поддержки🥸", url="https://t.me/Iltk01")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=button)
    await message.answer(text="Если у вас возникли проблемы, обратитесь в службу поддержки...", reply_markup=reply_markup)
