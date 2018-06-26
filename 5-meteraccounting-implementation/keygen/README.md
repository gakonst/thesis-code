# Meter/Billing Key Generation

Scripts for config file generation of meters and accounts for the purposes of the thesis _Decentralized Meter and Billing on Ethereum with respect to Security and Scalability_.

**ATTENTION. Unaudited cryptography and key generation! Do not use in production!**

## Meters 
Each meter is defined by its ID, and by its private/public keypair. In addition, if a meter is a _virtual meter_, it includes a formula which specifies the meters it is associated with and how to calculate its total consumption. 

Files under `lists` folders include meter ids in `meters.list` for simple meters. In `eq_virtual_meters.list` the equations for each virtual meter are provided.

## Accounts

The identified roles for the purpose of the thesis are Registry Operator, Meter Operator, Accounting Operator and Accountant. Keypairs are generated for each file from the `roles.list` file. 

## Usage
`./keygen.py -i lists/meters.list`
`./keygen.py -i lists/roles.list`
`./keygen_virtualmeters.py -i lists/eq_virtual_meters.list`


