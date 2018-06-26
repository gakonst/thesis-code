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

class MeterOperator(Contract):
    """ Module that manages the actions of an operator"""

    def __init__(self, private_key, abi_file, address, endpoint):
        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)
        self.logger = logging.getLogger('MeterOperator')
        info = 'Connected to MeterDB as operator!'
        self.logger.info(green(info))

    def get_meter_history(meter_id):
        # TODO: Return all events filtered for that MeterID and print in pandas dataframe
        # address = self._id_to_address(meter_id) # if user gives ID, convert to address
        pass



    def activate_meters(self, data):
        for meter_id, address in data:
            self.activate_meter(address, meter_id)

    def deactivate_meters(self, meter_ids):
        for meter_id in meter_ids:
            self.deactivate_meter(meter_id)

    def activate_meter(self, meter_address, meter_id):
        ''' ID can be either ELTXX or HX.ZXX.W so we normalize to ELT always'''
        elt = self._name_to_elt(meter_id)
        address = self.w3.toChecksumAddress(meter_address)
        args = [ address, normalize(elt) ]
        self.sign_and_send(self.contract.functions.activateMeter, args)

    def deactivate_meter(self, meter_id):
        address = self.w3.toChecksumAddress(
                self._id_to_address(meter_id) # if user gives ID, convert to address
                )
        args = [ address ]
        self.sign_and_send(self.contract.functions.deactivateMeter, args)

        

    def _id_to_address(self, meter_id):
        ''' If a meter_id is given it converts it to its address'''
        normalized = meter_id
        if not meter_id.startswith('0x'):
            normalized = self.contract.functions.meterAddressById(
                    bytes(meter_id, 'utf-8')).call()
        return normalized

    def _name_to_elt(self, meter_id):
        meters = dict(MeterNames.__dict__) # gets all name-values
        if meter_id not in (list(meters.values()) + list(meters.keys())):
            raise NotAMeter('Invalid meter ID/name')

        # Starts with ELT/KMZ
        if meter_id in list(meters.keys()):
            normalized = meter_id

        for elt, name in meters.items():
            if name == meter_id:
                normalized = elt

        return normalized
