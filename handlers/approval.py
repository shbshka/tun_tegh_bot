from aiogram import types
from data.database import engine, variables, Ticket
from datetime import datetime
from loader import bot, dp
from data.config import admins_id
from functions.f_sqlalchemy import sessionmaker, get_session
# from handlers.determine_card import russian_or_armenian
import os
from random import randint
import json

#----------------------------------------
#-----Пересылка сообщения с аппрувом-----
#----------------------------------------
async def approve_or_disapprove():
    @dp.callback_query_handler(text="approve")
    async def approve_transaction(call: types.CallbackQuery):
        msg_id = str(call.message.message_id)
        with open("screenshot_mapping.json", "r") as f:
            map = json.load(f)
        user_id = str(map[msg_id][0])
        x = str(map[msg_id][1])
        tkt_id = str(randint(0,999999)).zfill(6)
        print(f"[{datetime.now()}] New ticket for screenshot{x}.jpg - {tkt_id}-{user_id}")
        with engine.connect() as connection:
            users = variables.tables["users"]
            stmt = users.update().where(users.c.user_id == str(f"{user_id}")).values(if_paid = "y")
            connection.execute(stmt)
            connection.commit()
            connection.close()

            with open(f'./screenshots/screenshot{x}.jpg', "rb") as screenshot:
                await bot.send_message(user_id, "Transaction approved!\n"
                                                "Link to the channel with information about the party: https://t.me/+Ig2I2CwCe001ZDQy\n"
                                                f"Your ticket number: <u><b>{tkt_id}-{user_id}</b></u>", parse_mode="HTML")
                await bot.send_photo(admins_id, screenshot, caption=f"[{datetime.now()}] Transaction from {user_id} approved.\n"
                                                  f"Their ticket number is {tkt_id}-{user_id}")
            Session = sessionmaker(bind=engine)
            session = Session()
            new_ticket = Ticket(user_id=user_id, ticket_number=f"{tkt_id}-{user_id}")
            session.add(new_ticket)
            session.commit()
            session.close()

            await call.message.delete()
#            await russian_or_armenian(user_id, x)

    @dp.callback_query_handler(text="decline")
    async def decline_transaction(call: types.CallbackQuery):
        msg_id = str(call.message.message_id)
        with open("screenshot_mapping.json", "r") as f:
            map = json.load(f)
        user_id = str(map[msg_id][0])
        await bot.send_message(user_id,"Transaction was declined. Check again or send a valid screenshot")
        await call.message.delete()
