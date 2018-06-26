import time
import web3

from .monitoringserver.monitoringclient import MonitoringClient

from .utils.colors import green, red, yellow
from .utils.datatypes import Time, MeterNames
from .utils.exceptions import NotAMeter
from .utils.logconfig import configure_logging

from .base.contract import Contract
import json

class Meter(Contract):
    """ Module that manages 1 meter"""

    def __init__(self, private_key, abi_file, address, endpoint):
        with open(abi_file) as f:
            abi = json.load(f)['abi']
        super().__init__(private_key, address, abi, endpoint)

        # Check if meter is active
        active = self.contract.functions.isActive(self.account.address).call()
        if not active:
            raise NotAMeter('Check that the meter is enabled by the operator')

        # Get meter ID and connect to the monitoring server
        meter_id = self.contract.functions.getCurrentMeterData(self.account.address).call()[0]
        meter_id = meter_id.split(b'\0',1)[0].decode('ascii')
        self.meter_id = getattr(MeterNames, meter_id)
        self.monitoring_client = MonitoringClient(self.meter_id) 

        self.logger = self.monitoring_client.logger


        info = 'Initialized Meter {}'.format(self.meter_id)
        self.logger.info(green(info))

    def start_pinging(self):
        """ 
            TODO: Ping until latest value 
            and then wait until there is a new value 
            https://stackoverflow.com/questions/5114292/break-interrupt-a-time-sleep-in-python
        """
        (last_reading, reading) = (0, 0)
        while True: # Meter loops forever
            last_reading = reading
            (reading, timestamp) = \
                self.monitoring_client.get_single_reading(when=Time.NOW)
            # Wait until we get a new reading
            # Perhaps make a call to monitoring server every 15 mins? 
            while (reading == last_reading):
                print('Sleeping until new reading')
                time.sleep(20)
                (reading, timestamp) = \
                    self.monitoring_client.get_single_reading(when=Time.NOW)

            self.ping(reading, timestamp)
            
            info = 'Pinged {} kWh at t={}'.format(reading, timestamp)
            self.logger.info(green(info))

    def ping(self, reading, timestamp):
        """
            Takes reading and timestamp and creates a 
            raw transaction call to `ping` at the target contract
        """
        args = [int(reading), int(timestamp)]
        self.sign_and_send(self.contract.functions.ping, args)
