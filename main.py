import ipaddress

ip = input('Введите ip: ') # Пользователь вводит ip

list_ip = ip.split('/') # Разделяет вводимый ip на часть с маской, и без
ipv4 = ipaddress.ip_address(list_ip[0])
print('Ваш ip адрес:', ip) # Выводит например "Ваш ip адрес: 192.168.10.128/24"

net = ipaddress.ip_network(ip, strict=False) # В функцию кладётся сетевая часть ip, без хостовой части
print(net)
print(net.netmask)