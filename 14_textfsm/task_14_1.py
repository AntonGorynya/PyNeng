#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import textfsm
from tabulate import tabulate

template = sys.argv[1]
output_file = sys.argv[2]

def  parse_output(template, output_file):

	f = open(template)
	output = open(output_file).read()

	re_table = textfsm.TextFSM(f)

	header = re_table.header
	result = re_table.ParseText(output)

	return [header ,result]
	
print(parse_output(template, output_file))