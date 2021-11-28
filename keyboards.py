from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnHello = KeyboardButton("/subscribe")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnHello)

btnDir1 = KeyboardButton("ИБ")
btnDir2 = KeyboardButton("БИ")
btnDir3 = KeyboardButton("ФИИТ")
btnDir4 = KeyboardButton("ПМ")
btnDir5 = KeyboardButton("ПМИ")
btnDir6 = KeyboardButton("ПИ")
btnDir7 = KeyboardButton("ИСТ")
Dir_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnDir1).add(btnDir2).add(btnDir3).add(btnDir4).add(btnDir5).add(btnDir6).add(btnDir7)
