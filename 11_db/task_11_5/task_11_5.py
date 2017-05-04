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
import datetime


db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
db_exists = os.path.exists(db_filename)



def add_data_switches(filename = 'switches.yml'):
	con = sqlite3.connect(db_filename)	
	with open(filename , 'r') as f:
		switches = yaml.load(f)
	query = " INSERT  into switches (hostname, location) values(?, ?)"
	for pair in switches['switches'].items():
		try:
			con.execute(query,pair)			
		except sqlite3.IntegrityError as e:
			print("Error:", e)
	con.commit()

	
def add_data_dhcp(dhcp_snoop_file):
	regex = re.compile('(?P<mac>.+?) +(?P<ip>.*?) +\d+ +[\w-]+ +(?P<vlan>\d+) +(?P<interface>.*$)')
	con = sqlite3.connect(db_filename)	
	current_mac = con.execute('select mac from dhcp').fetchall()
	#print (current_mac)
	with open(dhcp_snoop_file, 'r') as f:
		#data = f.read().split('\n')
		data = f.readlines()		
		for line in data:
			if line[2] == ':':				
				mac = regex.search(line).group("mac")
				ip = regex.search(line).group("ip")
				vlan = regex.search(line).group("vlan")
				interface = regex.search(line).group("interface")					
				
				#кортеж из 1 элемента
				if (mac, ) in current_mac:					
					query = "UPDATE  dhcp set active = 0 where mac = '{}' ".format(mac)	
					#query = "UPDATE  dhcp set last_active = '{}'  ".format(week_ago)					
					con.execute(query)
					
					row = con.execute(("select * from dhcp where mac = '{}' ").format(mac)).fetchall() 	
					
					if (ip != row[0][1]) or (vlan != row[0][2]) or (interface != row[0][3]) :
						#print (ip,vlan,interface,hostname) 
						#print (row[0][1],row[0][2],row[0][3],row[0][4])
						query = " REPLACE  into dhcp (mac, ip, vlan, interface, switch, active, last_active) values(?, ?, ?, ?, ?, 1, ?)"											
						con.execute(query,tuple([mac,ip,vlan,interface,hostname,last_active]))					
				else:
					#its work
					query = " INSERT  into dhcp (mac, ip, vlan, interface, switch, active, last_active) values(?, ?, ?, ?, ?, 1, ?)"											
					con.execute(query,tuple([mac,ip,vlan,interface,hostname,last_active]))					
					
	con.commit()
			


	

def del_old():
		
	con = sqlite3.connect(db_filename)
	#Позволяет далее обращаться к данным в колонках, по имени колонки
	con.row_factory = sqlite3.Row
	for row in con.execute("SELECT * from dhcp"):		
		if (week_ago > datetime.datetime.strptime(row['last_active'], "%Y-%m-%d %H:%M:%S") ):
			query = "DELETE from dhcp where last_active = '{}'".format(row['last_active'])
			con.execute(query)
			print("Row deleted")
	con.commit()
		

			
			
def test():
	con = sqlite3.connect(db_filename)
	if __name__ == "__main__": 				
		#for row in con.execute("select * from switches"):
		#	print ("Row:",row	)	
		for row in con.execute("select * from dhcp"):
			print ("Row:",row)
		

	
			
if db_exists:	
	for dhcp_snoop_file in dhcp_snoop_files:
		hostname = dhcp_snoop_file[:dhcp_snoop_file.find("_")]	
		last_active = datetime.datetime.today().replace(microsecond=0)	
		week_ago = last_active - datetime.timedelta(days = 7)
		
		del_old()
		add_data_dhcp(dhcp_snoop_file)
		

	test()		
else:
	print("BD is not exist")

	

 
