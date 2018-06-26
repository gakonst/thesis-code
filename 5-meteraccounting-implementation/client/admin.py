#!/usr/bin/env python3

import sys
import argparse
import logging
import subprocess
import traceback
import json

from meter.administrator import Administrator

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Meter management to ping values to the MeterDB contract.
            Default config file is the meter_config.json file in the same directory
            """,
            usage="""
            ./accountant.py -c departments.conf --init
            """)

    parser.add_argument('--action',
            help='revoke or add roles',
            action="store",
            choices=['grant', 'revoke'],
            default=True)

    parser.add_argument('--key', '-k',
            help='file with the keys of the administrator',
            action='store',
            default='conf/roles/admin.json') # TODO CHANGE

    parser.add_argument('--fund', '-f',
            help='Fund the activated meters with a small amount so that they can ping',
            action='store_true')

    parser.add_argument('--config', '-c',
            help='Config file',
            action='store',
            default='conf/acl-roles.json')

    parser.add_argument('--authority-address', '-a',
            help='address of deployed authority',
            action='store',
            default='0x4495a829cd1dbdd445c05e1ae58db54a0fef5512')

    parser.add_argument('--authority-abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/DSRoles.json')

    parser.add_argument('--role', '-r',
            help='Role to give',
            choices=['meteroperator', 'accountant', 'accountingoperator', 'registryoperator'],
            action='store')

    parser.add_argument('--to',
            help='Modify role of this address',
            action='store')

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
            ('Administrator', default_log),
            ('Contract', default_log)]:
        l = logging.getLogger(l_name)
        l.setLevel(l_level)

    # Configure endpoint, 
    if args.ipc:
        endpoint = args.ipc
    if args.rpc:
        endpoint = args.rpc
    

    try:
        with open(args.key) as admin_key:
            key = json.load(admin_key)['private_key']
        # Initialize object for meter
        admin = Administrator(
                key, 
                args.authority_abi, args.authority_address, 
                endpoint)
        if args.config:
            with open(args.config) as data_in:
                data = json.load(data_in) # pubkey/role format
            data = [(role, d['public_key'])  for role, d in data.items()]
            if args.action.lower() == 'grant':
                admin.grant_roles(data)
                if args.fund:
                    for role, address in data:
                        admin.send_transaction(address, admin.w3.toWei(2, 'ether'))
            else:
                admin.revoke_roles(data)
        else:
            if args.action.lower() == 'grant':
                admin.grant_role(args.to, args.role)
            elif args.action.lower() == 'revoke':
                admin.revoke_role(args.to, args.role)
            if args.fund:
                admin.send_transaction(args.to, admin.w3.toWei(2, 'ether'))
    except Exception as e:
        # logging.error('Error in %s' % (args.filename, ))
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')

