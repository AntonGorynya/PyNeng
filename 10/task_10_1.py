#! /usr/bin/python3
# -*- coding: utf-8 -*-


'''
Задание 10.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает аргумент output в котором находится вывод команды sh version
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

Функция write_to_csv:

* ожидает два аргумента:
 * имя файла, в который будет записана информация в формате CSV
 * данные в виде списка списков, где:
    * первый список - заголовки столбцов,
    * остальные списки - содержимое
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает

Остальное содержимое скрипта может быть в скрипте, а может быть в ещё одной функции.

Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print sh_version_files, чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import re
import csv
#from os import listdir
import glob

def parse_sh_version(output):	
	output_list = output.split('\n')
	for line in output_list:
		#print(line)
		if line.startswith('Cisco IOS Software'):
			ios = line
		elif line.startswith('System image file'):
			image = line
		elif line.startswith('router uptime'):
			uptime = line
	ios = re.search('Version (?P<ios>.+?) ',ios).group(1)	
	image = re.search('\"(?P<image>.+?)\"',image).group(1)	
	uptime = re.search('is (?P<uptime>.+)',uptime).group(1)			
	return (ios, image, uptime)

def	write_to_csv(data,output_file):
	with open(output_file, 'w') as f:
		writer=csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
		for row in data:
			writer.writerow(row)
	return None

#if __name__ == "__main__":
	#parse_sh_version
	#from sys import argv
	#file_name = argv[1]
	#with open(file_name, 'r') as f:
	#	output=f.read()
	#print(parse_sh_version(output))
	
	#write_to_csv
	#data = [['hostname', 'vendor', 'model', 'location'],
    #    ['sw1', 'Cisco', '3750', 'London, Best str'],
    #    ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
    #    ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
    #   ['sw4', 'Cisco', '3650', 'London, Best str']]
	
	

sh_version_files = glob.glob('sh_vers*')
data=[]
data_out=[['hostname', 'ios', 'image', 'uptime']]
for file in sh_version_files:
	data.append(re.search('_\w+_(.+?)\.',file).group(1))
	with open(file, 'r') as f:	
		output=f.read()
		data.extend(list(parse_sh_version(output)))
		data_out.append(data)
		data = []

write_to_csv(data_out,"output_file.txt")			
