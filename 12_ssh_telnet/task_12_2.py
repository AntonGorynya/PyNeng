#! /usr/bin/python3
# -*- coding: utf-8 -*-

import netmiko
import yaml



device_list = yaml.load(open('devices.yaml'))

commands = [ 'interface  loopback 0',
             'shutdown']



def send_config_commands(device_list, commands , output= True):	
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
		
	


if __name__ == "__main__":
	for device_type in device_list.keys():				
		send_config_commands(device_list[device_type], commands)
		
		

	