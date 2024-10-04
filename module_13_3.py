from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "7793896466:AAFu86QIxEwI8iQ5iJpXqoxrKYWkEn7GyUI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['Urban', 'ff'])
async def urban_messages(message):
    print("Urban message")


@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
