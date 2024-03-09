import sqlite3
import datetime
from aiogram import Dispatcher, types, Router
from aiogram.filters import Command, command



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

#DATE REG USERS
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

