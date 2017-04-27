#! /usr/bin/python3
# -*- coding: utf-8 -*-

from task_10_3 import parse_cdp_neighbors

def  generate_topology_from_cdp(list_of_files,save_to_file = True,topology_filename ="topology.yaml" ):
	result={}
	for sh_cdp in list_of_files:
		with open(sh_cdp, 'r')as f:
			string = f.read()
			result.update(parse_cdp_neighbors(string))
	if save_to_file:
		with open(topology_filename, 'w') as f:
			f.write(str(result))
	return result


if __name__ == "__main__":
	import glob
	list_of_files = glob.glob('sh_cdp*')
	print(generate_topology_from_cdp(list_of_files,save_to_file = True,topology_filename ="topology.yaml" ))	
	


'''
Структура словаря topology должна быть такой:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}},
 'R5': {'Fa0/1': {'R4': 'Fa0/1'}},
 'R6': {'Fa0/0': {'R4': 'Fa0/2'}}}

Не копировать код функции parse_sh_cdp_neighbors
'''
