#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию send_show_command.

Функция подключается по SSH (с помощью netmiko) к устройствам из списка,
и выполняет  команду на основании переданных аргументов:
* devices_list - список словарей с параметрами подключения к устройствам,
  которым надо передать команды
* command - команда, которую надо выполнить

Функция возвращает словарь с результатами выполнения команды:
* ключ - IP устройства
* значение - результат выполнения команды

Проверить работу функции на примере:
* устройств из файла devices.yaml (для этого надо считать информацию из файла)
* и команды command

'''

import netmiko
import yaml
import sys

command = sys.argv[1]
device_list = yaml.load(open('devices.yaml'))


def send_show_command(device, command):	
	ssh = netmiko.ConnectHandler(**device)
	ssh.enable()
	result = ssh.send_command(command)
	return( {device['ip']: result})
	


if __name__ == "__main__":
	for device_type in device_list.keys():
		for device in device_list[device_type]:	
			print(device['ip'])
			try:
				print(send_show_command(device, command))
			except:
				print("unable to connect")
