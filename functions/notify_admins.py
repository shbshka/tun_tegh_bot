# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:31:07 2023

@author: Anna Shubkina
"""
import logging
from datetime import datetime
from aiogram import types
from data.config import admins_id
from aiogram import Dispatcher

async def on_startup_notify(user_id, dp: Dispatcher):
    try:
        text = f'[{datetime.now()}] Bot was started by @{user_id}'
        await dp.bot.send_message(admins_id, text)
    except Exception as err:
        logging.exception(err)
