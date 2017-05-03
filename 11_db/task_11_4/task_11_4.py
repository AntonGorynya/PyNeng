#! /usr/bin/python3
# -*- coding: utf-8 -*-

'''
Это копия скрипта get_data_ver1.py из раздела
'''

import sqlite3
import sys

db_filename = 'dhcp_snooping.db'
keys = ['mac', 'ip', 'vlan', 'interface', 'switch','active']

#active

		
def out(db_filename,key = False, value = False ):
	with sqlite3.connect(db_filename) as conn:
		#Позволяет далее обращаться к данным в колонках, по имени колонки
		conn.row_factory = sqlite3.Row
		#conn.execute("SELECT * from dhcp ORDER BY active DESC ")
		if key:
			print ("\nDetailed information for host(s) with", key, value)
			print ('-' * 40)	
			query = "SELECT * from dhcp where {} = ? ORDER BY active DESC".format( key )
			result = conn.execute(query, (value,))			
			for row in result:					
				for k in keys:
					print ("{:12}: {}".format(k, row[k]))
				print ('-' * 40)
		else:
			print('-' * 60)
			for row in conn.execute("SELECT * from dhcp ORDER BY active DESC"):	
				print ("{:12} {:15} {:5} {:16} {:6} {:2}".format(row['mac'], row['ip'],row['vlan'],row['interface'],row['switch'], row['active']))							
			print('-' * 60)				
			
	return 0
	
if sys.argv[2:]:
	key, value = sys.argv[1:]	
	flag = False
	for k in keys:
		if k == key:
			keys.remove(key)
			out(db_filename,key, value)
			flag = True
	if not flag:
		print("Key must be in range ", keys)
elif sys.argv[1:]: 
	print("0 or 2 arguments")
else:
	out(db_filename)	