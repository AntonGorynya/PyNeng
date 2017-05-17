#! /usr/bin/python3
# -*- coding: utf-8 -*-

import netmiko
import yaml



device_list = yaml.load(open('devices3.yaml'))

commands = [ 'interface  loopback 0',
             'shutdown']



def send_config_commands(device_list, commands , output= True):
	for device in device_list.keys():
		ssh = netmiko.ConnectHandler(**device_list[device])
		ssh.enable()
		result = ssh.send_config_set(commands)
		if output:
			print({device_list[device]['ip']: result})
		
	return( {device_list[device]['ip']: result})
	


if __name__ == "__main__":
	send_config_commands(device_list, commands)
		
