# Meter/Billing Client

Python implementation of clients that interact with the smart contracts for the purpose of the thesis. 

## Overview

The provided scripts are each meant to be used by the owner of the private key related to each role. The `admin.py` script allows the Administrator to set the roles that enable all other operators to use the scripts. A full setup of the system can be done as follows:

```
./admin.py -c conf/acl-roles.json --action grant -f --debug
./meter-operator.py -c conf/demo/simple_meters.json --fund --debug
./meter-operator.py -c conf/demo/simple_virtualmeters.json --fund --debug
./accounting-operator.py -c conf/demo/simple_departments.json --init --debug
```

At this point, all roles have been initialized, meters and virtual meters have been activated, and departments have been configured to have their proper headcount, delegates and subdepartments as the structure in the configuration files dictates. The system is created in such a way that only the owner for the private key of the `meteroperator` role is able to use the `meter-operator.py` script. This applies to all roles. All keys are stored in plaintext for usability and demonstration purposes however it is trivial to store them encrypted with a strong password.

For help regarding the command line usage run a script with the `help` flag, e.g. `./admin.py --help`. Make sure to install all dependencies before trying to run any script by running `pip install -r requirements.txt`. It is highly encouraged to create a separate virtual environment for this process.

A full demo that initializes the system, launches all meters and starts the accountant process can be performed by running `demo.sh`.

While the scripts are running, timestamped log data for each meter is saved under the logs directory.

## For Developers

### Smart Contract Interaction

All configuration files can be found under the `conf` directory. `conf/demo` contains sample keypairs for meters, virtual meters and departments for demonstration purposes and can be made public. The `conf/prod` directory contains proprietary honda company structure and is not to be made public. 


Each script connects to a web3 RPC endpoint which allows it to interface with the contract through [web3.py](https://github.com/ethereum/web3.py). By default, web3.py does not support locally signing smart contract function calls, and this needs to be done manually. A helper class `Contract` was written, found in `meter/base/contract.py` which can be used as a base class to write python bindings for smart contracts with offline transaction signing. This allows initializing a contract class by providing a private key, the contract's abi and address and the RPC URI where the contract is deployed at. After that, it's simply a matter of defining the contract's functions in Python. Files under the `meter` directory utilize the base class to interface with their respective smart contracts. 

### Monitoring Server Interaction
A class for interacting with the monitoring server REST API was written. It currently implements mehtods for parts of the rest API necesssary for the thesis however it can be extended to fully implement the API's functionality. 

### Command Line Interfaces

Each CLI takes arguments for each functionality and performs the necessary calls to the smart contracts depending on the flags supplied. It is expected that the admin account has an initial amount of Ether which they use to distribute funds for gas costs to the operators and the meters.  
