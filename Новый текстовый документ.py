import asyncio
import datetime
import logging
import sys

import requests
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile

BOT_TOKEN = "8552725265:AAEkgktgtdT4MMfH6bnlDgrGx2IMWF3CeH0"

session = AiohttpSession(proxy="http://72.56.115.39:3128")
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(CommandStart())
async def function3(message: types.Message):
    await message.answer("Привет")

@dp.message(F.text == "Кнопка 1")
async def f4(message: types.Message):
    await message.answer("Вы нажали кнопку 1")

@dp.message(F.text == "Кнопка 4")
async def f5(message: types.Message):
    await message.answer("Вы нажали кнопку 4")

@dp.message()
async def function(message: types.Message):
    keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Кнопка 1"),
                KeyboardButton(text="Кнопка 2"),
                KeyboardButton(text="Кнопка 3"),
            ],
            [
                KeyboardButton(text="Кнопка 4"),
                KeyboardButton(text="Кнопка 5"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите кнопку:", reply_markup=keyboard_markup)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())






                                    