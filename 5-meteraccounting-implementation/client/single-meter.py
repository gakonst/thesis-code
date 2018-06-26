#!/usr/bin/env python3

import sys
import os
import argparse
import logging
import traceback

from meter.meter import Meter

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Meter client that polls readings from the monitoring server
            and pings them periodically to the specified smart contract
            """,
            usage="./single-meter.py -k <meterPrivateKey> -a <contractAddress>")

    parser.add_argument('--address', '-a',
            help='address of deployed MeterDB contract',
            action='store',
            default='0xb549d25374337a3d2cc7bad7a4009d8cb1c3f537')

    parser.add_argument('--abi',
            help='ABI of Contract',
            action='store',
            default='conf/abi/MeterDB.json')

    parser.add_argument('--key', '-k',
            help='meter\'s private key, used to send data to the blockchain',
            action='store',
            default='0x0')

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
    if args.debug:
        os.environ['DEBUG'] = 'OK'

    # Configure endpoint
    if args.ipc:
        endpoint = args.ipc
    if args.rpc:
        endpoint = args.rpc

    try:
        meter = Meter(args.key, args.abi, args.address, endpoint)
        meter.start_pinging()
    except Exception as e:
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')

