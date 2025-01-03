# ---------------------Машина состояний---------------------


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):  # класс UserState наследованный от StatesGroup.
    """Внутри этого класса 3 объекта класса State: age, growth, weight (возраст, рост, вес)."""
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Calories')  # реагирует на текст 'Calories'
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
    norma_calories = 10 * data['weight'] + 6, 25 * data['growth'] - 5 * data['age'] + 5
    await message.answer(f'Ваша норма калорий {norma_calories} Ккал')
    await state.finish()  # Финишируем машину состояний


"""Важно поместить стартовые команды в конец, так как иначе бот не будет обрабатывать более редкие запросы"""


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer(
        'Привет! Я бот помогающий твоему здоровью. Введите команду Calories для подсчета суточной нормы калорий')


@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
