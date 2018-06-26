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

class Accountant(Contract):
    """ Module that manages the actions of an accountant"""

    def __init__(self, private_key, 
                abi_file, address, 
                meterdb_abi_file, meterdb_address, 
                endpoint):

        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)
        self.logger = logging.getLogger('Accountant')
        info = 'Connected to AccountingDB as operator!'
        self.logger.info(green(info))

        # ALSO CREATE A METERDB INSTANCE TO RETRIEVE VMETER VALUES/IDs.
        with open(meterdb_abi_file) as f:
            meterdb_abi = json.load(f)['abi']
        self.meterdb = Contract(None, meterdb_address, meterdb_abi, endpoint).contract

    ##### Billing Logic ############

    def bill(self, departments):
        """
        Bills departments. Gives priority to departments at bigger depth.
        Key to indicate bigger depth is the count of '::'.
        """
        departments = sort_by_depth(departments)
        for department_id in departments:
            (delegates, subdepartments, virtualmeters) = \
                    self._get_accounting_data(department_id)
            if len(virtualmeters) > 0:
                self.bill_virtualmeters(department_id, virtualmeters)
            if len(subdepartments) > 0:
                self.bill_subdepartments(department_id, subdepartments)
            if len(delegates) > 0:
                self.bill_delegates(department_id, delegates)

    def bill_virtualmeters(self, department_id, virtualmeters):
        total = 0
        for vm in virtualmeters:
            power = self._get_virtualmeter_power(vm)
            total += power

        self._bill_power(department_id, total)

    def bill_subdepartments(self, department_id, subdepartments):
        total = 0
        for subdep in subdepartments:
            power = self._get_department_power(subdep)
            total += power

        self._bill_power(department_id, total)   

    def bill_delegates(self, department_id, delegates):
        """ fixedSplits or headCountSplits """
        # Can only fixed split for 2 delegates

        # But only applies to a lower level department
        # High levels do headcount split (I.E. AdminAll -> HRI/HREG
        if len(delegates) == 2 and department_id.count('::') == 1:
            self._fixed_split(department_id)
        else:
            self._headcount_split(department_id)


    ########## General Management of Departments

    def _get_virtualmeter_power(self, vm):
        power = self.meterdb.functions.getCurrentMeterDataById(vm).call()[1]
        return power

    def _get_department_power(self, department_id):
        power = \
                self.contract.functions.getDepartmentData(
                        normalize(department_id)
                ).call()[2] # power is the 3rd argument

        return power

    def _get_accounting_data(self, department_id):
        (delegates, subdepartments, virtualmeters) = \
                self.contract.functions.getAccountingData(
                        normalize(department_id)
                ).call()

        return (delegates, subdepartments, virtualmeters)

    ########### Contract calls ##########

    def _bill_power(self, department_id, power):
        args = [normalize(department_id), power] 
        self.sign_and_send(self.contract.functions.billPower, args)

    def _fixed_split(self, department_id):
        args = [normalize(department_id), 50] # fixed 50-50 split here
        self.sign_and_send(self.contract.functions.fixedSplit, args)

    def _headcount_split(self, department_id):
        args = [normalize(department_id)] # need to send bytes
        self.sign_and_send(self.contract.functions.headcountSplit, args)

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
