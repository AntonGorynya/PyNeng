#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Задание 11.1

* add_data.py
 * с помощью этого скрипта, мы будем добавлять данные в БД
  * теперь у нас есть не только данные из вывода sh ip dhcp snooping binding,
    но и информация о коммутаторах

Соответственно, в файле add_data.py у нас будет две части:
* запись информации о коммутаторах в таблицу switches
 + данные о коммутаторах, находятся в файле switches.yml
+ запись информации на основании вывода sh ip dhcp snooping binding
 + теперь у нас есть вывод с трёх коммутаторов:
   + файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 + так как таблица dhcp изменилась, и в ней теперь присутствует поле switch,
   нам нужно его заполнять. Имя коммутатора мы определяем по имени файла с данными

"""

import glob
import sqlite3
import re
import yaml
import os

db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')

db_exists = os.path.exists(db_filename)
regex = re.compile('(?P<mac>.+?) +(?P<ip>.*?) +\d+ +[\w-]+ +(?P<vlan>\d+) +(?P<interface>.*$)')

#dhcp

def add_data_dhcp():
	for dhcp_snoop_file in dhcp_snoop_files:
		hostname = dhcp_snoop_file[:dhcp_snoop_file.find("_")]	
		with open(dhcp_snoop_file, 'r') as f:
			#data = f.read().split('\n')
			data = f.readlines()		
			for line in data:
				if line[2] == ':':
					mac = regex.search(line).group("mac")
					ip = regex.search(line).group("ip")
					vlan = regex.search(line).group("vlan")
					interface = regex.search(line).group("interface")
					query = " INSERT  into dhcp (mac, ip, vlan, interface, switch) values(?, ?, ?, ?, ?)"
					try:
						con.execute(query,tuple([mac,ip,vlan,interface,hostname]))					
					except sqlite3.IntegrityError as e:
						print("Error:", e)

					
#switch

def add_data_switches():
	with open('switches.yml' , 'r') as f:
		switches = yaml.load(f)
	query = " INSERT  into switches (hostname, location) values(?, ?)"
	for pair in switches['switches'].items():
		try:
			con.execute(query,pair)			
		except sqlite3.IntegrityError as e:
			print("Error:", e)


def test():
	if __name__ == "__main__": 	
		for row in con.execute("select * from switches"):
			print ("Row:",row	)	
		for row in con.execute("select * from dhcp"):
			print ("Row:",row)
			
			

if db_exists:
	con = sqlite3.connect(db_filename)	
	add_data_dhcp()
	add_data_switches()
	con.commit()
	test()
			
else:
	print("BD is not exist")

	

 
