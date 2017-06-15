#! /usr/bin/python3
# -*- coding: utf-8 -*-


import netmiko 
import yaml
import getpass
import os
#import scapy
from scapy.all import *


TIMEOUT = 4

device_list = yaml.load(open('devices3.yaml'))
commands = [ 'interface  loopback 0',
             'shutdown']
			 
command = "sh ip int br"

print("Hello!")
username = input('Username: ')
password = getpass.getpass('Password: ')
enable_password = getpass.getpass('Enable password: ')

for device_type in device_list.keys():
	for device in device_list[device_type]:
		device.update({'username':username})
		device.update({'password':password})
		device.update({'secret':enable_password})


def send_show_command(device_list, show_command):
	result_dict = {}
	for device in device_list:
		try:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()
			result = str(ssh.send_command(show_command))
			result_dict.update({device['ip']: result})	
		except:
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
		except:
			print("unable to connect to {}".format(device['ip']))
		
				
		if result.count('Incomplete command'):
			print ('Error during executing "%s" on %s: Incomplete command' % (commands, device['ip']))
		elif result.count('Ambiguous command'):
			print ('Error during executing "%s" on %s: Ambiguous command' % (commands, device['ip']))
		elif result.count('Invalid input'):
			print ('Error during executing "%s" on %s: Invalid input' % (commands, device['ip']))
		else:
			result_dict.update({device['ip']: result})
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
		except:
			print("unable to connect to {}".format(device['ip']))
		
		if result.count('Incomplete command'):
			print ('Error during executing "%s" on %s: Incomplete command' % (commands, device['ip']))
		elif result.count('Ambiguous command'):
			print ('Error during executing "%s" on %s: Ambiguous command' % (commands, device['ip']))
		elif result.count('Invalid input'):
			print ('Error during executing "%s" on %s: Invalid input' % (commands, device['ip']))
		else:
			result_dict.update({device['ip']: result})
	if output:
		print(result_dict)		
	return(result_dict)

def send_commands(device_list, config=[], show='', filename=''):
	if config:
		return send_config_commands(device_list, config, output=False)		
	if show:
		return send_show_command(device_list, show)		
	if filename:
		return send_commands_from_file(device_list, filename, output=True)
	
def ping(ip, count = 2):
	responce = 1
	responce = os.system("ping -c {} ".format(count) + ip)	
	return responce

def ping2(ip):	
	#packet = IP(dst=ip)/ICMP()
	#packet.show()
	#replay = sr(packet, timeout = TIMEOUT)
	#replay.show()
	#if not (replay is None):
	#	print (replay.src," is online")  
	#	return 0
	#else:
	#	print("Timeout waiting for {}".format(packet[IP].dst))
	#	return 1
	
	result = srloop(IP(dst=ip)/ICMP(), count =4)
	
	print ("Result is",result[0])
	
	

if __name__ == "__main__":
	for device_type in device_list.keys():
		print("Config",device_type )
		for device in device_list[device_type]:	
			print("pinging",device['ip'])				
			try:
				if ping(device['ip']) == 0:
					print( send_commands(device_list[device_type],show = command) )	
			except:
				pass
	#		#		print( send_commands(device_list[device_type],show = command) )			

#		print("config")
	#	print(send_commands(device_list[device_type],config = commands ))
	#	print("Show")
	#	print(send_commands(device_list[device_type],show = command))
	#	print("From File")
	#	print(send_commands(device_list[device_type],filename = 'config.txt' ))
	