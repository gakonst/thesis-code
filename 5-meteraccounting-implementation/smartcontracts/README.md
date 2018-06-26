# Meter/Accounting Smart Contracts

Brief description of the functionalities implemented in the smart contracts authored for the purposes of the thesis _Decentralized Meter and Billing on Ethereum with respect to Security and Scalability_

# Metering

A Meter library and Meter database contract are implemented which are responsible for all meter related logic. The last two stored values are stored in a smart contract. This is done so that, if needed, a billing contract can calculate the delta in energy consumption and bill it accordingly. A `Pinged` event is emitted after each ping so that clients can have full access to the meter readings that have been stord in the blockchain. 

## Meter Library
Each meter is required to have:
- **active** - `bool`: Used to verify if the meter at this address is initialized
- **ID** - `bytes8`: 8 characters including dots. e.g. 'U3.Z40.W. 
- **currentPower** - `uint48`: Balance in kWh. The chosen granularity is in multiples of **1 Wh**. It is considered that a meter can count up to 2^48 Wh which afr exceeds any value that it is expected to reach in its lifetime.
- **currentTimestamp** `uint32`: The UNIX timestamp that matches the `currentPower` reading, counts up to 2^32 which can suffice until the year 2106.
- **lastPower** - `uint48`: Same as **currentPower** but stores the last power value.
- **lastTimestamp** - `uint32`: Same as **currentTimestamp** but stores the last timestamp value.

This is implemented in `Meter.sol` and exports a gas efficient API for storing and retrieving meter values.

## MeterDB
Utilizes the `Meter.sol` library to maintain a list of meter readings that get stored in the smart contract. The `ping` is used to update the values of a registered meter.

# Billing

## Department Library

In order for department bill forwarding to happen, three separate variables are maintained that track power consumption from each source separately. As a result, each department is required to have:
- `totalPower` - `uint80`: The total power calculated for a department as a sum of the consumptions of its virtual meters and subdepartments
- `clearedPower` - `uint80`: The total power of the department that has been cleared, and as a result should not be further be taken into account for any billing processes
- `delegatedPower` - `uint80`: The amount of power that the department has received from other departments as part of the delegation / splitting process. 

In addition, some subdepartments may have a `headcount` variable which is a percentage (between 0 and 100) of employees that work at their department's subdepartment, i.e. DEP01::SUBDEP01 can have 25% and DEP01::SUBDEP02 can have 75% headcount. This is used for the headcount split forwarding logic, where each department in a headcount split is billed energy proportionally to the number of employees that work there. 

## DepartmentDB

As mentioned above, there are 3 ways to modify a department's consumption:
- `billPower` which increases that department's consumption by the amount that has not been cleared yet. It modifies `totalPower` by the amount that gets billed
- `clearDepartment`: Clears a department's consumption. It modifies `clearedPower` and sets `totalPower` to 0.
- `fixedSplit` or `headcountSplit` which handle all necessary logic for forwarding a department's consumption to its delegates. It increases the department's delegates power by the matching amount and clears the department's consumption.

# Utilities

## Name Registry
Provides a mapping of names to addresses and reverse. `resolveName(bytes32)` returns a register contract's address while `resolve(address)` returns the name of a contranct at that address. This can be used to have a repository of addresses that dynamically resolve names to addresses.

## Access Control List
Cloned from [DAppHub](https://github.com/dapphub/ds-roles), this is an implementation fo a role-based access control list.
> It facilitates access to lists of user roles and capabilities. Works as a set of lookup tables for the canCall function to provide boolean answers as to whether a user is authorized to call a given function at given address.

DepartmentDB and MeterDB inherit from the [DSAuth](https://github.com/dapphub/ds-auth) contract and use the `auth` modifier whenever access control needs to be imposed. The identified roles and how they are setup per function call are explained in detail in the thesis.

# For Developers
Node Package Manager scripts are defined in `package.json`. 
Useful scripts are:
- `compile`: Compiles the contracts, code can be found under `build/contracts` directory
- `migrate:dev`: Deploys contracts to local testnet instance
- `migrate:prod`: Deploys contract to production network as configured in `truffle-config.js`
- `test`: Runs tests under `test/` directory
- `test:gas`: Runs tests under `test/` directory and prints gas consumption per test and per function call.

## Getting started
Get started by cloning the repository, installing the dependencies and running the tests. If tests did not complete successfully consider opening an issue!
```bash
git clone <URL>
npm install
npm run test
```

## Deploy and interact with the contracts
Running `npm run migrate:dev` will spin a ganache instance (with the accounts specified from the ganache script under `scripts/start_ganache.sh`. Afterwards, you can run `npm run console` which will launch an interactive truffle console. Example of interacting with a contract:

```bash
npm run migrate:dev
# ... wait for command output to finish ...
npm run console
# ... truffle framework console starts
truffle(rpc)> meterdb = MeterDB.at(MeterDB.address)
truffle(rpc)> meter = web3.eth.accounts[1]
truffle(rpc)> meterdb.activateMeter(meter, 'ELT01')
truffle(rpc)> meterdb.ping(123, 456, {from: meter})
```

## Use helper scripts to execute more complex functionality
Calling `truffle exec` on a javascript file meant to be used with truffle executes it directly from the commandline. In order to execute a binary that is installed as a local dependency you can use npx. 

```bash
npx truffle exec scripts/get_meter_readings.js --network rpc ELT01
```
Alternatively, the same can be done from the previously described truffle console.
```bash
truffle(rpc)> exec get_meter_readings.js
```
