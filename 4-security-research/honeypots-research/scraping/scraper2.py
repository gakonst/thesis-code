#!/root/etherscan_contracts_parser/venv/bin/python

is_staging = True

# library to bypass cloudflare protection
import cfscrape
from bs4 import  BeautifulSoup
import time
import json
import requests
from random import randint


scraper = cfscrape.create_scraper()
verified_contracts_path = 'verified_contracts.json'
to_parse_path = 'to_parse.json'


def main():
    # update to_parse.json
    unsent_contracts = update_to_parse()
    # parse newly found contracts
    # & send to ethfiddle
    parse_contracts(unsent_contracts)


def update_to_parse():

    ###### Part 1 ######
    ###### Parsing conractVerified page to get contract address and compiler v ######

    # formats
    # verified_contracts.json
    # {"contract_address": {
    #     "contract_name": "XYZ",
    #     "compiler_version": "v0.4.18",
    #     "contract_source_code": "...",
    #     "contract_abi": "...",
    #     "checked": True,
    #     "ethfiddle_share_code": "xGFt0asd"
    #     }
    # }

    # to_parse.json
    # {"contract_address": {
    #     "checked": True,
    #     "ethfiddle_share_code": "xGFt0asd"
    #     },
    #  "contract_address": {
    #     "checked": False,
    #     "contract_name": "XYZ",
    #     "compiler_version": "v0.4.18"
    #     }
    # 
    # }
    with open(to_parse_path, 'r') as f:
        to_parse_contracts_json = json.loads(f.read())

    page_index = 1

    while True:
        to_break = False
        verified_contracts_url = "https://etherscan.io/contractsVerified/{}".format(page_index)

        print 'Parsing ' + verified_contracts_url

        tries = 0
        while tries<4:
            try:
                site_html = scraper.get(verified_contracts_url).content
            except:
                print "Some error occurred while requesting contractsVerified page..."
                print "Waiting 5 seconds..."
                time.sleep(10)

            soup = BeautifulSoup(site_html, "html.parser")

            verified_contracts_html_list = soup.find('tbody').findAll("tr")

            if not verified_contracts_html_list and page_index > 391:
                to_break = True
                break
            elif verified_contracts_html_list:
                break
            else:
                sleep_time = randint(0, 12)
                print "Failed {} time(s). Will try in {} sec".format(tries, sleep_time)
                time.sleep(sleep_time)
                tries += 1

            if tries == 4:
                print "Maybe we got blocked... I will start from this spot on next execution"

        for tag in verified_contracts_html_list:
            lst = tag.findAll('td')
            contract_address = lst[0].text.strip().split(' ')[0]
            contract_name = lst[1].text.strip()
            compiler_version = lst[2].text.strip()
            balance = lst[3].text.strip()
            txcount = lst[4].text.strip()
            verified_data = lst[5].text.strip()

            contract_details_json = {
              "contract_name": contract_name,
              "compiler_version": compiler_version,
              "balance": balance,
              "txcount": txcount,
              "verified_data": verified_data,
              "checked": False
            }

            if contract_address in to_parse_contracts_json:
                # probably we need it, as we do not want to reparse all
                # pages. Turned off for initial load and potential breaks
                to_break = True
                continue

            to_parse_contracts_json.update({contract_address: contract_details_json})

        if to_break:
            to_break = False
            break

        page_index += 1

    _update_file(to_parse_path, to_parse_contracts_json)

    unsent_contracts = {}
    for i in to_parse_contracts_json:
        if not to_parse_contracts_json[i]['checked']:
            unsent_contracts.update({i: to_parse_contracts_json[i]})

    return unsent_contracts


def parse_contracts(unsent_contracts_json):

    ###### Part 2 ######
    ###### Parsing contract page to get source code and ABI ######

    offset = 10
    counter = 0

    to_break = False
    send_batch = {}
    for contract_address in unsent_contracts_json:
        contract_address = str(contract_address.split(' ')[0])

        if unsent_contracts_json[contract_address].get('contract_source_code'):
            continue

        print "Parsing contract: " + contract_address

        contract_code_url = 'https://etherscan.io/address/{}#code'.format(contract_address)

        tries = 0
        while tries<4:
            try:
                time.sleep(0.55)
                site_html = scraper.get(contract_code_url).content
            except:
                print "Some error occurred while requesting contract page..."
                print "Waiting 10 seconds..."
                time.sleep(10)

            soup = BeautifulSoup(site_html, "html.parser")
            
            try:
                # finds HTML tag containing contract source code
                contract_source_code = soup.findAll('pre', {'class': 'js-sourcecopyarea'})[0].text
                # finds HTML tag containing contract ABI
                contract_abi = soup.findAll('pre', {'class': 'wordwrap js-copytextarea2'})[0].text
                break
            except:
                sleep_time = randint(0, 12)
                print "Failed {} time(s). Will try in {} sec".format(tries, sleep_time)
                time.sleep(sleep_time)
                tries += 1

            if tries == 4:
                print "Maybe we got blocked... I will start from this spot on next execution"
                to_break = True

        if to_break:
            to_break = False
            continue

        contract_details_json = unsent_contracts_json[contract_address]
        contract_details_json.update({"contract_source_code": contract_source_code})
        # contract_details_json.update({"contract_abi": contract_abi})
        # contract_details_json.update({"contract_code_url": contract_code_url})
	

#        unsent_contracts_json.update({contract_address: contract_details_json})
        send_batch.update({contract_address: contract_details_json})

        counter += 1
        if counter % offset == 0:
            send_to_ethfiddle(send_batch)
            send_batch = {}


def send_to_ethfiddle(verified_contracts_json):
    
    print('Updating batch...')
    #with open(verified_contracts_path, 'w') as f:
    #    f.write(json.dumps(verified_contracts_json))

        ###### Part 3 ######
        ###### Shooting requests at Ethfiddle ######
    to_parse_json = {}

    for contract_address in verified_contracts_json:

        if not verified_contracts_json[contract_address].get('contract_source_code') or\
           not verified_contracts_json[contract_address].get('contract_abi'):
            continue

        if verified_contracts_json[contract_address].get('checked'):
            continue

        contract_address = contract_address.split(' ')[0]

        contract_details_json = verified_contracts_json[contract_address]
        contract_details_json.update({"checked": True})
        # contract_details_json.update({"ethfiddle_share_code": r.text})

        verified_contracts_json.update({contract_address: contract_details_json})

        to_parse_json.update({
            contract_address: {
                "checked": True,
            }
        })

    # update verified_contracts.json
    _update_file(verified_contracts_path, verified_contracts_json)


    # update to_parse.json
    _update_file(to_parse_path, to_parse_json)


def _update_file(file_path, update_data_json):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())

    data.update(update_data_json)

    with open(file_path, 'w') as f:
        f.write(json.dumps(data))    


if __name__ == '__main__':
    print "Starting script..."
    main()
    print "Finished"

