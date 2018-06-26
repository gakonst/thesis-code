const _ = require('lodash')
const AccountingDB = artifacts.require("./AccountingDB.sol");

contract("AccountingDB.sol", async function(accounts) {

    let db;
    let owner = accounts[0];

    let HRE2W = "HRE::2W";
    let HRE2W_Headcount = 5; // PERCENTAGE!

    let HRE4W = "HRE::4W";
    let HRE4W_Headcount = 75; // PERCENTAGE!

    let HREPP = "HRE::PP";
    let HREPP_Headcount = 20;

    let Genteki4W = "HRE::4W::Genteki4W";

    let HRE2WGenteki = "HRE::2WGenteki";
    let HRE2WGenteki_Delegates = [Genteki4W, HRE2W];

    let SPLIT = 50;

    let HREAdmin = "HRE::Admin";


    describe("Checks that headcount split works for HREAdmin -> PP/4W/2W", function() {

        before("Deploys the contracts", async function() {
            db = await AccountingDB.new();
        });

        it("Activates the 4 departments and sets the headcounts", async function() {
            // Genteki is part of the 50/50 split so no headcount needed
            await db.activateDepartment(HRE2W);
            await db.setHeadcount(HRE2W, HRE2W_Headcount);

            await db.activateDepartment(HRE4W);
            await db.setHeadcount(HRE4W, HRE4W_Headcount);

            await db.activateDepartment(HREPP);
            await db.setHeadcount(HREPP, HREPP_Headcount);

            await db.activateDepartment(HREAdmin);
            await db.setDelegates(HREAdmin, [HRE2W, HRE4W, HREPP])
        });

        it("Fills them with some power", async function() {
            await db.billPower(HRE2W, 30000)
            await db.billPower(HREPP, 50000)
            await db.billPower(HRE4W, 80000)
            await db.billPower(HREAdmin, 10000)

            let data;
            data = await db.getDepartmentData(HRE2W);
            assert.equal(data[2].toNumber(), 30000);
            data = await db.getDepartmentData(HREPP);
            assert.equal(data[2].toNumber(), 50000);
            data = await db.getDepartmentData(HRE4W);
            assert.equal(data[2].toNumber(), 80000);
            data = await db.getDepartmentData(HREAdmin);
            assert.equal(data[2].toNumber(), 10000);
        });

        it("Headcount split from Admin to the rest", async function() {
            await db.headcountSplit(HREAdmin);

            let data;
            data = await db.getDepartmentData(HRE2W);
            assert.equal(data[3].toNumber(), 10000 * HRE2W_Headcount / 100);
            data = await db.getDepartmentData(HRE4W);
            assert.equal(data[3].toNumber(), 10000 * HRE4W_Headcount / 100);
            data = await db.getDepartmentData(HREPP);
            assert.equal(data[3].toNumber(), 10000 * HREPP_Headcount / 100 );
            data = await db.getDepartmentData(HREAdmin);
            assert.equal(data[4].toNumber(), 10000);
        });
    });

    describe("Checks that fixed split works for 2WGentekiWorkshop -> Genteki4W+2W", async function() {

        before("Deploys the contracts", async function() {
            db = await AccountingDB.new();
        });

        it("Activates the 3 departments and sets the delegates", async function() {
            // Genteki is part of the 50/50 split so no headcount needed
            await db.activateDepartment(HRE2W);
            await db.activateDepartment(HRE2WGenteki);
            await db.activateDepartment(Genteki4W);
            await db.setDelegates(HRE2WGenteki, HRE2WGenteki_Delegates)
        });

        it("Fills them with some power", async function() {
            await db.billPower(HRE2WGenteki, 30000)
            let data = await db.getDepartmentData(HRE2WGenteki);
            assert.equal(data[2].toNumber(), 30000);
        });

        it("Fix splits from 2W+Workshop to the rest", async function() {
            await db.fixedSplit(HRE2WGenteki, SPLIT);

            let data;
            // Genteki4W was the first delegate so it gets `SPLIT`%
            data = await db.getDepartmentData(Genteki4W);
            assert.equal(data[3].toNumber(), 30000 * SPLIT / 100);

            // HRE2W was the second delegate so it gets `100-SPLIT`%
            data = await db.getDepartmentData(HRE2W);
            assert.equal(data[3].toNumber(), 30000 * (100-SPLIT) / 100);

            data = await db.getDepartmentData(HRE2WGenteki);
            assert.equal(data[4].toNumber(), 30000);
        });

    });


});
