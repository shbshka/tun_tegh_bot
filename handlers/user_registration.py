from loader import bot, dp
from aiogram.dispatcher.filters import Text
from aiogram import types
from functions.f_sqlalchemy import get_session, add_user
from data.database import User
from data.config import admins_id
from datetime import datetime
from aiogram.dispatcher import FSMContext
import markups as nav
from aiogram.dispatcher.filters.state import StatesGroup, State

class Registration(StatesGroup):
    if_agree = State()
    name = State()
    surname = State()
    age = State()
    contacts = State()
    referrals = State()
    complete = State()

#---------------------
#-----Регистрация-----
#---------------------

#-----отмена регистрации-----
@dp.message_handler(Text(equals="Cancel registration"), state="*")
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Registration cancelled", reply_markup=nav.mainMenu)

#-----FSM-----
@dp.message_handler(Text(equals=("Register")))
async def assing_variables(message: types.Message):
    users = await get_session(User)
    if users != {}:
        user_ids = [x["user_id"] for x in users.values()]
        if str(message.from_user.id) in user_ids:
            await bot.send_message(message.from_user.id, "You are already registered", reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "By proceeding, you agree to share your personal data. Do you want to continue?\n"
                                                     "An alternative method to buy tickets is in <b>Tun Tegh</b>\n"
                                                     "(Mesrop Mashtoc avenue 5/4)", reply_markup=nav.registrationAgree, parse_mode="HTML")
            await Registration.if_agree.set()
    elif users == {}:
        await bot.send_message(message.from_user.id, "By proceeding, you agree to share your personal data. Do you want to continue?\n"
                                                     "An alternative method to buy tickets is in <b>Tun Tegh</b>\n"
                                                     "(Mesrop Mashtoc avenue 5/4)", reply_markup=nav.registrationAgree, parse_mode="HTML")
        await Registration.if_agree.set()

@dp.message_handler(Text(equals="Yes"), state=Registration.if_agree)
async def process_get_agreement(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["agreement"] = "received"
    await Registration.next()
    await bot.send_message(message.from_user.id, "What is your first name?")

@dp.message_handler(state=Registration.name, content_types="text")
async def process_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await Registration.next()
    await bot.send_message(message.from_user.id, "What is your surname?")


@dp.message_handler(state=Registration.surname, content_types="text")
async def process_get_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["surname"] = message.text
    await Registration.next()
    await bot.send_message(message.from_user.id, "How old are you?")

@dp.message_handler(state=Registration.age, content_types="text")
async def process_get_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["age"] = message.text
        try:
            age = int(data["age"])
        except ValueError:
            await bot.send_message(message.from_user.id, "Please cancel the registration, re-register and send a number")
        if age < 21:
            await bot.send_message(message.from_user.id, "You cannot access the event since it is 21+\n"
                                                         "To access the event on special terms, please contact @laguna1998", reply_markup=nav.mainMenu)
            data["agreement"] = "None"
            data["name"] = "None"
            data["surname"] = "None"
            data["contacts"] = "None"
            data["referrals"] = "None"
            await add_user(message, data)
            await state.finish()
        else:
            await Registration.next()
            await bot.send_message(message.from_user.id, "Please send here your <b>phone number</b> or <b>link to social media</b>", parse_mode="HTML")

@dp.message_handler(state=Registration.contacts, content_types="text")
async def process_get_contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["contacts"] = message.text
    await Registration.next()
    await bot.send_message(message.from_user.id, "Where did you learn about the event?")

@dp.message_handler(state=Registration.referrals, content_types="text")
async def process_get_referrals(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["referrals"] = message.text
    await Registration.next()
    await bot.send_message(message.from_user.id, "Complete registration?", reply_markup=nav.ifQuit)

@dp.message_handler(state=Registration.complete, content_types="text")
async def process_if_quit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(message.chat.id, f'Your name: <b>{data["name"]}</b>\n'
                                                f'Your surname: <b>{data["surname"]}</b>\n'
                                                f'Your age: <b>{data["age"]}</b>\n'
                                                f'Your contacts: <b>{data["contacts"]}</b>\n'
                                                f'You learned about the event from: <b>{data["referrals"]}</b>',
            reply_markup=nav.postRegistrationForm,
            parse_mode="HTML"
            )
        await add_user(message, data)
        await bot.send_message(message.from_user.id, "Now you can <u>pay the entrance fee</u> in your profile.\n"
                                                     "To do so, go to <b>'Main menu</b> --> <b>'My profile'</b> --> <b>'Pay'</b>",
                               parse_mode="HTML")
        await bot.send_message(admins_id, f"[{datetime.now()}] @{message.from_user.username} has registered")
