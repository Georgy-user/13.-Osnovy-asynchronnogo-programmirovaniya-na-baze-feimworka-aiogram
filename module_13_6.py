from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
request_botton = KeyboardButton(text='Рассчитать')
inform_botton = KeyboardButton(text='Информация')
kb.row(request_botton, inform_botton)

kb_in = InlineKeyboardMarkup(resize_keyboard=True)
request_in_botton = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Calories')
inform_in_botton = InlineKeyboardButton(text='Формула для расчёта', callback_data='Formula')
kb_in.row(request_in_botton, inform_in_botton)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите операцию', reply_markup=kb_in)

@dp.callback_query_handler(text='Formula')
async def get_formula(call):
    await call.message.answer('Формула для расчёта оптимального количества получаемых килокалорий (кК): '
                              'Норма кК = 1,2 * [10 * вес(в кг) + 6,25 * рост(в см) - 5 * возраст(в годах) + 5].')
    await call.answer()

@dp.callback_query_handler(text='Calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст в годах: целое число от 13 до 80.')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост в сантиметрах.')
    await UserState.growth.set()


@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свою массу в килограммах.')
    await UserState.weight.set()


@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    quantity_kilocalories = 1.2 * (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']))
    await message.answer(f'Для сохранения нормального веса или для оптимального похудения при средней физической '
                         f'активности Вам необходимо получать {quantity_kilocalories} килокалорий в сутки.')
    await state.finish()


@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer('Информация о боте')


@dp.message_handler(commands=['start'])
async def start_messages(message):
    await message.answer('Привет! Я бот, помогающий Вашему здоровью. Если хотите узнать колическтво килокалорий, '
                         'которое нужно получать Вам для сохранения нормального веса или для оптимального похудения, '
                         'нажмите на кнопку "Рассчитать".', reply_markup = kb)


@dp.message_handler(text=['Спасибо.', 'Спасибо', 'спасибо','Спасибо!'])
async def set_age(message):
    await message.answer('Пожалуйста!')
    await UserState.age.set()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
