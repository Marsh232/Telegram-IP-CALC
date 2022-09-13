from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

network = KeyboardButton('Сеть')
subnet = KeyboardButton('Подсети')
help = KeyboardButton('Помощь')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.row(network, subnet, help)