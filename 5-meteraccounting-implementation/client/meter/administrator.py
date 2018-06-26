import logging
import time
import web3
import json

from .utils.colors import green, red, yellow
from .utils.datatypes import Permissions
from .base.contract import Contract

logging.basicConfig()

class Administrator(Contract):
    """ Module that manages the actions of an accountant"""

    def __init__(self, private_key, 
                abi_file, address, 
                endpoint):

        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)
        self.logger = logging.getLogger('Administrator')
        info = 'Connected to Authority as admin {}!'.format(self.account.address)
        self.logger.info(green(info))

    ##### Administrative Logic ############

    def grant_roles(self, data):
        for role, to in data:
            self.grant_role(to, role)

    def revoke_roles(self, data):
        for role, to in data:
            self.revoke_role(to, role)

    def grant_role(self, to, role):
        role = self._get_role(role)
        self._set_user_role(to, role, True)

    def revoke_role(self, to, role):
        role = self._get_role(role)
        self._set_user_role(to, role, False)

    def grant_permissions_to_func(self, role, contract_address, func_sig):
        # TODO improve UX with providing signature
        self._set_role_capability(role, contract_address, func_sig, True)

    def revoke_permissions_to_func(self, role, contract_address, func_sig):
        # TODO improve UX with providing signature
        self._set_role_capability(role, contract_address, func_sig, False)

    ########### Contract calls ##########

    def _get_role(self, role):
        if role.lower() == 'registryoperator':
            return 1
        if role.lower() == 'meteroperator':
            return 2
        if role.lower() == 'accountingoperator':
            return 3
        if role.lower() == 'accountant':
            return 4

    def _set_user_role(self, user, role, state=True):
        # user = address, need to checksum
        # role = uint
        user = self.w3.toChecksumAddress(user)
        args = [user, role, state]
        self.sign_and_send(self.contract.functions.setUserRole, args)

    def _set_role_capability(self, role, contract_address, func_sig, state=True):
        # user = address, need to checksum
        # role = uint
        args = [role, contract_address, func_sig, state]
        self.sign_and_send(self.contract.functions.setRoleCapability, args)
