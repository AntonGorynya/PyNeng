#! /usr/bin/python3

if __name__ == "__main__":
	from sys import argv
	cdp_n = argv[1]
	with open(cdp_n , 'r') as f:
		string = f.read()

def parse_cdp_neighbors(string):
	d = {}
	hostname = string[:string.find(">")].strip()
	list=string[string.find("Port ID")+8:].split('\n')
	for i in range(len(list)):
		list[i]=list[i].split()			
		if list[i] != []:
			list[i] = [list[i][0],list[i][1]+list[i][2],list[i][-2]+list[i][-1]]		
			d.update( {(hostname,list[i][1]):(list[i][0],list[i][2])})	
			
	return d


if __name__ == "__main__":
	print (parse_cdp_neighbors(string))


	
	
