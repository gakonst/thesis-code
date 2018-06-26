# Gas Comparison between `struct` and manually packing with a `Library`

Provides a comparison between Method 1 and Method 3 described in Chapter 3, and applied in Chapter 5 in the thesis _Decentralized Metering and Billing of Energy on
Ethereum with Respect to Scalability and Security_

## Install

`npm install`

## Results

For gas costs run each test separately as follows:

```bash
GAS_REPORTER=1 npx truffle test test/testDepartmentLibs.js
GAS_REPORTER=1 npx truffle test test/testDepartmentStructs.js
GAS_REPORTER=1 npx truffle test test/testMeterLibs.js
GAS_REPORTER=1 npx truffle test test/testMeterStructs.js
```

