from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from crud_functions_new import *
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_4 = KeyboardButton(text='Регистрация')
kb.row(button_1, button_2)
kb.row(button_3, button_4)

kb_2 = InlineKeyboardMarkup()
kb_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
kb_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_2.add(kb_button_1, kb_button_2)

pr = InlineKeyboardMarkup()
pr_button_1 = InlineKeyboardButton(text='Product1',  callback_data='product_buying')
pr_button_2 = InlineKeyboardButton(text='Product2',  callback_data='product_buying')
pr_button_3 = InlineKeyboardButton(text='Product3',  callback_data='product_buying')
pr_button_4 = InlineKeyboardButton(text='Product4',  callback_data='product_buying')
pr.row(pr_button_1, pr_button_2, pr_button_3, pr_button_4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    #    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Этот бот создан, чтобы помочь людям '
                         'встать на путь здрового образа жизни.\n'
                         'Скорее жми кнопку "Рассчитать" '
                         'и узнай, сколько же калорий требуется '
                         'твоему организму!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_2)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    table = get_all_products()
    for product in table:
        with open(f'{product[0]}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {product[1]} | Описание: описание {product[2]} | Цена: {product[3]}')
    await message.answer('Выберите продукт для покупки: ', reply_markup=pr)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age_ = data['age']
    growth_ = data['growth']
    weight_ = data['weight']
    await message.answer(f'Ваша норма калорий: {10 * weight_ + 6.25 * growth_ - 5 * age_ + 5}')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    name = is_included(data['username'])
    if name is True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username_ = data['username']
    email_ = data['email']
    age_ = data['age']
    print(data)
    add_user(username_, email_, age_)
    await message.answer("Регистрация прошла успешно!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
