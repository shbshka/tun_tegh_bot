# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 20:27:33 2023

@author: Anna Shubkina
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#-----Main menu-----
btnRegister = KeyboardButton("Register")
btnViewPartyInfo = KeyboardButton("About event")
btnHelp = KeyboardButton("Help")
btnMain = KeyboardButton("Main menu")
btnViewData = KeyboardButton("My profile")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRegister, btnViewPartyInfo, btnHelp, btnViewData)

#-----Registration form-----
btnYes = KeyboardButton("Yes")
btnCancel = KeyboardButton("Cancel registration")
registrationForm = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)
registrationAgree = ReplyKeyboardMarkup(resize_keyboard=True).add(btnYes, btnCancel)

#-----Post-registration form-----
# btnReRegister = KeyboardButton("Изменить данные")
postRegistrationForm = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMain)

#------Change data-----
btnChangeName = InlineKeyboardButton("Change name", callback_data="name")
btnChangeQN = InlineKeyboardButton("Change question N", callback_data="question_n")
changeData = InlineKeyboardMarkup().add(btnChangeName, btnChangeQN)

#-----Complete registration-----
btnYes = KeyboardButton("Yes", callback_data="yes")
ifQuit = ReplyKeyboardMarkup(resize_keyboard=True).add(btnYes, btnCancel)

#-----View profile-----
btnViewProfile = KeyboardButton("View profile")
btnPay = KeyboardButton("Pay")
myProfile = ReplyKeyboardMarkup(resize_keyboard=True).add(btnViewProfile, btnPay, btnMain)

#-----Transaction-----
btnApprove = InlineKeyboardButton("Approve", callback_data="approve")
btnDecline = InlineKeyboardButton("Decline", callback_data="decline")
transaction = InlineKeyboardMarkup().add(btnApprove, btnDecline)

#-----Transaction type-----
btnRussian = InlineKeyboardButton("Russian", callback_data="russian")
btnArmenian = InlineKeyboardButton("Armenian", callback_data="armenian")
transactionType = InlineKeyboardMarkup().add(btnRussian, btnArmenian)

#-----Send screenshot-----
btnSend = KeyboardButton("Send the screenshot")
send = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSend)
