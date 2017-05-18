#! /usr/bin/python3
# -*- coding: utf-8 -*-


import netmiko 
import yaml
import getpass
import os

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
	for device_type in device_list.keys():
		for device in device_list[device_type]:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()
			result = str(ssh.send_command(show_command))
			result_dict.update({device['ip']: result})
			#print(result_dict[device['ip']])
		
	return(result_dict)



def send_config_commands(device_list, config_commands, output=True):
	result_dict = {}
	for device_type in device_list.keys():
		for device in device_list[device_type]:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()	
			result = ssh.send_config_set(config_commands)
			
			if result.count('Incomplete command'):
				print ('Error during executing "%s" on %s: Incomplete command' % (config_commands, device['ip']))
			elif result.count('Ambiguous command'):
				print ('Error during executing "%s" on %s: Ambiguous command' % (config_commands, device['ip']))
			elif result.count('Invalid input'):
				print ('Error during executing "%s" on %s: Invalid input' % (config_commands, device['ip']))
			else:
				result_dict.update({device['ip']: result})
				if output:
					print({device['ip']: result})	
	return(result_dict)

def send_commands_from_file(device_list, filename, output=True):
	result_dict = {}
	for device_type in device_list.keys():
		for device in device_list[device_type]:
			ssh = netmiko.ConnectHandler(**device)
			ssh.enable()	
			result = ssh.send_config_from_file(filename)
			
			if result.count('Incomplete command'):
				print ('Error during executing "%s" on %s: Incomplete command in file' % (filename, device['ip']))
			elif result.count('Ambiguous command'):
				print ('Error during executing "%s" on %s: Ambiguous command' % (filename, device['ip']))
			elif result.count('Invalid input'):
				print ('Error during executing "%s" on %s: Invalid input' % (filename, device['ip']))
			else:
				result_dict.update({device['ip']: result})
				if output:
					print({device['ip']: result})		
	return(result_dict)

def send_commands(device_list, config=[], show='', filename=''):
	if config:
		return send_config_commands(device_list, config, output=False)		
	if show:
		return send_show_command(device_list, show)		
	if filename:
		return send_commands_from_file(device_list, filename, output=True)
	
def ping(ip, count):	 
	responce = os.system("ping -c {} ".format(count) + ip)	
	return responce
	
	

	
if __name__ == "__main__":
	for device_type in device_list.keys():
		for device in device_list[device_type]:
			if ping(device['ip'],2) == 0:			
#				print("Config")
#				print(send_commands(device_list,config = commands ))
#				print("Show")
#				print(send_commands(device_list,show = command))
				print("From File")
#				print(send_commands(device_list,filename = 'config.txt' ))	