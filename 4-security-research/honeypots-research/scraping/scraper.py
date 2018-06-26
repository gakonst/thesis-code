#!/usr/bin/env python
from __future__ import print_function
import os
import requests
import codecs
from bs4 import BeautifulSoup


ETHERSCAN_URL = 'https://etherscan.io/'

def getPage(sess, *args):
	url = ETHERSCAN_URL + '/'.join(args)
	print("Retrieving", url)
	return BeautifulSoup(sess.get(url).text, 'html.parser')

def getContracts(sess, page=1):
	table = getPage(sess, 'contractsVerified', str(int(page))).find('table')
	headings = [X.text for X in table.find('thead').find_all('th')]
	return [dict(zip(headings, [X.text.strip() for X in row.find_all('td')]))
		    for row in table.find('tbody').find_all('tr')]

def addressPath(addr):
	return '/'.join(['contracts', addr[2:4], addr + '.sol'])

def saveContract(sess, contract):
	page = getPage(sess, 'address', contract['Address']).find('pre')
	path = addressPath(contract['Address'])
	if not os.path.isdir(os.path.dirname(path)):
		os.makedirs(os.path.dirname(path))
	with codecs.open(path, 'w', 'utf-8') as handle:
            try:
		handle.write(page.contents[0])
            except:
                print('Skipping', contract)

def main():
	# Retrieve a list of verified contracts
	base_url = "https://etherscan.io/"
	resp = requests.get(base_url + "contractsVerified")
	sess = requests.Session()

	pageno = 2
	while True:
		pageno += 1
                if pageno==391: break
		for contract in getContracts(sess, pageno):
			saveContract(sess, contract)

if __name__ == "__main__":
	main()


