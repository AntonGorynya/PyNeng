#! /usr/bin/python3
# -*- coding: utf-8 -*-
'''
Задание 2

Создать функции:
- generate_access_config - генерирует конфигурацию для access-портов,
                           на основе словарей access и psecurity из файла sw_templates.yaml
- generate_trunk_config - генерирует конфигурацию для trunk-портов,
                           на основе словаря trunk из файла sw_templates.yaml
- generate_ospf_config - генерирует конфигурацию ospf, на основе словаря ospf из файла templates.yaml
- generate_mngmt_config - генерирует конфигурацию менеджмент настроек, на основе словаря mngmt из файла templates.yaml
- generate_alias_config - генерирует конфигурацию alias, на основе словаря alias из файла templates.yaml
- generate_switch_config - генерирует конфигурацию коммутатора, в зависимости от переданных параметров,
                           использует для этого остальные функции
'''
import yaml

yaml_template = 'templates.yaml'

access_dict = { 'FastEthernet0/12':10,
                'FastEthernet0/14':11,
                'FastEthernet0/16':17,
                'FastEthernet0/17':150 }

trunk_dict = { 'FastEthernet0/1':[10,20,30],
               'FastEthernet0/2':[11,30],
               'FastEthernet0/4':[17] }


def generate_access_config(access, psecurity=False):
	templates = yaml.load(open('sw_templates.yaml'))
	result = ""
	for interface in access.keys():
		result += str('interface ' + interface+ '\n')		
		for command in templates['access']:
			if command.startswith('switchport access vlan'):
				result += (command + ' ' + str(access[interface]) +'\n')				
			else:
				result += (command+'\n')
			if psecurity:
				for command in templates['psecurity']:
					result += (command+'\n')
	return result	
	

#print(generate_access_config(access_dict, psecurity=False))		
	
def generate_trunk_config(trunk):
	templates = yaml.load(open('sw_templates.yaml'))
	result = ""
	for interface in trunk.keys():
		result += str('interface ' + interface+ '\n')
		for command in templates['trunk']:
			if command.startswith('switchport trunk allowed vlan'):				
				result += (command + ' ' + ",".join(str(e) for e in  trunk[interface]) +'\n')
			else:
				result += (command+'\n')
	return result
	
#print(generate_trunk_config(trunk_dict))

def generate_ospf_config(filename):
	templates = yaml.load(open(filename))
	result = ""
	for command in templates['ospf']:
		result += (command+'\n')
	return result

#print(generate_ospf_config("templates.yaml"))

def generate_mngmt_config(filename):
	templates = yaml.load(open(filename))
	result = ""
	for command in templates['mngmt']:
		result += (command+'\n')
	return result
	

def generate_alias_config(filename):
	templates = yaml.load(open(filename))
	result = ""
	for command in templates['alias']:
		result += (command+'\n')
	return result

def generate_switch_config(access=True, psecurity=False, trunk=True,ospf=True, mngmt=True, alias=False):
	result =""
	if (access and psecurity):
		result += generate_access_config(access_dict, psecurity=True)
	if (access and (psecurity == False)):
		result += generate_access_config(access_dict, psecurity=False)
	if trunk:
		result += generate_trunk_config(trunk_dict)
	if ospf:
		result += generate_ospf_config("templates.yaml")
	if mngmt:
		result += generate_mngmt_config("templates.yaml")
	if alias:
		result += generate_alias_config("templates.yaml")
	return result


# Сгенерировать конфигурации для разных коммутаторов:

sw1 = generate_switch_config()
sw2 = generate_switch_config(psecurity=True, alias=True)
sw3 = generate_switch_config(ospf=False)



