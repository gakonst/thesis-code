from utils.framework import *
from utils.getWeb3 import *
import pandas as pd
from os.path import basename
import configparser
import sys

config = configparser.RawConfigParser()
config.optionxform = str
config.read(sys.argv[1])

TEXDIR = './tex/'

BREAKLINE = '========================= {} ========================='
CONTRACTS_DIR = 'contracts/'
endpoint = '/tmp/geth.ipc'
w3 = getWeb3(endpoint)

contracts = sys.argv[2:]
# Remix is running optimizer 500 times
optimizer_runs = [1, 100, 500, 500000]

def functions_gas_consumption(r):
    '''Longer bytecode for bigger r -> more gas to deploy, but less gas per function call
    https://github.com/ethereum/solidity/issues/2245'''
    # print('Optimizer runs: {}'.format(r))
    for func_name in funcs:
        args = funcs[func_name].split(',') 
        if len(args) > 1: # make easier to follow
            args = [int(arg) for arg in args] # should be done via ABI.
            tx_hash, gas_used = contract.call(func_name, args)
        else:
            tx_hash, gas_used = contract.call(func_name)
        # print('{} estimated gas => {}'.format(func_name, gas_used))
        gas_costs.at[r, func_name] = gas_used

for fname in contracts:
    print(BREAKLINE.format(fname))
    funcs = dict(config.items('FUNCTIONS'))
    gas_costs = pd.DataFrame(index=[0].extend(optimizer_runs), columns=funcs.keys())

    contract = Contract(fname, endpoint) # contract object from our framework connected to w3
    compiled = contract.compile(False)

    instance, deploy_gas = compiled.deploy()
    gas_costs.at[0, 'Deployment'] = deploy_gas # set constructor costs
    functions_gas_consumption(0)
    for r in optimizer_runs:
        compiled = contract.compile(True, r)
        instance, deploy_gas = compiled.deploy()
        gas_costs.at[r, 'Deployment'] = deploy_gas

        functions_gas_consumption(r)

    print(gas_costs)
    ''' Gas costs for each function depending on optimizer runs
           OptRuns   Register CreateCharacter  Deployment
           0         70003           66584     748911.0
           1         69943           66555     508730.0
           100       69811           65974     539653.0
           500       69604           65905     557086.0
           500000    69598           65905     570402.0
    '''
    with open(TEXDIR+basename(fname)+'_data.tex', 'w') as f:
        f.write(gas_costs.to_latex())


    print(instance.functions.GetCharacterStats(0).call())
