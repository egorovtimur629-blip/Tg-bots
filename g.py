import asyncio
import datetime
import logging
import sys

import requests
import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from pyexpat.errors import messages

BOT_TOKEN = "8552725265:AAEkgktgtdT4MMfH6bnlDgrGx2IMWF3CeH0"

session = AiohttpSession(proxy="http://72.56.115.39:3128")
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(CommandStart())
async def function3(message: types.Message):
    await message.answer("Привет")

@dp.message()
async def function(message: types.Message):
    keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Кнопка 1", callback_data="button1"),
                InlineKeyboardButton(text="Кнопка 2", callback_data="button2"),
                InlineKeyboardButton(text="Кнопка 3", callback_data="button3"),
            ],
            [
                InlineKeyboardButton(text="Кнопка 4", callback_data="button4"),
                InlineKeyboardButton(text="Кнопка 5", callback_data="button5"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите кнопку:", reply_markup=keyboard_markup)

@dp.callback_query(lambda x: x.data == "button1")
async def f4(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Вы нажали кнопку 1")
     

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())