from data.database import User
from functions.f_sqlalchemy import get_session
from loader import bot
async def send_scheduled_message():
    dict_of_users = await get_session(User)
    paid_users = []
    for x in range(0, len(dict_of_users)):
        if dict_of_users[x]["if_paid"] == "y":
            paid_users.append(dict_of_users[x])
            await bot.send_message(int(dict_of_users[x]["user_id"]),
                                   "Welcome to Tun-Tegh PulPulak!\n"
                                   "Link to the channel with information about the party: https://t.me/+Ig2I2CwCe001ZDQy")
