#!/usr/bin/python3

import requests, sys, re, argparse, time, csv

def ip_address(inpt, to_file):
	url = 'https://ipgen.hasarin.com/iprange'
	Headers = {"Te":"trailers", "Content-Type":"application/x-www-form-urlencoded"}
	if ('/' in inpt):
		print('\n-------- Printing from CIDR Notation ---------\n')
		ip = inpt.split('/')
		ipcidr = ip[0]
		mask = ip[1]
		body = 'iprangetype=cidr&ipstart=&ipend=&ipcidr={}&mask={}'.format(ipcidr, mask)

	elif ('-' in inpt):
		print('\n--------- Printing from Range Notation ---------\n')
		time.sleep(2.5)
		ip = inpt.split('-')
		ipstart = ip[0]
		ipend = ip[1]
		body = 'iprangetype=plain&ipstart={}&ipend={}&ipcidr=&mask=32'.format(ipstart, ipend)

	else:
		sys.exit('Usage: python3 ip_address.py')


	x = requests.post(url,body,headers=Headers)

	cleanr = re.compile('<.*?>')

	cleantext = re.sub(cleanr, '', x.text)

	ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', cleantext )

	new_ip = '\n'.join(ip)

	if to_file:
		with open(to_file,'a') as file:
			file.write(new_ip+'\n')
			file.close()
	else:
		print(new_ip)

def client_file(inpt):
	try:
		ip_f = (inpt.replace(' ','').split('-')[1:])
		first_ip = ip_f[0]
		last_half = ip_f[1]
		if '/' in last_half:
			octet = ip_f[1].split('/')[1]
			result = (first_ip + '/' + octet).strip()
			return result
		elif '/' not in last_half:
			new_ip = ip_f[0].split('.')[:3]
			last_ip = ('.'.join(new_ip) + '.' + last_half)
			result = (first_ip + '-' + last_ip).strip()							
			return(result)
	except:
		pass
	try:
		return inpt.strip()
	except:
		pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser('Usage: python3 ip_address.py')
	required = parser.add_argument_group("Required")
	optional = parser.add_argument_group("Optional")
	required.add_argument('-i', dest='input', nargs='+', help='IP Address[es] or File in CIDR Notation or Range Notation', required=True)
	optional.add_argument('-o', dest='output', help='Output to file [txt]', default='stdout')
	args=parser.parse_args()
	for items in args.input:
		if '.txt' in items:
			with open(items, 'r') as file:
				f = file.readlines()
				for lines in f:
					clients = client_file(lines)
					ip_address(clients, args.output)
		elif '.csv' in items:
			with open(items,'r',encoding='utf-8-sig') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for row in csv_reader:
					ip = ', '.join(row).strip()
					clients = client_file(ip)
					ip_address(clients, args.output)
		else:
			ip_address(items,args.output)
	

	print('\nEnd Program')
		
