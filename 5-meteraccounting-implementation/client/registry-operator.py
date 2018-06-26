#!/usr/bin/env python3

import sys
import argparse
import logging
import subprocess
import traceback
import json

from meter.registryOperator import RegistryOperator

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Meter management to ping values to the MeterDB contract.
            Default config file is the meter_config.json file in the same directory
            """,
            usage="""
            ./registry-operator.py --action <ACTION> [args]
            """)

    parser.add_argument('--action',
            help='revoke or add roles',
            action="store",
            choices=['resolve', 'enable', 'disable'],
            default=True)

    parser.add_argument('--key', '-k',
            help='file with the keys of the registry_operatoristrator',
            action='store',
            default='conf/roles/registryoperator.json') # TODO CHANGE

    parser.add_argument('--registry-address', '-a',
            help='address of deployed registry',
            action='store',
            default='0x90154ecdbb7affec73ec45c0da0d42f4f339766c')

    parser.add_argument('--registry-abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/Registry.json')

    parser.add_argument('--contract', '-c',
            help='Contract to resolve',
            action='store')

    parser.add_argument('--id', '-i',
            help='Contract to enable/disable id',
            action='store')

    parser.add_argument('--address',
            help='Contract to enable/disable address',
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
            ('RegistryOperator', default_log),
            ('Contract', default_log)]:
        l = logging.getLogger(l_name)
        l.setLevel(l_level)

    # Configure endpoint, 
    if args.ipc:
        endpoint = args.ipc
    if args.rpc:
        endpoint = args.rpc
    

    try:
        with open(args.key) as registry_operator_key:
            key = json.load(registry_operator_key)['private_key']
        # Initialize object for meter
        registry_operator = RegistryOperator(
                key, 
                args.registry_abi, args.registry_address, 
                endpoint)

        if args.action == 'resolve':
            ret = registry_operator.resolve(args.contract)
            print(args.contract, 'resolves to =>', ret)
        elif args.action == 'enable':
            registry_operator.enable(args.address, args.id)
        elif args.action == 'disable':
            registry_operator.disable(args.id)

    except Exception as e:
        # logging.error('Error in %s' % (args.filename, ))
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')

