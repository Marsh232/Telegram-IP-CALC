from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

network_button = KeyboardButton('Сеть')
subnet_button = KeyboardButton('Подсети')
help_button = KeyboardButton('Помощь')

kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb.row(network_button, subnet_button, help_button)
