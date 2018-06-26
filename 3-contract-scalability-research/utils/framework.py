from .getWeb3 import *
from os.path import basename
from solc import compile_source
import warnings
import re

with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)

class Contract(object):

    def __init__(self, fname, endpoint=None):
        ''' Initialize web3 object and attributes for the contract'''
        self.fname = fname
        self.web3  = getWeb3(endpoint) 
        self.abi = None
        self.bytecode = None
        self.contract_instance = None

    def compile(self, optimize=False, optimize_runs=200):
        '''Compile & get Contract's Application Binary Interface & Bytecode'''
        src = open(self.fname).read()
        if optimize:
            compiled_sol = compile_source(src, optimize=optimize, optimize_runs=optimize_runs)
        else:
            compiled_sol = compile_source(src, optimize=optimize)

        interface = compiled_sol['<stdin>:{}'.format(
                        basename(self.fname.rstrip('.sol')))]
        self.bytecode = interface['bin']
        self.abi = interface['abi']
        return self

    def deploy(self, constructor_args=None, sender=None, amount=0):
        ''' Returns contract instance and how much was used for deploying'''
        if constructor_args is None: 
            constructor_args = []
        if sender is None:
            sender = self.web3.eth.accounts[0]

        contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.deploy(args=constructor_args, transaction={'from': sender, 'value': amount}) # deprecated in newer web3 version

        # Wait until transaction is mined
        tx_receipt = waitForTransactionReceipt(self.web3, tx_hash)
        contract_address = tx_receipt['contractAddress']

        # print('Contract ABI {}'.format(self.abi))
        # print('Contract Bytecode {}'.format(self.bytecode))
        # print('Transaction Hash: {}'.format(self.web3.toHex(tx_hash)))
        # print('Contract deployed at: {}'.format(contract_address))

        # Create web3 contract object
        self.contract_instance = self.web3.eth.contract(address=contract_address, abi=self.abi)

        return self.contract_instance, tx_receipt['gasUsed']

    def call(self, function_name, args=None):
        ''' Returns tx_hash  and how much was used for calling the function'''
        func = getattr(self.contract_instance.functions, function_name)
        # print('Expecting to spend {} gas'.format(func().estimateGas()))
        # print(function_name, args)
        # args go inside `func`, not in `transact`
        if args is None:
            args = []
        tx_hash = func(*args).transact()
        tx_receipt = waitForTransactionReceipt(self.web3, tx_hash)
        return tx_hash, tx_receipt['gasUsed']





