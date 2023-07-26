from loader import bot, dp
from data.config import admins_id
from datetime import datetime
import markups as nav
from aiogram import types
from functions.f_sqlalchemy import sessionmaker
from data.database import engine, Card
import os
import json

async def russian_or_armenian(user_id, x):
    with open(f"screenshot_mapping.json", "r") as f:
        map = json.load(f)
    with open(f"screenshots/screenshot{x}.jpg", "rb") as screenshot:
        await bot.send_photo(admins_id, screenshot, caption="Is the screenshot from Russian or from Armenian card?",
                             reply_markup=nav.transactionType)

    @dp.callback_query_handler()
    async def get_country(call: types.CallbackQuery):
        if call.data == "russian":
            country = "Russian"
        elif call.data == "armenian":
            country = "Armenian"
        else:
            pass
        await bot.send_message(admins_id, f"[{datetime.now()}] User {user_id} paid with {country} card")
        await call.message.delete()


        Session = sessionmaker(bind=engine)
        session = Session()

        new_card = Card(user_id=user_id,
                        country=country)
        session.add(new_card)
        session.commit()
        session.close()
