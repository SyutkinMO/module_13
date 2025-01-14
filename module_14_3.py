# ---------------------Доработка бота---------------------

# ------------------необходимые импорты----------------------
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----------------------SetUp параметры бота---------------------
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# ---------------------Клавиатуры--------------------
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Информация')],
        [
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)  # инициализируем клавиатуру

catalog_cb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")]
    ]
)


# --------------------Класс регистрации параметров пользователя------------------------


class UserState(StatesGroup):  # класс UserState наследованный от StatesGroup.
    """Внутри этого класса 3 объекта класса State: age, growth, weight (возраст, рост, вес)."""
    age = State()
    growth = State()
    weight = State()


# --------------------Хэндлеры--------------------


@dp.message_handler(text='Рассчитать')  # теперь реагирует на текст 'Рассчитать' на кнопке
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


@dp.message_handler(text='Купить')  # реагирует на текст 'Купить' на кнопке
async def get_buying_list(message):
    for i in range(4):
        with open(f'picture/{i + 1}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: Product{i + 1} | '
                                            f'Описание: описание {i + 1} | Цена: {(i + 1) * 100}')  # ответ с фото
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
