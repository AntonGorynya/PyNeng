#! /usr/bin/python3
# -*- coding: utf-8 -*-

import multiprocessing
import getpass
import netmiko
from task_14_4 import parse_command_dynamic


#with open('ip_list.txt', 'r') as f:
#	ip_list = f.read().rstrip().split('\n')

ip_list = ['192.168.102.226']
show_command = "show ip interface brief"

	
print("Hello!")
#username = input('Username: ')
#password = getpass.getpass('Password: ')
#enable_password = getpass.getpass('Enable password: ')




def create_net_dict(ip_list):
	device_dict = {'cisco':[]}
	for ip in ip_list:
		device_dict['cisco'].append({'ip':ip})
	for device_vendor in device_dict.keys():
		for device in device_dict[device_vendor]:
			device.update({'username':username})
			device.update({'password':password})
			device.update({'secret':enable_password})
			device.update({'device_type':'cisco_ios_telnet'})
			device.update({'global_delay_factor': 3})
	return(device_dict)


def send_show_command(device, show_command, queue):
	try:
		ssh = netmiko.ConnectHandler(**device)
		ssh.enable()
		result = ssh.send_command(show_command)
		print("Connected to {}".format(device['ip']))		
	except:
		print("unable to connect to {}".format(device['ip']))	
	queue.put({device['ip']: result})		


def conn_processes(function, devices, command):
	processes  = []
	queue = multiprocessing.Queue()
	
	for device in devices:
		p = multiprocessing.Process(target = function, args = (device, command, queue))
		p.start()
		processes.append(p)
		
	for p in processes:
		p.join()
		
	result = []
	
	for p in processes:
		result.append(queue.get())
	return result

	

username = 'admin'
password = '12345As'
enable_password = '12345As'

#для подключения
device_dict = create_net_dict(ip_list)
#для parse_command_dynamic
attributes = {'Command': show_command , 'Vendor': 'cisco_ios'}

def send_and_parse_command_parallel(device_dict,show_command):
	
	for device_vendor in device_dict.keys():
		output = conn_processes(send_show_command, device_dict[device_vendor], show_command)
		for i in output[0].keys():	
			output[0][i] = parse_command_dynamic(attributes,output[0][i],show_output= True)
			
	return output[0]	
	
print(send_and_parse_command_parallel(device_dict,show_command))