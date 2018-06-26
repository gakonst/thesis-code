const _ = require('lodash')
const AccountingDB = artifacts.require("./AccountingDBLib.sol");

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

    let SPLIT = 50; // PERCENTAGE!

    let HREAdmin = "HRE::Admin";

    it("Activates the 4 departments and sets the headcounts", async function() {
        db = await AccountingDB.new();


        await db.activateDepartment(HRE2W);
        await db.setHeadcount(HRE2W, HRE2W_Headcount);

        await db.activateDepartment(HRE4W);
        await db.setHeadcount(HRE4W, HRE4W_Headcount);

        await db.activateDepartment(HREPP);
        await db.setHeadcount(HREPP, HREPP_Headcount);

        await db.activateDepartment(Genteki4W);

        await db.activateDepartment(HREAdmin);
        await db.setDelegates(HREAdmin, [HRE2W, HRE4W, HREPP]);

        await db.activateDepartment(HRE2WGenteki);
        await db.setDelegates(HRE2WGenteki, HRE2WGenteki_Delegates);

        await db.billPower(HRE2WGenteki, 30000);
        await db.billPower(HREAdmin, 10000);

        await db.headcountSplit(HREAdmin);
        await db.fixedSplit(HRE2WGenteki, SPLIT);

        // console.log(await db.getDepartmentData(HRE2W));
    });


});
