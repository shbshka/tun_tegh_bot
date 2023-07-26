# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 20:23:35 2023

@author: Anna Shubkina
"""

# ----- nest-asyncio -----
import nest_asyncio
nest_asyncio.apply()

# -----aiogram-----
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

#----- bot config -----
from data.config import idram, mir, admins_id
from data.database import engine, User, Ticket, Card
from loader import dp, bot


# -----innate imports------
import markups as nav


# -----sqlalchemy-----
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)

# ----- apsheduler ------
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime

#---- общие функции и классы-----

from functions.f_apschedule import send_scheduled_message

# ----- Стартовое сообщение -----
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    username = message.from_user.username
    await bot.send_message(
        message.from_user.id,
        "Hello, {0.first_name}! Glad to see you here!".format(message.from_user),
        reply_markup=nav.mainMenu)
    from functions.notify_admins import on_startup_notify
    await on_startup_notify(username, dp)
    print(message.chat.
          id)

@dp.message_handler(Text(equals="Main menu"), state="*")
async def return_to_main(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Back to the main menu", reply_markup=nav.mainMenu)
    await state.finish()


@dp.message_handler(Text(equals="Help"))
async def refer_to_admins(message: types.Message):
    await bot.send_message(message.from_user.id,
                              "To get a payment bill, please <b>register</b>!\n"
                              "@shbshka - technical issues\n"
                              "@laguna1998 - other questions", parse_mode="HTML")


#-------------------
#----Запуск бота----
#-------------------

async def start():
    print(f"[{datetime.now()}] Starting the bot...")
    scheduler = AsyncIOScheduler(timezone="Asia/Yerevan")
    scheduler.add_job(send_scheduled_message, trigger="date",
                        run_date=datetime(2023, 7, 5, 12, 00, 0))
    scheduler.start()
    print(f"[{datetime.now()}] The bot has started")
    from handlers import dp
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
