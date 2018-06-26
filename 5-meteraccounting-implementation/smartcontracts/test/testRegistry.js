const _ = require('lodash')
const Registry = artifacts.require("./Registry.sol");
const Authority = artifacts.require('./DSRoles.sol');

import assertRevert from './helpers/assertRevert.js';

function toAscii(input) {
    return web3.toAscii(input).replace(/\u0000/g, '') 
}

contract("Registry.sol", async function(accounts) {

    let registry, authority;
    let [owner, meterdb, registryOperator, random] = accounts;
    let _registryOperator = 254;

    let meterdb_id =  "meterdb.honda@0.1";
    before("Deploys the contracts", async function() {
        registry = await Registry.new();
        authority = await Authority.new();

        registry.setAuthority(authority.address);

        authority.setUserRole(registryOperator, _registryOperator, true);
    });

    describe("Tests Activation and deactivation", function() {

        it("Gives the Registry Operator permissions to enable/disable contracts", async function() {
            let enableSig = web3.sha3('enable(address,bytes32)').slice(0,10);
            let disableSig = web3.sha3('disable(address)').slice(0,10);


            authority.setRoleCapability(_registryOperator, registry.address, enableSig, true);
            authority.setRoleCapability(_registryOperator, registry.address, disableSig, true);

            assert.equal(await authority.canCall(registryOperator, registry.address, enableSig), true);
            assert.equal(await authority.canCall(registryOperator, registry.address, disableSig), true);
        });

        it("Enables a contract as registrOperator", async function() {
            await registry.enable(meterdb, meterdb_id, {from: registryOperator});

            let ret_id 
                = await registry.resolve.call(meterdb);

            assert.equal(toAscii(ret_id), meterdb_id);

            let ret_address 
                 = await registry.resolveName.call(meterdb_id);

            assert.equal(ret_address, meterdb);
        });

        it("Fails to enable a contract as random user", async function() {
            assertRevert(registry.enable(meterdb, meterdb_id, {from: random}))
        });

        it("Disables a contract as registryOperator", async function() {
            await registry.disable(meterdb, {from: registryOperator});

            let ret_address 
                 = await registry.resolve.call(meterdb);

            assert.equal(ret_address, '0x0000000000000000000000000000000000000000000000000000000000000000');
        });

    });
});
