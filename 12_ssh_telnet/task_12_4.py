#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
Задание 12.4

В задании используется пример из раздела про [модуль threading](book/chapter12/5a_threading.md).

Переделать пример таким образом, чтобы:
* вместо функции connect_ssh, использовалась функция send_commands из задания 12.3
 * переделать функцию send_commands, чтобы использовалась очередь и функция conn_threads по-прежнему возвращала словарь с результатами.
 * Проверить работу со списком команд, с командами из файла, с командой show

'''

from netmiko import ConnectHandler
import sys
import yaml
import threading
#import queue
from queue import Queue
import netmiko 
import os


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


def send_config_commands(device_list, config_commands, output=True):
	result_dict = {}
	for device in device_list:
		result =""
		print(device['ip'])
		try:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()		
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
		#return send_config_commands(device_list, config, output=False)	
		queue.put(send_config_commands(device_list, config, output=False))
	if show:
		#return send_show_command(device_list, show)
		queue.put(send_show_command(device_list, show))		
	if filename:
		#return send_commands_from_file(device_list, filename, output=True)
		queue.put(send_commands_from_file(device_list, filename, output=True))

def conn_threads(function, devices, config=[], show='', filename=''):
	threads = []
	q = Queue()
	print("!"*80)	
	print("devices is ",devices)
	print("config is ",config)
	print("show is ",show)
	print("filename is ",filename)
	print("!"*80)
	for device in devices:
		th = threading.Thread(target = function, args = ([device], q ,  config, show, filename))
		th.start()
		threads.append(th)
		
	for th in threads:
		th.join()
	
	
	results = []
	for t in threads:
		#print (t)
		results.append(q.get())

	return results


	

commands = [ 'interface  loopback 0',
             'no shutdown']
			 
command = "sh ip int br"
device_list = yaml.load(open('devices.yaml'))	
	
if __name__ == "__main__":		
#	command = sys.argv[1]
	print("send config command")	
	print (conn_threads(send_commands, device_list['routers'], config = commands))
#	print ('send show command')
#	print (conn_threads(send_commands, device_list['routers'], show = command))
#	print ('send from file')
#	print (conn_threads(send_commands, device_list['routers'], filename = 'config.txt'))
