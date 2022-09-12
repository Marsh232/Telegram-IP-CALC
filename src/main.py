#  Project: Telegram-IP-CALC
#  Filename: main.py
#  Create Date:
#  Marsh232 Copyright (c) 2022
#  SantaSpeen Copyright (c) 2022

import ipaddress
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatType, ParseMode
from aiogram.utils import executor

from src.config import Config

config = Config("config.json")
log = logging.getLogger("Bot")
bot = Bot(token=config.token)
dp = Dispatcher(bot)


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
        "max": f"{net[1]}",
        "min": f"{net[-2]}",
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
    await msg.reply(f"Привет, дорогой мой {msg.from_user.username}")


@dp.message_handler(commands=["help"], chat_type=ChatType.PRIVATE)
async def start(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await msg.reply("Ты беспомощный")


@dp.message_handler(commands=["calc"], chat_type=ChatType.PRIVATE)
async def calc(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    text = msg.text
    splt = text.split(" ")
    if len(splt) > 1:
        ip = splt[1]
        c = calc_subnet(ip)
        await msg.reply(f"Данные ввода: `{c['addr']}`\n"
                        f"Маска: `{c['mask']}`\n"
                        f"Сеть: `{c['net']}`\n"
                        f"Broadcast: `{c['broadcast']}`\n"
                        f"Макс адресов: `{c['max']}`\n"
                        f"Мин адресов: `{c['min']}`\n"
                        f"Всего адресов: `{c['hosts']}`\n"
                        f"Номер в сети: `{c['num']}`",
                        parse_mode=ParseMode.MARKDOWN)
    else:
        await msg.reply("Пример выполнения команды:  `/calc 192.168.0.1/24`", parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
    exit(0)
    #  Тут должна быть кнопка типа "Подсети"
    # new_prefix = input('\nВведите префикс: ')
    # subnets(addr, new_prefix)
