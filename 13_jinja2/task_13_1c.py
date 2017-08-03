#! /usr/bin/python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import importlib
import yaml
import json
import sys
import os







def generate_cfg_from_template(template_path,VARS_FILE, **kwargs):
	TEMPLATE_DIR = template_path[:template_path.rfind('/')]
	template = template_path[template_path.rfind('/')+1::]
	
	env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), **kwargs)
	template = env.get_template(template)
			
#	elif type(data_dict) is dict:
	if type(VARS_FILE) is dict:
		vars_dict = VARS_FILE
		return template.render( vars_dict )	
	elif VARS_FILE[VARS_FILE.rfind('.')+1::] == 'yml' or VARS_FILE[VARS_FILE.rfind('.')+1::] == 'yaml':
		vars_dict = yaml.load( open( VARS_FILE ) )	
		return template.render( vars_dict )
	elif VARS_FILE[VARS_FILE.rfind('.')+1::] == 'json':
		vars_dict = json.load( open( VARS_FILE ) )	
		return template.render( vars_dict )
	else:
		print("Error")
		return None
		
	
if __name__ == "__main__":

	data_dict = {'vlans': {
						10: 'Marketing',
						20: 'Voice',
						30: 'Management'},
			'ospf': [{'network': '10.0.1.0 0.0.0.255', 'area': 0},
						{'network': '10.0.2.0 0.0.0.255', 'area': 2},
						{'network': '10.1.1.0 0.0.0.255', 'area': 0}],
			'id': 3,
			'name': 'R3'}



	template = sys.argv[1]
	VARS_FILE = sys.argv[2]
	TEMPLATE_DIR = os.getcwd() 
	if template.rfind('/') >= 0:	
		TEMPLATE_DIR = TEMPLATE_DIR +'/' + template[:template.rfind('/')]
		template= template[template.rfind('/')+1::]	
	template_path = TEMPLATE_DIR +'/' + template	
	print(generate_cfg_from_template(template_path,VARS_FILE,  trim_blocks=True, lstrip_blocks=True))