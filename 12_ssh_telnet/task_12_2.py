#! /usr/bin/python3
# -*- coding: utf-8 -*-

import netmiko
import yaml



device_list = yaml.load(open('devices3.yaml'))

commands = [ 'interface  loopback 0',
             'shutdown']



def send_config_commands(device_list, commands , output= True):
	result_dict = {}
	for device in device_list.keys():
		ssh = netmiko.ConnectHandler(**device_list[device])
		ssh.enable()	
		result = ssh.send_config_set(commands)
		
		if result.count('Incomplete command'):
			print ('Error during executing "%s" on %s: Incomplete command' % (commands, device_list[device]['ip']))
		elif result.count('Ambiguous command'):
			print ('Error during executing "%s" on %s: Ambiguous command' % (commands, device_list[device]['ip']))
		elif result.count('Invalid input'):
			print ('Error during executing "%s" on %s: Invalid input' % (commands, device_list[device]['ip']))
		else:
			result_dict.update({device_list[device]['ip']: result})
			if output:
				print({device_list[device]['ip']: result})	
		
	return(result_dict)
		
	


if __name__ == "__main__":
	send_config_commands(device_list, commands)
		
