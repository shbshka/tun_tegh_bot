from information.information import afisha, info
from aiogram import types
from loader import bot, dp
from aiogram.dispatcher.filters import Text

@dp.message_handler(Text(equals="About event"))
async def send_message_with_photo(message: types.Message):
    with open(afisha, "rb") as afisha_o:
        await bot.send_photo(message.from_user.id, afisha_o)
        await bot.send_message(message.from_user.id, info)