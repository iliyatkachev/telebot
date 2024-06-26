import sqlite3
import datetime
from aiogram import Dispatcher, types, Router


dp = Dispatcher()
name = None
sql_router = Router()
#


#SELECT LIST
def ferch_all_users():
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM login_id")
    all_users = cursor.fetchall()
    cursor.close()
    connect.close()
    return [user[0] for user in all_users]

#DATA REG USERS
def fetch_user_date(user_id):
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()
    cursor.execute("SELECT date FROM login_id WHERE user_id = (?)", (user_id,))
    user_date = cursor.fetchone()
    cursor.close()
    connect.close()
    if user_date:
        return user_date[0]
    else:
        return None

#NAME
def fetch_user_name(user_id):
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM login_id WHERE user_id = (?)", (user_id,))
    user_name = cursor.fetchone()
    cursor.close()
    connect.close()
    if user_name:
        return user_name[0]
    else:
        return None



#ADD SQL BD
async def bd(message: types.Message):
    all_users = ferch_all_users()
    user_id = message.from_user.id

    if user_id not in all_users:
        connect = sqlite3.connect('users_bd.db')
        cursor = connect.cursor()
        users_id = message.from_user.id
        cursor.execute("INSERT INTO login_id (user_id, date, name) VALUES (?, ?, ?)", (users_id, datetime.datetime.now(), message.from_user.full_name),)
        connect.commit()
        cursor.close()
        connect.close()
    else:
        pass




async def add_channel(name: str, url: str, id_channel: str):
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM channels WHERE id_channel = ?", (id_channel,))
    channel_exists = cursor.fetchone()

    if not channel_exists:
        cursor.execute("INSERT INTO channels (name, url, id_channel) VALUES (?, ?, ?)", (name, url, id_channel))
        connect.commit()
    else:
        pass

    cursor.close()
    connect.close()


async def delete_all_channels(message: types.Message):
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("DELETE FROM channels")
    connect.commit()

    if cursor.rowcount > 0:
        await message.answer("Все каналы были успешно удалены из базы данных.")
    else:
        await message.answer("В базе данных не было найдено каналов для удаления.")

    cursor.close()
    connect.close()


def fetch_urls_and_ids():
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("SELECT url FROM channels")
    rows = cursor.fetchall()

    urls = [row[0] for row in rows]

    cursor.close()
    connect.close()

    return urls




def find_public_ids():
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("SELECT id_channel FROM channels")
    rows = cursor.fetchall()

    ids = [row[0] for row in rows]

    cursor.close()
    connect.close()

    return ids



async def add_admin(name, id_admin):
    connect = sqlite3.connect('users_bd.db')
    cursor = connect.cursor()

    cursor.execute("INSERT INTO admin(name, id_admin) VALUES (?, ?)",
                   (name, id_admin))

    connect.commit()
    cursor.close()
    connect.close()


async def fetch_admins_from_db():
    connect = sqlite3.connect('users_bd.db')  # Путь к вашей базе данных
    cursor = connect.cursor()
    # Запрос на выборку всех user_id администраторов из таблицы
    cursor.execute("SELECT id_admin FROM admin")
    admins = cursor.fetchall()  # Получаем список кортежей с одним элементом

    cursor.close()
    connect.close()

    return [admin[0] for admin in admins]