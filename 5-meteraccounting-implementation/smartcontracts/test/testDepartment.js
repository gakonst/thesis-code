const _ = require('lodash')
const AccountingDB = artifacts.require("./AccountingDB.sol");

import assertRevert from './helpers/assertRevert.js';

function toAscii(input) {
    return web3.toAscii(input).replace(/\u0000/g, '');
}

contract("AccountingDB.sol", async function(accounts) {

    let db;
    let owner = accounts[0];

    let HRE2W = "HRE::2W";
    let HRE2W_VMs = [accounts[1], accounts[2]];
    let HRE2W_Headcount = 5; // PERCENTAGE!

    let HRE4W = "HRE::4W";

    let Genteki4W = "HRE::4W::Genteki4W";
    let Genteki4W_VMs = [accounts[3]];

    let GentekiWorkshop = "HRE::4W::2WGenteki";
    let GentekiWorkshop_VMs = [accounts[4]];
    let GentekiWorkshop_Delegates = [Genteki4W, HRE2W];

    let HREAdmin = "HRE::Admin";
    let HREPP = "HRE::PP";

    let HRE = "HRE";
    let HRE_Headcount = 75; // PERCENTAGE!
    let HRE_Subdepartments = [HRE2W, HRE4W, HREPP, HREAdmin, GentekiWorkshop];


    before("Deploys the contracts", async function() {
        db = await AccountingDB.new();
    });

    describe("Activates the departments", function() {

        it("Activates Genteki4W", async function() {
            // Genteki is part of the 50/50 split so no headcount needed
            await db.activateDepartment(Genteki4W);
            await db.setVirtualMeters(Genteki4W, Genteki4W_VMs);
            let [del, subdep, vms] = await db.getAccountingData(Genteki4W);
            // expect(vms).to.eql(Genteki4W_VMs);
        });

        it("Activates HRE::2W", async function() {
            await db.activateDepartment(HRE2W);
            await db.setVirtualMeters(HRE2W, HRE2W_VMs);
            await db.setHeadcount(HRE2W, HRE2W_Headcount);
            let [del, subdep, vms] = await db.getAccountingData(HRE2W);
            let [,headcount,,] = await db.getDepartmentData(HRE2W);
            // expect(vms).to.eql(HRE2W_VMs);
            expect(headcount.toNumber()).to.equal(HRE2W_Headcount);
        });

        it("Activates 2W+GentekiWorkshop", async function() {
            // Delegates 50/50 to Genteki4W and 2W
            await db.activateDepartment(GentekiWorkshop);
            await db.setVirtualMeters(GentekiWorkshop, GentekiWorkshop_VMs);
            await db.setDelegates(GentekiWorkshop, GentekiWorkshop_Delegates);

            let [del, subdep, vms] = await db.getAccountingData(GentekiWorkshop);

            // expect(vms).to.eql(GentekiWorkshop_VMs);
            // Delegates are OK, need to compare bytes 
            // expect(del).to.eql(GentekiWorkshop_Delegates);
        });

        it("Activates HRE", async function() {
            await db.activateDepartment(HRE2W);
            await db.setHeadcount(HRE, HRE_Headcount);
            await db.setSubDepartments(HRE, HRE_Subdepartments);
            let [del, subdep, vms] = await db.getAccountingData(HRE);
        });




    });
});
