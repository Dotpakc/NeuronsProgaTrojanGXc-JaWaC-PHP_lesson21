# pip install aiogram python-decouple
#aiogram == 3.0
# Cтворіть папку photo


import asyncio
import logging
import sys
import os
import uuid
import json

from random import choice, randint
from decouple import config


from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command

API_TOKEN = config('TELEGRAM_API_TOKEN')
ADMIN_ID = config('TELEGRAM_ADMIN_ID')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()



def save_data():
    with open('users.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def load_data():
    global users
    try:
        with open('users.json', 'r', encoding='utf-8') as file:
            users = json.load(file)
    except:
        users = []


def create_user(user_id, username, full_name):
    users.append({
        "id": user_id,
        "username": username,
        "full_name": full_name,
        "balance": 500,
    })
    save_data()
    return users[-1]

def check_user(from_user: types.User):
    user_id = from_user.id
    for user in users:
        if user['id'] == user_id:
            return user
    return create_user(user_id, from_user.username, from_user.full_name)

def chenge_balance(user_id, value):
    for user in users:
        if user['id'] == user_id:
            user['balance'] += value
            save_data()
            return user['balance']
    return False



load_data()
users = [# {id, username, full_name , balance}

]

# ban_list = [
#
# ]


@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    await message.reply('Hi!')
    user = check_user(message.from_user)
    if user['balance'] == 0:
        await message.answer(f'Ви новий користувач, ваш баланс: {user["balance"]}')
    else:
        await message.answer(f'Ваш баланс: {user["balance"]}')



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

@dp.message(Command("time"))
async def photo_handler(message: types.Message):
    await message.answer(f'Теперішній час: {message.date}')
    # text = f'Теперішній час: {message.date.hour}:{message.date.minute}:{message.date.second}'
    text = f'Теперішній час: {message.date.strftime("%H:%M:%S")}'
    await message.answer(text)

@dp.message(F.animation | F.video | F.video_note | F.voice | F.audio | F.document | F.sticker)
async def some_handler(message: types.Message):

    # if message.from_user.id in [el['id'] for el in ban_list]:
    #     if message.date - [el['time'] for el in ban_list if el['id'] == message.from_user.id][0] < 60:
    #         await message.answer(f'Ви заблоковані на 60 секунд')
    #         return False
    #     else:
    #         ban_list.remove([el for el in ban_list if el['id'] == message.from_user.id][0])
    #         await message.answer(f'Ви розблоковані')
    #     return False
    # await message.reply('Nice media!')
    try:
        balance = chenge_balance(message.from_user.id, 2)
        await message.answer(f'Ваш баланс: {balance}')
    except:
        pass
        # ban_list.append({'id': message.from_user.id, 'time': message.date})
    # await message.copy_to(message.from_user.id, caption=f'LOL')
    # await message.copy_to(ADMIN_ID, caption=f'@{message.from_user.username} - {message.from_user.full_name} - {message.from_user.id}')


@dp.message(Command("rep"))
async def rep_handler(message: types.Message):
    button = types.KeyboardButton(text="Yes")
    button2 = types.KeyboardButton(text="No")
    button3 = types.KeyboardButton(text="Відправити моє місцезнаходження", request_location=True)
    button4 = types.KeyboardButton(text="Відправити мій номер телефону", request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [button, button2],
        [button3, button4]
    ])

    await message.answer("Do you like aiogram?", reply_markup=markup)

@dp.message( (F.text == "Yes") | (F.text == "No") )
async def rep_handler(message: types.Message):
    if message.text == "Yes":
        await message.answer("Cool!")
    else:
        await message.answer("Why?")

    await message.answer("lol", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.location)
async def rep_handler(message: types.Message):
    await message.answer(f'Ваше місцезнаходження: {message.location.latitude} - {message.location.longitude}')
    await bot.send_message(ADMIN_ID, f'Місцезнаходження: {message.location.latitude} - {message.location.longitude} - {message.from_user.username} - {message.from_user.full_name} - {message.from_user.id}')

