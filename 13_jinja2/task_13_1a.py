#! /usr/bin/python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import importlib
import yaml
import sys
import os
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

template = sys.argv[1]
VARS_FILE = sys.argv[2]
TEMPLATE_DIR = os.getcwd() 

if template.rfind('/') >= 0:	
	TEMPLATE_DIR = TEMPLATE_DIR +'/' + template[:template.rfind('/')]
	template= template[template.rfind('/')+1::]
	


def generate_cfg_from_template(TEMPLATE_DIR,template,VARS_FILE):
	env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
	template = env.get_template(template)
	vars_dict = yaml.load( open( VARS_FILE ) )	
	return template.render( vars_dict )
	
print(generate_cfg_from_template(TEMPLATE_DIR,template,VARS_FILE))