#! /usr/bin/python3
# -*- coding: utf-8 -*-

from task_10_3b import generate_topology_from_cdp
from draw_network_graph import draw_topology
import copy

if __name__ == "__main__":
	import glob
	list_of_files = glob.glob('sh_cdp*')	
	input = generate_topology_from_cdp(list_of_files,save_to_file = True,topology_filename ="topology.yaml" )
	
def yaml_to_graph(input):	
	dict={}
	for hostname in input.keys():
		#print (hostname)
		for local_int in input[hostname].keys():
			#print(local_int)
			#print (input[hostname][local_int])
			for remote_host in input[hostname][local_int].keys(): 				
				dict.update({(hostname,local_int):(remote_host,input[hostname][local_int][remote_host])})
			
	return dict
	
		
def get_key(d,value):
	for k,v in d.items():
		if v == value:
			return k

cdp_neighbors_dict = yaml_to_graph(input)		
d_copy=copy.deepcopy(cdp_neighbors_dict)
for i,k in enumerate(cdp_neighbors_dict.keys()):	
	for j,v in enumerate(cdp_neighbors_dict.values()):
		if k == v:
			if cdp_neighbors_dict[k] == get_key(cdp_neighbors_dict, v) and j > i:
				del(d_copy[k]) 

		
draw_topology(d_copy)



'''
Задание 10.3c

С помощью функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует описанию в файле topology.yaml

Обратите внимание на то, какой формат данных ожидает функция draw_topology.
Описание топологии из файла topology.yaml нужно преобразовать соответствующим образом,
чтобы использовать функцию draw_topology.

Для решения задания можно создать любые вспомогательные функции.

В итоге, должно быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_10_3c_topology.svg

Не копировать код функции draw_topology.

> Для выполнения этого задания, должен быть установлен graphviz:
> pip install graphviz

'''