@dp.message(F.contact)
async def rep_handler(message: types.Message):
    await message.answer(f'Ваш номер телефону: {message.contact.phone_number}')
    await bot.send_message(ADMIN_ID, f'Номер телефону: {message.contact.phone_number} - {message.contact.first_name} - {message.contact.last_name} - {message.contact.user_id}')


@dp.message(Command("inline"))
async def inline_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Yes", callback_data="yes"),
            types.InlineKeyboardButton(text="No", callback_data="no"),
        ],
        [
            types.InlineKeyboardButton(text="🎰", callback_data="slot"),
        ]
    ])
    await message.answer("Do you like aiogram?", reply_markup=markup)

@dp.callback_query(F.data == 'yes')
async def inline_handler(call: types.CallbackQuery):
    await call.answer("Done")
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Back to start", callback_data="start"),
            types.InlineKeyboardButton(text="No", callback_data="no"),
        ],
    ])
    await call.message.edit_text("Realy YEs?", reply_markup=markup)


@dp.callback_query(F.data == 'no')
async def inline_handler(call: types.CallbackQuery):
    await call.answer("fdsfsdfsdfsdfsdfsdfsdfsdfsdf")
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Back to start", callback_data="start"),
            types.InlineKeyboardButton(text="Yes", callback_data="yes"),
        ],
    ])
    await call.message.edit_text("Realy No?", reply_markup=markup)

@dp.callback_query(F.data == 'start')
async def inline_handler(call: types.CallbackQuery):
    await call.answer("fdsfsdfsdfsdfsdfsdfsdfsdfsdf")
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Yes", callback_data="yes"),
            types.InlineKeyboardButton(text="No", callback_data="no"),
        ],
        [
            types.InlineKeyboardButton(text="🎰", callback_data="slot"),
        ]
    ])
    await call.message.edit_text("Do you like aiogram?", reply_markup=markup)


@dp.callback_query(F.data == 'slot')
async def slot_handler(call: types.CallbackQuery):
    user = check_user(call.from_user)
    print(user)
    if user['balance'] < 10:
        await call.answer("У вас недостатньо коштів", show_alert=True)
        return False

    chenge_balance(user['id'], -10)

    list_emoji = ["🍎", "🍊", "🍋", "🍌", "🍉", "🍇","7️⃣"]
    lists_of_wins = [
        {"slot": ["7️⃣", "7️⃣", "7️⃣"], "win": 100},

        {"slot": ["🍎", "🍎", "🍎"], "win": 50},
        {"slot": ["🍊", "🍊", "🍊"], "win": 50},
        {"slot": ["🍋", "🍋", "🍋"], "win": 50},
        {"slot": ["🍌", "🍌", "🍌"], "win": 50},
        {"slot": ["🍉", "🍉", "🍉"], "win": 50},
        {"slot": ["🍇", "🍇", "🍇"], "win": 50},

        {"slot": ["🍇", "🍇", "*"], "win": 25},
        {"slot": ["🍋", "🍋", "*"], "win": 10},

    ]

    r = [choice(list_emoji) for _ in range(3)]
    win = 0
    for el_win in lists_of_wins:
        if el_win["slot"] == r:
            win = el_win["win"]
            break
        elif el_win["slot"][-1] == '*' and el_win["slot"][:-1] == r[:-1]:
            win = el_win["win"]
            break
    chenge_balance(user['id'], win)
    user = check_user(call.from_user)
    text = f'???{r[0]}{r[1]}{r[2]}???\nВи виграли: {win} ??\nВаш баланс: {user["balance"]}'

    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Спробувати ще раз", callback_data="slot"),
        ],
        [
            types.InlineKeyboardButton(text="Back to start", callback_data="start"),
        ],
    ])
    await call.message.edit_text(text, reply_markup=markup)



async def main():
    print("Starting bot...")
    print("Bot username: @{}".format((await bot.me())))
    await dp.start_polling(bot)

asyncio.run(main())