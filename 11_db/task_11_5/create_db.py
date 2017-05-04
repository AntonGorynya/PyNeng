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

db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'

db_exists = os.path.exists(db_filename)

def create_db():
	with sqlite3.connect(db_filename) as conn:
		if not db_exists:
			with open(schema_filename, 'r') as f:
				shema = f.read()
			conn.executescript(shema)
		else:
			print('Database exists')


create_db()		
