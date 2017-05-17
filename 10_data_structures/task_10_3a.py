#! /usr/bin/python3
# -*- coding: utf-8 -*-

import glob
from task_10_3 import parse_cdp_neighbors

sh_cdp_files = glob.glob('sh_cdp*')

result={}
for sh_cdp in sh_cdp_files:
	with open(sh_cdp, 'r')as f:
		string = f.read()
		result.update(parse_cdp_neighbors(string))
with open("topology.yaml", 'w') as f:
	f.write(str(result))


	
	

'''
Структура словаря topology должна быть такой:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}},
 'R5': {'Fa0/1': {'R4': 'Fa0/1'}},
 'R6': {'Fa0/0': {'R4': 'Fa0/2'}}}

Не копировать код функции parse_sh_cdp_neighbors
'''
