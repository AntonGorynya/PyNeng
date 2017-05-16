#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Задание 11.1

* create_db.py
 + сюда должна быть вынесена функциональность по созданию БД:
  + должна выполняться проверка наличия файла БД
  + если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
    должна быть создана БД (БД отличается от примера в разделе)

В БД теперь будут две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - эта таблица осталась такой же как в примере, за исключением поля switch
  * это поле ссылается на поле hostname в таблице switches

"""
import os
import sqlite3
import sys
import yaml
import re
import datetime




def create_db(db_file='dhcp_snooping.db', schema_filename='dhcp_snooping_schema.sql'):
	db_exists = os.path.exists(db_file)
	with sqlite3.connect(db_file) as conn:
		if not db_exists:
			with open(schema_filename, 'r') as f:
				shema = f.read()
			conn.executescript(shema)
		else:
			print('Database exists')

def add_data_switches(db_file='dhcp_snooping.db', filename = ['switches.yml']):		
	con = sqlite3.connect(db_file)	
	with open(filename[0] , 'r') as f:		
		switches = yaml.load(f)			
	query = " INSERT  into switches (hostname, location) values(?, ?)"
	for pair in switches['switches'].items():		
		try:
			con.execute(query,pair)			
		except sqlite3.IntegrityError as e:
			print("Error:", e)
	con.commit()
	return 0

def add_data(db_file, dhcp_snoop_file):	
	last_active = datetime.datetime.today().replace(microsecond=0)
	regex = re.compile('(?P<mac>.+?) +(?P<ip>.*?) +\d+ +[\w-]+ +(?P<vlan>\d+) +(?P<interface>.*$)')
	con = sqlite3.connect(db_file)	
	current_mac = con.execute('select mac from dhcp').fetchall()
	#print (current_mac)
	with open(dhcp_snoop_file[0], 'r') as f:
		hostname = dhcp_snoop_file[0][:dhcp_snoop_file[0].find("_")]		
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

	
def get_data(db_file='dhcp_snooping.db',key = False, value = False ):	
	keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
	with sqlite3.connect(db_file) as conn:
		#Позволяет далее обращаться к данным в колонках, по имени колонки
		conn.row_factory = sqlite3.Row
		
		if key:
			print ("\nDetailed information for host(s) with", key, value)
			print ('-' * 40)	
			query = "select * from dhcp where {} = ?".format( key )
			result = conn.execute(query, (value,))			
			for row in result:				
				for k in keys:
					print ("{:12}: {}".format(k, row[k]))
				print ('-' * 40)			
	return 0
	
def get_all_data(db_file='dhcp_snooping.db'):
	with sqlite3.connect(db_file) as conn:
	#Позволяет далее обращаться к данным в колонках, по имени колонки	
		conn.row_factory = sqlite3.Row
	print('-' * 60)
	for row in conn.execute("select * from dhcp"):	
		print ("{:12} {:15} {:5} {:16} {:5}".format(row['mac'], row['ip'],row['vlan'],row['interface'],row['switch']))								
	print('-' * 60)	
	for row in conn.execute("select * from switches"):	
		print ("{:7} {:15} ".format(row['hostname'], row['location']))
	print('-' * 60)		

