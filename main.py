# pip install aiogram python-decouple
#aiogram == 3.0
# Cтворіть папку photo


import asyncio
import logging
import sys
import os
import uuid

from random import choice
from decouple import config


from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command

API_TOKEN = config('TELEGRAM_API_TOKEN')
ADMIN_ID = config('TELEGRAM_ADMIN_ID')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    await message.reply('Hi!')


@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await message.reply('Nice photo!')
    await bot.download(message.photo[-1].file_id, f'./photo/{len(os.listdir("photo"))}_{uuid.uuid4()}.jpg')
    # await bot.download_file(message.photo[-1].file_id, f'./photo/{message.photo[-1].file_id[:15]}.jpg')
    # await message.answer_photo(message.photo[-1].file_id, caption="Ну цікаво ж")
    # await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f'@{message.from_user.username} - {message.from_user.full_name} - {message.from_user.id}')
    print(message)

@dp.message(Command("photo"))
async def photo_handler(message: types.Message):
    list_photos = os.listdir("photo")
    photo = types.FSInputFile(f'photo/{choice(list_photos)}')
    await message.answer_photo(photo, caption="Ну цікаво ж")

async def main():
    print("Starting bot...")
    print("Bot username: @{}".format((await bot.me())))
    await dp.start_polling(bot)

asyncio.run(main())