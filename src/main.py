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
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from utils import Config, FSMachine, FSMContext

storage = MemoryStorage()

config = Config("config.json")
log = logging.getLogger("Bot")
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)

network_button = KeyboardButton('🧮Сеть🧮')
subnet_button = KeyboardButton('🕸Подсети🕸')
cancel_button = KeyboardButton('❌Отмена❌')
more_button = KeyboardButton('📝Прочее📝')

start_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
start_buttons.row(network_button, subnet_button)
start_buttons.add(more_button).add(cancel_button)


def calc_net(_ip):
    splt = _ip.split('/')  # Разделяет вводимый ip на часть с маской, и без
    if len(splt) == 1:
        splt.append("24")

    ip, mask = splt
    addr = ip + "/" + mask

    internet = ''
    ipv4 = ipaddress.ip_address(ip)
    if ipv4.is_global: internet = 'Public network'
    else: internet = 'Private network'
    net = ipaddress.ip_network(addr, strict=False)  # В функцию кладётся сетевая часть ip, без хостовой части
    dict_out = {
        "addr": addr,
        "mask": f"{net.netmask} - {mask}",  # Выводит маску
        "net": f"{net}",  # Выводит сеть
        "broadcast": f'{net.broadcast_address}',  # Выводит broadcast
        "min": f"{net[1]}",
        "max": f"{net[-2]}",
        "hosts": f"{len(list(net.hosts()))}",
        "num": None,
        "network": f"{internet}"
    }

    count = 0
    for n_ip in net.hosts():
        count += 1
        if str(n_ip) == ip:
            dict_out["num"] = count  # Выводит какой ip по счёту в сети

    return dict_out


@dp.message_handler(commands=["start"], state=None, chat_type=ChatType.PRIVATE)
async def start(msg: types.Message):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await msg.reply(f"Привет {msg.from_user.username}😀, я IP Bot🤖, я могу посчитать🧮 ip и не только.", reply_markup=start_buttons)


@dp.message_handler(lambda msg: msg.text.lower().startswith('❌отмена❌'), state="*")
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Ок🥸')


@dp.message_handler(lambda msg: msg.text.lower().startswith('📝прочее📝'))
async def more_handler(msg: types.Message, state: FSMContext):
    await msg.reply(f"📄Все идеи и предложения писать -> @ilassik📄\n"
                    f"💸Донаты -> www.donationalerts.com/r/ilassik💸",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=start_buttons)


@dp.message_handler(lambda msg: msg.text.lower().startswith('🧮сеть🧮'))
async def calcnet(msg: types.Message, state: FSMContext):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await FSMachine.network.set()
    await msg.reply("Введите ip")


@dp.message_handler(state=FSMachine.network, chat_type=ChatType.PRIVATE)
async def calcnet1(msg: types.Message, state: FSMContext):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    text = msg.text
    c = calc_net(text)
    await msg.reply(f"Вводимые данные: `{c['addr']}`\n"
                    f"Маска: `{c['mask']}`\n"
                    f"Сеть: `{c['net']}`\n"
                    f"Broadcast: `{c['broadcast']}`\n"
                    f"Мин адрес: `{c['min']}`\n"
                    f"Макс адрес: `{c['max']}`\n"
                    f"Всего адресов: `{c['hosts']}`\n"
                    f"Номер в сети: `{c['num']}`",
                    f"`{c['network']}`",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=start_buttons)
    await state.finish()


@dp.message_handler(lambda msg: msg.text.lower().startswith('🕸подсети🕸'))
async def calcsub(msg: types.Message, state: FSMContext):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    await FSMachine.subnetwork.set()
    await msg.reply("**Введите ip с увеличенной маской**\n"
                    "**Пример -> 10.10.10.10/24 26**")


@dp.message_handler(state=FSMachine.subnetwork, chat_type=ChatType.PRIVATE)
async def calcsub1(msg: types.Message, state: FSMContext):
    log.info(f"New message from {msg.from_user.id}(@{msg.from_user.username}) in {msg.chat.id}: '{msg.text}'")
    text = msg.text
    splt = text.split(" ")
    if len(splt) > 1:
        try:
            ip = splt[0]
            prefix = splt[1]
            subnet = ipaddress.ip_network(ip, strict=False)
            list_subnet = list(subnet.subnets(new_prefix=int(prefix)))
            subnet1 = ipaddress.ip_network(str(list_subnet[1]), strict=False)
            ip4 = ip.split('/')
            ipv = ip4[0]
            inter = ' '
            ipv4 = ipaddress.ip_address(ipv)
            if ipv4.is_global:
                inter = 'Public network'
            else:
                inter = 'Private network'

            await msg.reply(f"Маска: {subnet1.netmask} = {prefix}")

            for i in list_subnet:
                subnet2 = ipaddress.ip_network(i, strict=False)
                await msg.reply(f"Network: `{subnet2}`\n"
                                f"Broadcast: `{subnet2.broadcast_address}`\n"
                                f"HostMin: `{subnet2[1]}`\n"
                                f"HostMax: `{subnet2[-2]}`\n"
                                f"Hosts: `{len(list((subnet2.hosts())))}`",
                                f"`{inter}`",
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=start_buttons)
                await state.finish()
        except IndexError:
            await msg.reply("**😡Вы ввели неправильно**😡\n"
                            "**🤓Попробуйте ещё раз🤓**",
                            parse_mode=ParseMode.MARKDOWN)
    else:
        await msg.reply("**😡ВЫ ввели неправильно**😡\n"
                        "🤓Пример ввода: ` 192.168.0.1/24 26`🤓",
                        parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
