import asyncio
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import bot_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()

#обработка команды старт
@dp.message(CommandStart())
async def hendel_start(message: types.Message):
    await message.answer(text=f'Hello, {message.from_user.full_name}!')

#обработка команды хелп
@dp.message(Command("help"))
async def hendel_help(message: types.Message):
    await message.answer(text="Если у вас возникли проблемы, обратитесь в службу поддержки...")

#стартовая кнопка
@dp.message()
async def echo(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Простите, я не понимаю вас...")

#логика бота
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


