#!/usr/bin/python3
from pyhunter import PyHunter
import validators
import csv

auth_key = input("Enter API Key: ")
hunter = PyHunter(auth_key)

dom = input('Enter domain to search: ')
if(validators.domain(dom) is True):
	results = hunter.domain_search(dom.lower(), limit=100).get('emails')
	choice1 = input("Output as [txt,csv]: ")
	if (choice1.lower() == 'txt'):
		with open(dom+'.txt','w') as file:
			for i in range(len(results)):
				new_res = results[i].get('value')
				file.write(new_res)
				file.write('\n')
	elif (choice1.lower() == 'csv'):
		with open(dom+'.csv','w') as file:
			wr = csv.writer(file, dialect='excel')
			for i in range(len(results)):
				new_res = results[i].get('value')
				wr.writerow(new_res.split('\n'))
	else:
		print("Invalid Selection")
else:
	print("Invalid Domain")

