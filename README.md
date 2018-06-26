# Decentralized Metering and Billing of energy on Ethereum with respect to scalability and security

This is the repository containing all research and implemented code for the purposes of the thesis _Decentralized Metering and Billing of Energy on Ethereum with Respect to Scalability and Security_ which was authored by Georgios Konstantopoulos (@gakonst), for the Electrical and Computer Engineering Department of Aristotle University of Thessaloniki in collaboration with Honda Research & Development Europe Germany. 

## Thesis abstract:

> We leverage the power of the Ethereum blockchain and smart contracts to create a system that can transparently and securely perform metering of energy as well as perform accounting for the consumed energy based on specific business logic. The advantages and disadvantages of smart contracts are explored. Past literature on current scalability and security issues of smart contracts is studied. Contributions are made on scalability by proposing a method to make data storage on smart contracts more energycient. On security we utilize and augment the functionality of an auditing tool in order to analyze and identify vulnerabilities in smart contracts. We apply the gained insight and techniques on the described metering and billing use case in order to enhance its viability and robustness in production. Finally, we evaluate the ectiveness of the proposed scalability techniques and security bestpractices on the written smart contracts.

## Repository Overview

### 3-contract-scalability-research

Contains all the research made for Chapter 3 of the thesis on contract level scalability. Includes a set of smart contracts along with custom made deployment and testing scripts for the gas costs of each implementation.

### 4-security-research

Contains all the research done for Chapter 4 of the thesis on smart contract security. The smart contracts under the folder `referenced-master-thesis-results` are taken from https://github.com/DikaArdit/Master-Thesis. The contracts were tested to validate the effectiveness of the tool Slither on the referenced thesis' results.

### 5-meteraccounting-implementation

Contains the full implementation made for Chapter 5 of the thesis on decentralized metering and billing.

### 6-gas-evaluation

Contains a gas comparison between the proposed method from Chapter 3, applied on the use case from Chapter 5. 
