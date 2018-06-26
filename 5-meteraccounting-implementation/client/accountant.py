#!/usr/bin/env python3

import sys
import argparse
import logging
import subprocess
import traceback
import json

from meter.accountant import Accountant

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Meter management to ping values to the MeterDB contract.
            Default config file is the meter_config.json file in the same directory
            """,
            usage="""
            ./accountant.py -c conf/demo/simple_departments.json
            """)

    parser.add_argument('--key', '-k',
            help='file with the keys of the manager',
            action='store',
            default='conf/roles/accountant.json')

    parser.add_argument('--config', '-c',
            help='Config file',
            action='store',
            default='conf/demo/simple_departments.json')

    parser.add_argument('--meter-address', '-m',
            help='address of deployed meter contract',
            action='store',
            default='0xb549d25374337a3d2cc7bad7a4009d8cb1c3f537')

    parser.add_argument('--meter-abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/MeterDB.json')

    parser.add_argument('--accounting-address', '-a',
            help='address of deployed accounting contract',
            action='store',
            default='0x8b09c842d2116f682e75c8b8bb148d6f9983b468')

    parser.add_argument('--accounting-abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/AccountingDB.json')

    endpoint_config = parser.add_mutually_exclusive_group()
    endpoint_config.add_argument('--rpc',
            help='json rpc endpoint',
            action='store',
            default='http://localhost:8545')

    endpoint_config.add_argument('--ipc',
            help='ipc endpoint',
            action='store',
            default='/tmp/geth.ipc')

    # Debug
    parser.add_argument('--debug',
            help='Debug mode',
            action="store_true",
            default=False)

    parser.set_defaults(init=False)
    args = parser.parse_args()

    # Configure logging
    default_log = logging.INFO
    if args.debug:
        default_log = logging.DEBUG

    for (l_name, l_level) in [('Meter', default_log),
            ('Accountant', default_log),
            ('Contract', default_log)]:
        l = logging.getLogger(l_name)
        l.setLevel(l_level)

    # Configure endpoint, 
    if args.ipc:
        endpoint = args.ipc
    if args.rpc:
        endpoint = args.rpc
    

    try:
        # Initialize object for meter
        with open(args.key) as operator_key:
            key = json.load(operator_key)['private_key']
        accountant = Accountant(
                key, 
                args.accounting_abi, args.accounting_address, 
                args.meter_abi, args.meter_address, 
                endpoint)
        with open(args.config) as data_in:
            departments = json.load(data_in).keys()

        while True:
            accountant.bill(departments)
            input("Press Enter to bill again...")

    except Exception as e:
        # logging.error('Error in %s' % (args.filename, ))
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')

