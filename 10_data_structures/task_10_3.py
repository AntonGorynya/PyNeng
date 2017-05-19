#! /usr/bin/python3

if __name__ == "__main__":
	from sys import argv
	cdp_n = argv[1]
	with open(cdp_n , 'r') as f:
		string = f.read()

def parse_cdp_neighbors(string):
	d = {}
	hostname = string[:string.find(">" or "#")].strip()	
	raw_list=string[string.find("Port ID")+8:].split('\n')	
	
	#исправление бага если слишком длинный hostname		
	for i in range(len(raw_list)):
		raw_list[i]=raw_list[i].split()				
		if len(raw_list[i]) == 1:
			raw_list[i].extend(raw_list[i+1].split())			
			raw_list[i+1] = "\n"
		
	for i in range(len(raw_list)):		
	#	print(raw_list[i]," ",len(raw_list[i]), "\n")		
		if raw_list[i] != []:
			raw_list[i] = [raw_list[i][0],raw_list[i][1]+raw_list[i][2],raw_list[i][-2]+raw_list[i][-1]]		
			d.update( {(raw_list[i][1]):{raw_list[i][0]:raw_list[i][2]}})	
	d ={hostname:d}
			
	return d


if __name__ == "__main__":
	print (parse_cdp_neighbors(string))


	
	
