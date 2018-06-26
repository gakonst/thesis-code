#!/usr/bin/env python3

import sys
import argparse
import logging
import subprocess
import traceback
import json

from meter.meterOperator import MeterOperator

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Meter management to ping values to the MeterDB contract.
            Default config file is the meter_config.json file in the same directory
            """,
            usage="""
            ./meter-operator.py -c remove.conf
            ./meter-operator.py -c add.conf
            ./meter-operator.py -m 0xfe666de1e8c832ed75c49976aa7899565c21b106 -i KMZ6
            ./meter-operator.py -m 0xfe666de1e8c832ed75c49976aa7899565c21b106
            """)

    parser.add_argument('--deactivate', '-d',
            help='deactivate mode',
            action='store_true')

    parser.add_argument('--abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/MeterDB.json')

    parser.add_argument('--address', '-a',
            help='address of deployed MeterDB contract',
            action='store',
            default='0xb549d25374337a3d2cc7bad7a4009d8cb1c3f537')

    parser.add_argument('--key', '-k',
            help='file with the keys of the manager',
            action='store',
            default='conf/roles/meteroperator.json') # TODO CHANGE

    parser.add_argument('--meter-address', '-m',
            help='address of the meter to activate/deactivate',
            action='store')

    parser.add_argument('--meter-id', '-i',
            help='id of the meter to be activated',
            action='store')

    parser.add_argument('--fund', '-f',
            help='Fund the activated meters with a small amount so that they can ping',
            action='store_true')


    parser.add_argument('--config', '-c',
            help='Config file',
            default='conf/demo/simple_meters.json',
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

    args = parser.parse_args()


    # Configure logging
    default_log = logging.INFO
    if args.debug:
        default_log = logging.DEBUG

    for (l_name, l_level) in [('Meter', default_log),
            ('MeterOperator', default_log),
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
        admin = MeterOperator(key, args.abi,  args.address, endpoint)
        if (args.config):
            with open(args.config) as meter_keys:
                data = json.load(meter_keys)
            if args.deactivate:
                data = [data[meter_id]['public_key']  for meter_id in data]
                admin.deactivate_meters(data)
            else:
                data = [(meter_id, d['public_key'])  for meter_id, d in data.items()]
                admin.activate_meters(data)
                if args.fund:
                    for meter_id, address in data:
                        admin.send_transaction(address, admin.w3.toWei(0.01, 'ether'))

                # When activating, allow the option to fund that address:

        elif (args.meter_address):
            if (args.meter_id):
                admin.activate_meter(args.meter_address, args.meter_id)
                if args.fund:
                    admin.send_transaction(args.meter_address, admin.w3.toWei(0.01, 'ether'))
            else:
                admin.deactivate_meter(args.meter_address)
        else:
            print('CLI not implemented yet!')

        ## Command line interface here.
        # Break command in <command> <args>

        # meter.administrator()
    except Exception as e:
        # logging.error('Error in %s' % (args.filename, ))
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')

