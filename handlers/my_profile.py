from loader import bot, dp
from data.database import User
from functions.f_sqlalchemy import get_session
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import date
from datetime import datetime
from data.config import admins_id, idram, mir
import markups as nav
from functions.hasher import is_different_image
from handlers.approval import approve_or_disapprove
from aiogram.dispatcher.filters.state import StatesGroup, State
import os
import json


class Pay(StatesGroup):
    screenshot = State()

#----------------
#-----Профиль----
#----------------

@dp.message_handler(Text(equals="View profile"), state="*")
async def choose_action(message: types.Message, state=FSMContext):
    users = await get_session(User)
    for user in users.values():
        if user["user_id"] == str(message.from_user.id) and user["name"] != "None":
            await bot.send_message(message.from_user.id,
                         f"Name: <b>{user['name']}</b>\n"
                         f"Surname: <b>{user['surname']}</b>\n"
                         f"Age: <b>{user['age']}</b>\n"
                         f"Contacts: <b>{user['contacts']}</b>", parse_mode="HTML")
        elif user["name"] == "None":
            await bot.send_message(message.from_user.id, "You are underage and cannot perform any actions here")
    await state.finish()

@dp.message_handler(Text(equals="Pay"))
async def pay(message: types.Message, state: FSMContext):
    await state.finish()
    users = await get_session(User)
    deadline = date(2023, 7, 6)
    for user in users.values():
        if deadline <= date.today() and user["name"] != "None":
            await bot.send_message(message.from_user.id, "Sorry, the event has nearly or already started\n"
                                                         "You cannot buy tickets here anymore\n"
                                                         "To buy a ticket, please contact @laguna1998")
        elif user["name"] != "None" and user["user_id"] == str(message.from_user.id):
            await bot.send_message(message.from_user.id, "Links to pay the entrance fee\n"
                                                         "|\n"
                                                         "|\n"
                                                         "V\n"
                                                         f"iDram: <b>{idram}</b> (5000 AMD)\n"
                                                         f"Russian MIR: <b>{mir}</b> (1200 RUB)\n"
                                                         "\n"
                                                         "You can buy the tickets until <u><b>5.07.2022 23:59</b></u>\n"
                                                         "Please send a <u>screenshot</u> of your payment right after this message", parse_mode="HTML")
            await Pay.screenshot.set()
        elif user["name"] == "None":
            await bot.send_message(message.from_user.id, "You are underage and cannot perform any actions here")


@dp.message_handler(state=Pay.screenshot, content_types="photo")
async def get_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    filelist = os.listdir("screenshots")
    x = len([int(name.split("screenshot")[1].split(".jpg")[0]) for name in filelist])
    await message.photo[-1].download(destination_file=f"./temporary_screenshots/screenshot.jpg")
    if is_different_image(f"./temporary_screenshots/screenshot.jpg"):
        await message.photo[-1].download(destination_file=f"./screenshots/screenshot{x}.jpg")
        with open(f"screenshots/screenshot{x}.jpg", "rb") as screenshot:
            msg = await bot.send_photo(chat_id=admins_id, photo=screenshot, caption="Approve the transaction", reply_markup=nav.transaction)
            msg_id = str(msg.message_id)
            await bot.send_message(message.from_user.id,
                           "Your screenshot is sent for verification, you will receive a notification if it is successful")
            await state.finish()
            with open("screenshot_mapping.json", "r") as f:
                maps = json.load(f)
            maps[str(msg_id)] = [str(user_id), str(x)]
            with open("screenshot_mapping.json", "w") as f:
                json.dump(maps, f)

            await approve_or_disapprove()
    else:
        await bot.send_message(message.from_user.id, "This is the same screenshot. "
                                                     "Press <b>Pay</b> and send a different one", parse_mode="HTML")
        await state.finish()
    temp_file_list = [os.path.join("./temporary_screenshots", x) for x in os.listdir("./temporary_screenshots")]
    for x in temp_file_list:
        os.remove(x)

@dp.message_handler(Text(equals="My profile"))
async def view_data(message: types.Message):
    users = await get_session(User)
    if users != {}:
        ids = [str(entry["user_id"]) for entry in users.values()]
        if str(message.from_user.id) in ids:
            await bot.send_message(message.from_user.id, "Choose what you want to do", reply_markup=nav.myProfile)
        else:
            await bot.send_message(message.from_user.id, "Please register", reply_markup=nav.mainMenu)
    else:
        await bot.send_message(message.from_user.id, "Be the first to register!", reply_markup=nav.mainMenu)

