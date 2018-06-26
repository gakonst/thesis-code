import logging
import time
import web3

from .monitoringserver.monitoringclient import MonitoringClient

from .utils.colors import green, red, yellow
from .utils.datatypes import Time, MeterNames
from .utils.exceptions import NotAMeter
import json

from .base.contract import Contract
from .utils.formatters import normalize

logging.basicConfig()

class RegistryOperator(Contract):
    """ Module that manages the actions of an operator"""

    def __init__(self, private_key, abi_file, address, endpoint):
        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)
        self.logger = logging.getLogger('RegistryOperator')
        info = 'Connected to Registry!'
        self.logger.info(green(info))

    def resolve(self, contract):
        if not contract.startswith('0x'):
            # Given a contract name => return its address
            return self._resolve_name(contract)
        else:
            # Given a contract address => return its name
            return self._resolve(contract)


    def _resolve(self, address):
        args = self.w3.toChecksumAddress(address)
        return self.contract.functions.resolve(args).call()

    def _resolve_name(self, contract_name):
        args = normalize(contract_name)
        return self.contract.functions.resolveName(args).call()

    def enable(self, contract_address, contract_id):
        address = self.w3.toChecksumAddress(contract_address)
        args = [ address, normalize(contract_id) ]
        self.sign_and_send(self.contract.functions.enable, args)

    def disable(self, contract):
        address = self.w3.toChecksumAddress(
                self._id_to_address(contract) # if user gives ID, convert to address
                )
        args = [ address ]
        self.sign_and_send(self.contract.functions.deactivateMeter, args)

    def _id_to_address(self, name):
        ''' If a meter_id is given it converts it to its address'''
        normalized = name
        if not name.startswith('0x'):
            normalized = self._resolve_name(name)
        return normalized

