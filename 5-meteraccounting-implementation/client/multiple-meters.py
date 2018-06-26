#!/usr/bin/env python3

import sys
import argparse
import logging
import subprocess
import traceback
import json
import time

from subprocess import Popen
import os
import sys

LOGS = './logs'

def run(cmd, logfile):
    fname = os.path.join(LOGS,logfile+'_{}.log'.format(int(time.time())))
    with open (fname, 'w') as log:
        p = Popen(cmd, stdout=log, stderr=log)
        return p


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
            """
            Launch multiple Meter instances
            Default config file is the meter_config.json file in the same directory
            """,
            usage="""
            ./multiple-meters.py -c multi-meter.json
            """)

    parser.add_argument('--address', '-a',
            help='address of deployed MeterDB contract',
            action='store',
            default='0xb549d25374337a3d2cc7bad7a4009d8cb1c3f537')

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

    # Configure endpoint, 
    if args.ipc:
        endpoint = args.ipc
    if args.rpc:
        endpoint = args.rpc


    try:
        # Initialize object for meter
        with open(args.config) as meter_keys:
            data = json.load(meter_keys)

        cmd = './single-meter.py -k {} -a ' +args.address
        if args.debug:
            cmd += ' --debug'

        processes = []
        for meter_id in data:
            key = data[meter_id]['private_key']
            p = run(
                cmd.format(key).split(),
                meter_id
            )
            print('Launched', cmd.format(key))
            processes.append(p)
        print('Entering infinite loop until CTRL+C. Will cleanup processes afterwards')
        while True:
            time.sleep(1)
    except Exception as e:
        logging.error(traceback.format_exc())
    except (KeyboardInterrupt, SystemExit):
        print('\n Got interrupt. Exiting...')
        for p in processes:
            p.kill()

