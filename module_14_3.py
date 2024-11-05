from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
kb.row(button_1, button_2, button_3)

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
    with open('1.jpg', 'rb') as img_1:
        await message.answer_photo(img_1, 'Название: Product1 | Описание: описание number1 | Цена: 100')
    with open('2.jpg', 'rb') as img_2:
        await message.answer_photo(img_2, 'Название: Product2 | Описание: описание number2 | Цена: 200')
    with open('3.jpg', 'rb') as img_3:
        await message.answer_photo(img_3, 'Название: Product3 | Описание: описание number3 | Цена: 300')
    with open('4.jpg', 'rb') as img_4:
        await message.answer_photo(img_4, 'Название: Product4 | Описание: описание number4 | Цена: 400')
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


# @dp.message_handler()
# async def all_messages(message):
#    print('Введите команду /start, чтобы начать общение.')
#    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
