import logging
import time
import web3
import json

from .monitoringserver.monitoringclient import MonitoringClient

from .utils.colors import green, red, yellow
# from .utils.datatypes import Time, AccountingNames
# from .utils.exceptions import NotAAccounting

from .utils.formatters import normalize, sort_by_depth
from .base.contract import Contract

logging.basicConfig()

class AccountingOperator(Contract):
    """ Module that manages the actions of an accountant"""

    def __init__(self, private_key, 
                abi_file, address, 
                meterdb_abi_file, meterdb_address, 
                endpoint):

        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)
        self.logger = logging.getLogger('AccountingOperator')
        info = 'Connected to AccountingDB as operator!'
        self.logger.info(green(info))

        # ALSO CREATE A METERDB INSTANCE TO RETRIEVE VMETER VALUES/IDs.
        with open(meterdb_abi_file) as f:
            meterdb_abi = json.load(f)['abi']
        self.meterdb = Contract(None, meterdb_address, meterdb_abi, endpoint).contract

    def activate_departments(self, data):
        for department_id, d in data.items():
            self.activate_department(department_id, d)

    def deactivate_departments(self, department_ids):
        for department_id in department_ids:
            self.deactivate_department(department_id)

    def activate_department(self, department_id, data):
        """ ID follows the formatting XX::XX"""
        # Activate department ID
        self._activate_department_id(department_id)
        for prop, d in data.items():
            self._set_department_property(prop, department_id, d)

    def deactivate_department(self, department_id):
        self._deactivate_department(department_id)

    ########### Contract calls ##########

    def _activate_department_id(self, department_id):
        args = [normalize(department_id)] # need to send bytes
        self.sign_and_send(self.contract.functions.activateDepartment, args)

    def _deactivate_department(self, department_id):
        args = [normalize(department_id)] # need to send bytes
        self.sign_and_send(self.contract.functions.deactivateDepartment, args)

    def _set_department_property(self, key, department_id, data):
        """ Calls function of department based on the key given """
        args = [ normalize(department_id), normalize(data) ]
        func = self._get_func_mux(key)
        self.sign_and_send(func, args)

    def _get_func_mux(self, key):
        if key == 'headcount':
            func = self.contract.functions.setHeadcount
        if key == 'delegates':
            func = self.contract.functions.setDelegates
        if key == 'subdepartments':
            func = self.contract.functions.setSubDepartments
        if key == 'virtualmeters':
            func = self.contract.functions.setVirtualMeters
        return func
