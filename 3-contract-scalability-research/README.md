# Gas Comparison between Struct Tight Packing, Manual Uint Packing through masks and Manual byte packing through masks with libraries

This directory contains a comparison of the 3 methods described in Chapter 3 of the thesis _Decentralized Metering and Billing of Energy on Ethereum with Respect to scalability and security_.
Latex code of the results is exported in the `tex` directory, to be imported in a Latex report.

## Verify Results

1. Run an ethereum node instance, either by `ganache-cli` or by `geth --dev --rpc`
2. Run `python gas-tests.py config.ini contracts/GameByteMasking.sol contracts/GameTightlyPacked.sol contracts/GameUintMasking.sol`

