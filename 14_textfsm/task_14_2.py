#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from task_14_1 import parse_output


template = sys.argv[1]
output_file = sys.argv[2]


l_h = parse_output(template,output_file)[0] 
l_p = parse_output(template,output_file)[1]

def list_to_csv ( list_of_header,list_of_parametr, name_out_csv):
	with open(name_out_csv , 'w') as f:
		writer = csv.writer(f)
		#print(list_of_header)
		writer.writerow(list_of_header)
		for row in list_of_parametr:
			writer.writerow(row)
	return 0

	
list_to_csv ( l_h,l_p, "test.csw")

with open('test.csw') as f:	
	print (f.read())