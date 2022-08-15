#!/usr/bin/python3
from pyhunter import PyHunter
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import csv, argparse, validators, requests, shodan, os, time, socket


print('\n\t'
'-----------------OSINTER--------------------'
'\n'
	)

hunterapi = "" #Enter Hunter.io API Key for hardcoded
shodanapi = "" #Enter Shodan.io API Key for hardcoded

def clear_screen():
	if os.name == 'posix':
		_ = os.system('clear')
	else:
		_ = os.system('cls')


def osinter(dom, filetype, auth_key, shodan_api):
	print("\n-----------------------------------EMAILS-----------------------------------\n")
	global hunterapi
	global shodanapi

	hunter = PyHunter(auth_key)
	shodan_api = shodan.Shodan(shodan_api)
	if(validators.domain(dom) is True):
		emails = hunter.domain_search(dom.lower(), limit=100).get('emails')
		if (filetype.lower() == 'txt'):
			fileName = os.path.join("./{}".format(dom), 'emails.txt')
			with open(fileName,'w') as file:
				for i in range(len(emails)):
					new_res = emails[i].get('value')
					print(new_res)
					file.write(new_res)
					file.write('\n')
		elif (choice1.lower() == 'csv'):
			fileName = os.path.join("./{}".format(dom), 'emails.csv')
			with open(fileName,'w') as file:
				wr = csv.writer(file, dialect='excel')
				for i in range(len(emails)):
					new_res = emails[i].get('value')
					print(new_res)
					wr.writerow(new_res.split('\n'))
		else:
			print("Invalid Selection")
		print("\n-----------------------------------Subdomains-----------------------------------\n")
		
		subdomains = DNSDumpsterAPI().search(dom.lower())
		fileName = os.path.join("./{}".format(dom), 'subdomains.txt')
		with open(fileName,'w') as file:
			for entry in subdomains['dns_records']['host']:
				if (entry['reverse_dns']):
					result = "{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry)
					domain = "{domain}".format(**entry)
					ip_address = "{ip}".format(**entry)
					print(result)
					file.write(domain)
					file.write('\n')
					time.sleep(0.7)
				else:
					result = "{domain} ({ip}) {as} {provider} {country}".format(**entry)
					domain = "{domain}".format(**entry)
					ip_address = "{ip}".format(**entry)
					print(result)
					file.write(domain)
					file.write('\n')
					time.sleep(0.7)
		time.sleep(5)
		print("\n-----------------------------------Wayback Machine-----------------------------------\n")
		
		with open('./{}/subdomains.txt'.format(dom),'r') as file:
			print([requests.get('http://archive.org/wayback/available?url={}'.format(line)).text for line in file.readlines()])

		time.sleep(5)
		print("\n-----------------------------------Shodan-----------------------------------\n")
		
		with open('./{}/subdomains.txt'.format(dom),'r') as file:
			for line in file.readlines():
				try:
					ip_address = socket.gethostbyname(line.strip())
					ipinfo = shodan_api.host(ip_address)
					print("IP: %s" % ipinfo.get('ip_str'))
					print("Country: %s" % ipinfo.get('city','Unknown'))
					print("Hostnames: %s" % ipinfo.get('hostnames'))
					for i in ipinfo['data']:
						print('Port: %s' % i['port'])
				except shodan.APIError:
					pass
	else:
		print("Invalid Domain")


if __name__ == '__main__':
	parser = argparse.ArgumentParser("python3 osinter.py -d <domain> -o <filetype>")
	parser.add_argument('-d', dest='dom', help='Domain name to search', type=str)
	parser.add_argument('-o', dest='filetype', help='Output file type [txt/csv]', default='txt', type=str)
	parser.add_argument('-H', dest='hunterio', help='Hunter.io API Key')
	parser.add_argument('-S', dest='shodanio', help="Shodan.io API Key")
	args=parser.parse_args()
	clear_screen()
	try:
		os.makedirs("./{}".format(args.dom), exist_ok = True)
	except OSError as error:
		print(error)
	osinter(args.dom, args.filetype, args.hunterio, args.shodanio)
	print("\nEnd program...")
