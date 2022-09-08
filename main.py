import ipaddress


def main(ip):
    list_ip = ip.split('/')  #  Разделяет вводимый ip на часть с маской, и без
    print('Ваш ip адрес:', ip)  #  Выводит например "Ваш ip адрес: 192.168.10.128/24"

    net = ipaddress.ip_network(ip, strict=False)  #  В функцию кладётся сетевая часть ip, без хостовой части
    print('Маска:', net.netmask, '=', list_ip[1], '\n')  #  Выводит маску
    print('Network:', net)  #  Выводит сеть
    print('Broadcast:', net.broadcast_address)  #  Выводит broad
    print('HostMin:', net[1])
    print('HostMax:', net[-2])
    print('Hosts:', len(list(net.hosts())))  #  Выводит кол-во хостовых ip
    count = 0
    for n_ip in net.hosts():
        count += 1
        if str(n_ip) == list_ip[0]:
            print('№ в сети:', count)  #  Выводит какой ip по счёту в сети
            break


def subnets(ip, prefix):
    subnet = ipaddress.ip_network(ip, strict=False)
    list_subnet = list(subnet.subnets(new_prefix=int(prefix)))
    subnet1 = ipaddress.ip_network(str(list_subnet[1]), strict=False)

    print('\nМаска:', subnet1.netmask, '=', prefix)

    #for i in


if __name__ == '__main__':
    addr = input('Введите ip: ')  #  Пользователь вводит ip
    main(addr)
    #  Тут должна быть кнопка типа "Подсети"
    new_prefix = input('\nВведите префикс: ')
    subnets(addr, new_prefix)