#! /usr/bin/python3

from sys import argv
import my_func

config_file_name = argv[1]

d_access_trunk = my_func.get_int_vlan_map(config_file_name)
with open("result.txt",'w+') as f:
	f.write("\n".join(my_func.generate_access_config(d_access_trunk["access"]))+'\n')		
	f.write("\n".join(my_func.generate_trunk_config(d_access_trunk["trunk"])))

