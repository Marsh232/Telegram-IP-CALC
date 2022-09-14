#  Project: Telegram-IP-CALC
#  Filename: main.py
#  Create Date:
#  Marsh232 Copyright (c) 2022
#  SantaSpeen Copyright (c) 2022

import ipaddress
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType, ParseMode, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

from utils import Config

config = Config("config.json")
log = logging.getLogger("Bot")
bot = Bot(token=config.token)
dp = Dispatcher(bot)

network_button = KeyboardButton('Сеть')
subnet_button = KeyboardButton('Подсети')
start_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
start_buttons.row(network_button, subnet_button)


def calc_subnet(_ip):
    splt = _ip.split('/')  # Разделяет вводимый ip на часть с маской, и без
    if len(splt) == 1:
        splt.append("24")

    ip, mask = splt
    addr = ip + "/" + mask

    net = ipaddress.ip_network(addr, strict=False)  # В функцию кладётся сетевая часть ip, без хостовой части
    dict_out = {
        "addr": addr,
        "mask": f"{net.netmask} - {mask}",  # Выводит маску
        "net": f"{net}",  # Выводит сеть
        "broadcast": f'{net.broadcast_address}',  # Выводит broadcast
        "min": f"{net[1]}",
        "max": f"{net[-2]}",
        "hosts": f"{len(list(net.hosts()))}",
        "num": None
    }

    count = 0
    for n_ip in net.hosts():
        count += 1
        if str(n_ip) == ip:
            dict_out["num"] = count  # Выводит какой ip по счёту в сети

    return dict_out


def subnets(ip, prefix):
    subnet = ipaddress.ip_network(ip, strict=False)
    list_subnet = list(subnet.subnets(new_prefix=int(prefix)))
    subnet1 = ipaddress.ip_network(str(list_subnet[1]), strict=False)

    print('\nМаска:', subnet1.netmask, '=', prefix)
    print()

    for i in list_subnet:
        subnet2 = ipaddress.ip_network(i, strict=False)
        print('Network:', subnet2)
        print('Broadcast:', subnet2.broadcast_address)
        print('HostMin:', subnet2[1])
        print('HostMax:', subnet2[-2])
        print('Hosts:', len(list((subnet2.hosts()))))


@dp.message_handler(commands=["start"], chat_type=ChatType.PRIVATE)
async def start(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await msg.reply(f"Привет, дорогой мой {msg.from_user.username}", reply_markup=start_buttons)


@dp.message_handler(lambda msg: msg.text.lower().startswith('сеть'))
async def calcnet(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await msg.reply("Введи ip")


@dp.message_handler(regexp=r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}(|\/\d{0,2})$", chat_type=ChatType.PRIVATE)
async def calcnet1(msg):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    text = msg.text
    c = calc_subnet(text)
    await msg.reply(f"Вводимые данные: `{c['addr']}`\n"
                    f"Маска: `{c['mask']}`\n"
                    f"Сеть: `{c['net']}`\n"
                    f"Broadcast: `{c['broadcast']}`\n"
                    f"Мин адрес: `{c['min']}`\n"
                    f"Макс адрес: `{c['max']}`\n"
                    f"Всего адресов: `{c['hosts']}`\n"
                    f"Номер в сети: `{c['num']}`",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=start_buttons)


@dp.message_handler(lambda msg: msg.text.lower().startswith('подсети'))
async def calcsub(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    text = msg.text
    splt = text.split(" ")
    if len(splt) > 1:
        ip = splt[1]
        await msg.reply("Не готова")
    else:
        await msg.reply("**Командна введена не правильно**\n"
                        "Пример выполнения команды: `/calcsub 192.168.0.1/24 26`",
                        parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
