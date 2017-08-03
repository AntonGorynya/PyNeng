#! /usr/bin/python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import importlib
import yaml
import sys
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

TEMPLATE_DIR, template = sys.argv[1].split('/')
VARS_FILE = sys.argv[2]


env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
template = env.get_template(template)

vars_dict = yaml.load( open( VARS_FILE ) )

print (template.render( vars_dict ))