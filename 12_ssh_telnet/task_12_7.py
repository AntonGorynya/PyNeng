#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Задание 12.6

В задании используется пример из раздела про [модуль multiprocessing](book/chapter12/5b_multiprocessing.md).

Переделать пример таким образом, чтобы:
* вместо функции connect_ssh, использовалась функция send_commands из задания 12.3
 * переделать функцию send_commands, чтобы использовалась очередь и функция conn_processes по-прежнему возвращала словарь с результатами.
 * Проверить работу со списком команд, с командами из файла, с командой show


Пример из раздела:
"""
from netmiko import ConnectHandler
import sys
import yaml
import threading
#import queue
from queue import Queue
import netmiko 
import multiprocessing



COMMAND = sys.argv[1]
devices = yaml.load(open('devices.yaml'))
print(COMMAND)

def send_show_command(device_list, show_command):
	result_dict = {}
	for device in device_list:
		try:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()
			result = str(ssh.send_command(show_command))
			result_dict.update({device['ip']: result})	
			print("Connected to {}".format(device['ip']))
		except:
			result_dict.update({device['ip']: ""})
			print("unable to connect to {}".format(device['ip']))	
		
	return(result_dict)


def send_config_commands(device_list, commands, output=True):
	result_dict = {}
	for device in device_list:
		result =""
		print("connecting to ", device['ip'])
		try:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()
			print("sending commands {} to".format(commands[0]), device['ip'])
			
			result = ssh.send_config_set(commands)
			print("Connected to {}".format(device['ip']))				
			if result.count('Incomplete command'):
				print ('Error during executing "%s" on %s: Incomplete command' % (commands, device['ip']))
			elif result.count('Ambiguous command'):
				print ('Error during executing "%s" on %s: Ambiguous command' % (commands, device['ip']))
			elif result.count('Invalid input'):
				print ('Error during executing "%s" on %s: Invalid input' % (commands, device['ip']))
			else:
				result_dict.update({device['ip']: result})	
			print("command send successeful for {}".format(device['ip']))		
		except:
			result_dict.update({device['ip']: result})
			print("unable to connect to {}".format(device['ip']))
	if output:
		print(result_dict)	
		
	return(result_dict)

def send_commands_from_file(device_list, filename, output=True):
	result_dict = {}
	for device in device_list:
		result =""
		print(device['ip'])
		try:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()		
			result = ssh.send_config_from_file(filename)
			print("Connected to {}".format(device['ip']))		
			if result.count('Incomplete command'):
				print ('Error during executing "%s" on %s: Incomplete command' % (commands, device['ip']))
			elif result.count('Ambiguous command'):
				print ('Error during executing "%s" on %s: Ambiguous command' % (commands, device['ip']))
			elif result.count('Invalid input'):
				print ('Error during executing "%s" on %s: Invalid input' % (commands, device['ip']))
			else:
				result_dict.update({device['ip']: result})
		except:
			result_dict.update({device['ip']: result})
			print("unable to connect to {}".format(device['ip']))
	if output:
		print(result_dict)		
	return(result_dict)

def send_commands(device_list, queue, config=[], show='', filename='' ):
		
	if config:
		#print("config command is",config)
		#return send_config_commands(device_list, config, output=False)	
		queue.put(send_config_commands(device_list, config, output=False))
	if show:
		#print("show command is",show)
		#return send_show_command(device_list, show)
		queue.put(send_show_command(device_list, show))		
	if filename:
		#print("filename command is",filename)
		#return send_commands_from_file(device_list, filename, output=True)
		queue.put(send_commands_from_file(device_list, filename, output=True))


def conn_processes(function, devices, command , limit = 2):
	processes = []
	queue = multiprocessing.Queue()
	results = []
	w_min = 0	
	while True:
		print("new round")

		for device in devices[w_min:min(w_min+limit,len(devices))]:
			p = multiprocessing.Process(target = function, args = ([device],queue, [command] ))
			p.start()
			processes.append(p)

		for p in processes:
			p.join()  
	
		for p in processes:
			results.append(queue.get())
			
		print("Round end ")
		processes = []
		
		if w_min+limit <=  len(devices)  :
			w_min = w_min+limit
	
		else:
			break

	return results

print( conn_processes(send_commands, devices['routers'], COMMAND) )
