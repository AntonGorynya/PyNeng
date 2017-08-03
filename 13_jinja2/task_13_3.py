#! /usr/bin/python3
# -*- coding: utf-8 -*-


from task_13_1c import generate_cfg_from_template
router_info = 'data_files/ospf.yml'	
template_path = 'templates/ospf.txt'		
print(generate_cfg_from_template(template_path,router_info,  trim_blocks=True, lstrip_blocks=True))