# -----------------------------Написание примитивной ORM-----------------------------


# ------------------необходимые импорты----------------------
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from module_14_5_CRUD import *

# ----------------------SetUp параметры бота---------------------
api = "7583741296:AAGKvr4Mc9kL5cL9JlT6XN8A1AQfGHXnz08"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# ---------------------Клавиатуры--------------------

# ------Главное меню------
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Купить'),
            KeyboardButton(text='Регистрация')
        ]
    ], resize_keyboard=True
)  # инициализируем стандартную клавиатуру

catalog_cb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]
    ]
)  # инициализируем инлайн клавиатуру


# --------------------Класс параметров для рассчета нормы ККал------------------------
class UserState(StatesGroup):  # класс UserState наследованный от StatesGroup.
    """Внутри этого класса 3 объекта класса State: age, growth, weight (возраст, рост, вес)."""
    age = State()
    growth = State()
    weight = State()


# --------------------Класс регистрации пользователя------------------------
class RegistrationState(StatesGroup):
    """объектsы класса State: username, email, age, balance(по умолчанию 1000)."""
    username = State()
    email = State()
    age = State()
    balance = 1000


# --------------------Хэндлеры--------------------

# ------------------------Машина состояний расчета нормы ККал------------------------

@dp.message_handler(text='Рассчитать')  # реагирует на текст 'Рассчитать' на кнопке
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)  # реагирует на UserState.age
async def set_growth(message, state):
    """Эта функция обновляет данные в состоянии age на message.text (написанное пользователем сообщение).
    Используется метод update_data."""
    await state.update_data(age=int(message.text))  # переводим в числовой вариант!
    await message.answer('Введите свой рост см')  # Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'
    await UserState.growth.set()  # После ожидать ввода роста в атрибут UserState.growth при помощи метода set.


@dp.message_handler(state=UserState.growth)  # реагирует UserState.growth
async def set_weight(message, state):
    """Эта функция обновляет данные в состоянии growth на message.text (написанное пользователем сообщение).
    Используется метод update_data."""
    await state.update_data(growth=int(message.text))  # переводим в числовой вариант!
    await message.answer('Введите свой вес в кг')  # Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'
    await UserState.weight.set()  # После ожидать ввода веса в атрибут UserState.weight при помощи метода set.


@dp.message_handler(state=UserState.weight)  # реагирует UserState.weight
async def send_calories(message, state):
    """Эта функция обновляет данные в состоянии weight на message.text (написанное пользователем сообщение).
        Используется метод update_data.
        Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий
    (для женщин или мужчин - на ваше усмотрение).
    Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно."""
    await state.update_data(weight=int(message.text))  # переводим в числовой вариант!
    data = await state.get_data()  # запомнить в переменную data все ранее введённые состояния (это будет словарь)
    norma_calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    await message.answer(f'Ваша норма калорий {norma_calories} Ккал')
    await state.finish()  # Финишируем машину состояний


# ------------------------Машина состояний регистрации пользователя------------------------


@dp.message_handler(text='Регистрация')  # реагирует на текст 'Регистрация' на кнопке
async def sing_up(message):
    initiate_db()
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    """Эта функция проверяет наличие message.text (написанное пользователем сообщение) в БД."""
    if is_included(message.text):  # если такой username уже есть
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)  # добавляем данные username
        await message.answer("Введите свой email:")  # запрос email
        await RegistrationState.email.set()  # После ожидать ввода email


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    """Функция добавляет email"""
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    """Добавляет возраст пользователя. Далее берет все данные (username, email и age) из состояния и записывает в
    таблицу Users при помощи ранее написанной crud-функции add_user."""
    await state.update_data(age=message.text)
    data = await state.get_data()  # извлекаем данные из состояния
    add_user(data.get('username'), data.get('email'), data.get('age'))
    await message.answer(f'Вы успешно зарегистрированы')
    await state.finish()


# -----------------------Оставшиеся хэндлеры-----------------------


@dp.message_handler(text='Купить')  # реагирует на текст 'Купить' на кнопке
async def get_buying_list(message):
    for i in range(len_db()):  # использует прописанные в CRUD функции
        with open(f'picture/{i + 1}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: {get_all_products().get(i + 1)[1]} | '
                                            f'Описание: {get_all_products().get(i + 1)[2]} | '
                                            f'Цена: {get_all_products().get(i + 1)[3]}')  # ответ с фото
    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_cb)


@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Привет! Здесь ты можешь рассчитать суточную норму каллорий и приобрести витамины!')


@dp.callback_query_handler(text='product_buying')  # покупка
async def get_formulas(call):  # важно для удобства используется call
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer  # обязательно для завершения вызова


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
