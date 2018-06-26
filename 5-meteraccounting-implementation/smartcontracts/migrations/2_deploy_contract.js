const MeterDB = artifacts.require("./MeterDB.sol");
const AccountingDB = artifacts.require("./AccountingDB.sol");
const Registry = artifacts.require("./Registry.sol");
const Authority = artifacts.require('./DSRoles.sol');

module.exports = async function(deployer, network, accounts) {
    let aRegistryInstance;
    let aMeterDBInstance;
    let aAccountingDBInstance;
    let aAuthorityInstance;

    let [_aRegistryInstanceOperator, _aMeterDBInstanceOperator, _aAccountingOperator, _aAccountant] = [1,2,3,4];

    let enableSig = web3.sha3('enable(address,bytes32)').slice(0,10);
    let disableSig = web3.sha3('disable(address)').slice(0,10);

    let activateMeterSig = web3.sha3('activateMeter(address,bytes8)').slice(0,10);
    let deactivateMeterSig = web3.sha3('deactivateMeter(address)').slice(0,10);

    let activateDepartmentSig = web3.sha3('activateDepartment(bytes32)').slice(0,10);
    let deactivateDepartmentSig = web3.sha3('deactivateDepartment(bytes32)').slice(0,10);


    let setDelegatesSig = web3.sha3('setDelegates(bytes32,bytes32[])').slice(0,10);
    let setVirtualMetersSig = web3.sha3('setVirtualMeters(bytes32,bytes8[])').slice(0,10);
    let setSubDepartmentsSig = web3.sha3('setSubDepartments(bytes32,bytes32[])').slice(0,10);
    let setHeadcountSig = web3.sha3('setHeadcount(bytes32,uint8)').slice(0,10);

    let fixedSplitSig = web3.sha3('fixedSplit(bytes32,uint8)').slice(0,10);
    let headcountSplitSig = web3.sha3('headcountSplit(bytes32)').slice(0,10);
    let billPowerSig = web3.sha3('billPower(bytes32,uint80)').slice(0,10);
    let clearDepartmentSig = web3.sha3('clearDepartment(bytes32,uint80)').slice(0,10);

    // Migration shall deploy and link to 1 meter.
    return deployer.deploy(Authority)
        .then(() => Authority.deployed())
        .then(instance => {
            aAuthorityInstance = instance;
            console.log('Authority deployed at address: ' + instance.address);
            return deployer.deploy(Registry);
        })
    .then(() => Registry.deployed())
        .then((instance) => {
            aRegistryInstance = instance;
            console.log('Registry deployed at address: ' + instance.address);
            aRegistryInstance.setAuthority(aAuthorityInstance.address);


            aAuthorityInstance.setRoleCapabilityBatch(_aRegistryInstanceOperator, aRegistryInstance.address, [enableSig, disableSig], true);

            return deployer.deploy(MeterDB)
        })
    .then(() => MeterDB.deployed())
        .then((instance) => {
            aMeterDBInstance = instance;
            console.log('MeterDB deployed at address: ' + instance.address);
            aMeterDBInstance.setAuthority(aAuthorityInstance.address);

            aAuthorityInstance.setRoleCapabilityBatch(_aMeterDBInstanceOperator, 
                    aMeterDBInstance.address, 
                    [activateMeterSig, deactivateMeterSig], 
                    true);


            return deployer.deploy(AccountingDB)
        })
    .then(() => AccountingDB.deployed())
        .then((instance) => {
            aAccountingDBInstance = instance;
            console.log('AccountingDB deployed at address: ' + instance.address);
            aAccountingDBInstance.setAuthority(aAuthorityInstance.address);

            aAuthorityInstance.setRoleCapabilityBatch(
                    _aAccountingOperator,
                    aAccountingDBInstance.address, 
                    [activateDepartmentSig, deactivateDepartmentSig, 
                     setDelegatesSig, setVirtualMetersSig, 
                     setSubDepartmentsSig, setHeadcountSig], 
                    true
                    );

            aAuthorityInstance.setRoleCapabilityBatch(
                    _aAccountant, 
                    aAccountingDBInstance.address,
                    [fixedSplitSig, headcountSplitSig, 
                    billPowerSig, clearDepartmentSig], 
                    true
                    );

        }).then(() => {
            let ids = ['acl.hnd', 'metering.hnd', 'billing.hnd'];
            let addr = [
                aAuthorityInstance.address, 
                aMeterDBInstance.address, 
                aAccountingDBInstance.address
            ];
            aRegistryInstance.enableBatch(addr, ids);
        });
};

