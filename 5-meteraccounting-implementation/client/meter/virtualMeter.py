import time
import web3
import json


from .utils.colors import green, red, yellow
from .utils.datatypes import Time, MeterNames, Coefficients
from .utils.exceptions import NotAMeter

from .base.contract import Contract
from py_expression_eval import Parser

from .utils.formatters import normalize
from .utils.logconfig import configure_logging


class VirtualMeter(Contract):
    """ Module that manages a virtual meter"""

    def __init__(self, private_key, abi_file, address, endpoint, formula):
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
        # Replace formula with ELT(x) calls.
        self.formula = Parser().parse(formula.replace('x','*'))
        self.logger = configure_logging(self.meter_id)

        info = 'Initialized!'
        self.logger.info(green(info))
        
    def start_pinging(self):
        (last_reading, reading) = (0, 0)
        while True: # Meter loops forever
            last_reading = reading
            (reading, timestamp) = \
                self.calculate_reading()
            # Wait until we get a new reading
            # Perhaps make a call to monitoring server every 15 mins? 
            while (reading == last_reading):
                self.logger.warning(red('Sleeping until new reading'))
                time.sleep(20)
                (reading, timestamp) = \
                    self.calculate_reading()

            self.ping(reading, timestamp)
            
            info = 'Pinged {} kWh at t={}'.format(reading, timestamp)
            self.logger.info(green(info))


    def calculate_reading(self):
        """
            Utilizes Abstract Syntax Trees to parse an equation
            and evaluate ELT readings or Coefficients
            github.com/Axiacore/py-expression-eval
        """

        args = dict()
        coefficients = vars(Coefficients)
        meters = [m for m in self.formula.variables() if not m.startswith('F')]
        for var in self.formula.variables():
            # If it's a known coefficient get it from the constants list
            if var in coefficients:
                args[var] = getattr(Coefficients, var)
            # If it's an ELT or KMZ, get it from the blockchain
            else:
                info = 'Fetching reading for => {}'.format(var)
                self.logger.debug(green(info))
                addr = self.contract.functions.meterAddressById(normalize(var)).call()
                data = self.contract.functions.getCurrentMeterData(addr).call()
                reading = data[1]
                args[var] = reading
        timestamp = data[2]
        info = 'Arguments to be evaluated => {}'.format(args)
        self.logger.debug(yellow(info))

        reading = self.formula.evaluate(args)
        return reading, timestamp

    def ping(self, reading, timestamp):
        """
            Takes reading and timestamp and creates a 
            raw transaction call to `ping` at the target contract
        """
        args = [int(reading), int(timestamp)]
        self.sign_and_send(self.contract.functions.ping, args)
