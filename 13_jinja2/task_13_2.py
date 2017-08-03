#! /usr/bin/python3
# -*- coding: utf-8 -*-

from task_13_1c import generate_cfg_from_template
router_info = { 'hostname': 'R1' }	
template_path = 'templates/cisco_router_base.txt'		
print(generate_cfg_from_template(template_path,router_info,  trim_blocks=True, lstrip_blocks=True))