# Implementation of Metering and Billing business logic

Contains all the implementation and business logic described in Chapter 5 of the thesis _Decentralized Metering and Billing of Energy on Ethereum with Respect to Scalability and Security_

## Setup
1. `cd smartcontracts` in `5-meteraccounting-implementation` directory
2. `npm install` to install dependencies
3. `cd client` in `5-meteraccounting-implementation` directory
4. `mkvirtualenv demo --python=/usr/bin/python3.6`
5. `pip install -r requirements.txt`

## Demo
1. `cd smartcontracts` in `5-meteraccounting-implementation` directory
2. `npm run migrate:dev` to deploy and initialize contracts
3. `cd client` in `5-meteraccounting-implementation` directory
4. `./demo.sh`

## Resources Monitoring
Monitoring the performance of the system can be done through `htop` through the following command: 

```bash
PID=$(pgrep demo.sh) && htop -p `pstree -p $PID | perl -ne 'push @t, /\((\d+)\)/g; END { print join ",", @t }'`}`
```
