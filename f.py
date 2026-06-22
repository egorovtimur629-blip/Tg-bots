import asyncio
import datetime
import logging
import sys

import requests
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from pyexpat.errors import messages

BOT_TOKEN = ""

# session = AiohttpSession(proxy="http://72.56.115.39:3128")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class Survey(StatesGroup):
    InputName = State()
    InputAge = State()
    InputAnswer = State()

@dp.message(CommandStart())
async def function3(message: types.Message):
    await message.answer("Привет когда будешь готов пиши /start_servey")

@dp.message(Command("start_servey"))
async def start_servey(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Survey.InputName)

@dp.message(Survey.InputName)
async def input_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(Survey.InputAge)

@dp.message(Survey.InputAge)
async def input_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число")
        return
    await state.update_data(age=message.text)
    await message.answer("Что вы думаете о нашем сервисе?")
    await state.set_state(Survey.InputAnswer)

@dp.message(Survey.InputAnswer)
async def input_answer(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    answer = data.get("answer")
    await message.answer(f"Вас зовут {name}, вам {age} лет, и вы думаете о нашем сервисе: {answer}")
    await state.clear()
    await message.answer("Привет когда будешь готов пиши /start_servey")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())