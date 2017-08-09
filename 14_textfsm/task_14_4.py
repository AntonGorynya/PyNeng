#! /usr/bin/python3
# -*- coding: utf-8 -*-

import textfsm
import clitable

attributes = {'Command': 'show ip interface brief' , 'Vendor': 'cisco_ios'}
output_sh_ip_route_ospf = open('output/sh_ip_int_br.txt').read()


def parse_command_dynamic(att_dict,output,index_f = 'index',index_dir = 'templates' , show_output= False):
	cli_table = clitable.CliTable(index_f, index_dir)
	cli_table.ParseCmd(output, att_dict)
	
	#print ("CLI Table output:\n", cli_table)
	if show_output:
		print ("Formatted Table:\n", cli_table.FormattedTable())
	
	header = cli_table.header
	
	
	listd = []
	for r in cli_table:
		d = {}
		for i in range(len(header)):
			d.update({header[i]:r[i]})
		listd.append(d)	
	
	return listd
	
	

	
#parse_command_dynamic(attributes,output_sh_ip_route_ospf,show_output= True)