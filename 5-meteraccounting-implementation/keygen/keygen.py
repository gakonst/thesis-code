#!/usr/bin/env python3

#### INSECURE Version, outputs private keys in plaintext in json file
#### USE ONLY FOR TESTING - Georgios Konstantopoulos 

import argparse
import sys

import json
import Crypto
import ethereum.tools.keys
import collections

def main():
    """ Program to create keys for a given list of meters and store them in
        an encrypted mapping file.
    """

    DEFAULT_INPUT  = 'meters.list'

    # Define a command line parser and parse the command line arguments
    parser = argparse.ArgumentParser(description='Program to create keys for a given list of meters and store them in an encrypted mapping file.')
    parser.add_argument('-i', '--input',  default=DEFAULT_INPUT,  help='name of the file containing the meter names (default: {})'.format(DEFAULT_INPUT))
    args = parser.parse_args()

    # Read the meter list
    with open(args.input, 'r') as f_in:
        meters = f_in.read().split('\n')[:-1]

    # Create keys for the new meters
    rng = Crypto.Random.new()
    data = collections.defaultdict(dict)
    for meter in meters:
        key_priv = rng.read(32)
        key_pub  = ethereum.tools.keys.privtoaddr(key_priv)
        data[meter]['private_key'] = '0x'+ethereum.tools.keys.encode_hex(key_priv)
        data[meter]['public_key'] = '0x'+ethereum.tools.keys.encode_hex(key_pub)
    with open(args.input.replace('list', 'json'), 'w') as f_out:
        json.dump(data, f_out, sort_keys=True)

if __name__ == '__main__':
    sys.exit(main())
