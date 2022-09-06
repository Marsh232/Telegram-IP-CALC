import ipaddress

ip = input('Введите ip: ') # Пользователь вводит ip

list_ip = ip.split('/')
ipv4 = ipaddress.ip_address(list_ip[0])
print(ipv4)
net = ipaddress.ip_network('192.168.10.0/24') # В функцию кладётся сетевая часть ip, без хостовой части
print(net.netmask)