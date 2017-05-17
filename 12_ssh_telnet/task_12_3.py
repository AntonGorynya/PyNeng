#! /usr/bin/python3
# -*- coding: utf-8 -*-


import netmiko 
import yaml

device_list = yaml.load(open('devices3.yaml'))
commands = [ 'interface  loopback 0',
             'shutdown']
			 
command = "sh ip int br"




def send_show_command(device_list, show_command):
	result_dict = {}
	for device in device_list.keys():
		ssh = netmiko.ConnectHandler(**device_list[device])
		ssh.enable()
		result = str(ssh.send_command(show_command))
		result_dict.update({device_list[device]['ip']: result})
		#print(result_dict[device_list[device]['ip']])
		
	return(result_dict)



def send_config_commands(device_list, config_commands, output=True):
	result_dict = {}
	for device in device_list.keys():
		ssh = netmiko.ConnectHandler(**device_list[device])
		ssh.enable()	
		result = ssh.send_config_set(config_commands)
		
		if result.count('Incomplete command'):
			print ('Error during executing "%s" on %s: Incomplete command' % (config_commands, device_list[device]['ip']))
		elif result.count('Ambiguous command'):
			print ('Error during executing "%s" on %s: Ambiguous command' % (config_commands, device_list[device]['ip']))
		elif result.count('Invalid input'):
			print ('Error during executing "%s" on %s: Invalid input' % (config_commands, device_list[device]['ip']))
		else:
			result_dict.update({device_list[device]['ip']: result})
			if output:
				print({device_list[device]['ip']: result})	
	return(result_dict)

def send_commands_from_file(device_list, filename, output=True):
	result_dict = {}
	for device in device_list.keys():
		ssh = netmiko.ConnectHandler(**device_list[device])
		ssh.enable()	
		result = ssh.send_config_from_file(filename)
		
		if result.count('Incomplete command'):
			print ('Error during executing "%s" on %s: Incomplete command in file' % (filename, device_list[device]['ip']))
		elif result.count('Ambiguous command'):
			print ('Error during executing "%s" on %s: Ambiguous command' % (filename, device_list[device]['ip']))
		elif result.count('Invalid input'):
			print ('Error during executing "%s" on %s: Invalid input' % (filename, device_list[device]['ip']))
		else:
			result_dict.update({device_list[device]['ip']: result})
			if output:
				print({device_list[device]['ip']: result})		
	return(result_dict)

def send_commands(device_list, config=[], show='', filename=''):
	if config:
		return send_config_commands(device_list, config, output=False)		
	if show:
		return send_show_command(device_list, show)		
	if filename:
		return send_commands_from_file(device_list, filename, output=True)
	
		

if __name__ == "__main__":
#	print("Config")
#	print(send_commands(device_list,config = commands ))
#	print("Show")
#	print(send_commands(device_list,show = command))
	print("From File")
	print(send_commands(device_list,filename = 'config.txt' ))
	