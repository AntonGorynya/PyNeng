# 7_1a
def generate_access_config(access_dict, psecurity = False):
	list = []
	for i in access_dict.keys():
		list.append(i)
		for j in access_template:
			if j.endswith('access vlan'):
				list.append(j+" "+ str(access_dict[i]) )
				
			else:
				list.append(j)
		if psecurity:
			list.extend(port_security)
	return list

access_template = ['switchport mode access',
		'switchport access vlan',
		'switchport nonegotiate',
		'spanning-tree portfast',
		'spanning-tree bpduguard enable']
port_security = ['switchport port-security maximum 2',
			'switchport port-security violation restrict',
			'switchport port-security']	
	
# 7_2	
def generate_trunk_config(trunk_dict):
	d = []
	for i in trunk_dict.keys():		
		int_commands=[i]
		for j in trunk_template:
			if j.endswith('allowed vlan'):
				int_commands.append(j+" "+ str(trunk_dict[i])[1:-1])
			else:
				int_commands.append(j)
		d.extend(int_commands)
	return (d)
# 7_2a
def generate_trunk_config_d(trunk_dict):
	d = {}
	for i in trunk_dict.keys():	
		int_commands =[]		
		for j in trunk_template:
			if j.endswith('allowed vlan'):
				int_commands.append(j+" "+ str(trunk_dict[i])[1:-1])
			else:
				int_commands.append(j)
		d.update(dict({i: int_commands}))
	return (d)

trunk_template = ['switchport trunk encapsulation dot1q',
				'switchport mode trunk',
				'switchport trunk native vlan 999',
				'switchport trunk allowed vlan']	
# 7_3a

def get_int_vlan_map(config_file_name):
	d_access = {}
	d_trunk = {}
	with open(config_file_name, 'r') as f:
		for command in f:		
			vlans =[]
			if command.startswith('interface'):
				key_t = command.rstrip()
				vlan_found = False			
			if command.startswith(' switchport mode access') and (vlan_found == False):
				d_access.update({key_t: "1"})			
			if command.startswith(' switchport access vlan'):			
				d_access.update({key_t: command.split()[-1]})
				vlan_found = True
			if command.startswith(' switchport trunk allowed'):
				vlans = command.split()
				d_trunk.update({key_t: vlans[vlans.index('vlan')+1:]})				
	return ({"access":d_access , "trunk":d_trunk})	
	