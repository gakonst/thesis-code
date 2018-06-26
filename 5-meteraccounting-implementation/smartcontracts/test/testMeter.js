const _ = require('lodash')
const MeterDB = artifacts.require("./MeterDB.sol");

import assertRevert from './helpers/assertRevert.js';


contract("MeterDB.sol", async function(accounts) {

    let db;
    let first_reading = 100; // 100 kWh
    let first_timestamp = parseInt(Date.now() / 1000);
    let second_reading = 200; // 200 kWh
    let second_timestamp = parseInt(Date.now() / 1000);
    let meterId = "U3.Z40.W";


    let meterIDs = ["A", "B", "C"]
    let [owner, operator, meter, m1, m2, m3] = accounts;

    before("Deploys the contracts", async function() {
        db = await MeterDB.new();
    });

    describe("Tests Library functionality", function() {

        it("Activates a meter and tests its initial values", async function() {
            await db.activateMeter(meter, meterId);

            let [returnedId, currentPower, currentTimestamp]
                = await db.getCurrentMeterData(meter);

            assert.equal(web3.toAscii(returnedId), meterId, "Meter id does not match");
            assert.equal(currentPower, 0, "Initial power should be 0");
            assert.equal(currentTimestamp, 0, "Initial timestamp should be 0");

        });

        it("Activates multiple meters", async function() {
            await db.activateMeterBatch([m1, m2, m3], meterIDs);

            let [returnedId, currentPower, currentTimestamp]
                = await db.getCurrentMeterData(m1);

            // need to strip \x00 from returnedd
            // assert.equal(web3.toAscii(returnedId), 'A', "Meter id does not match");
            assert.equal(currentPower, 0, "Initial power should be 0");
            assert.equal(currentTimestamp, 0, "Initial timestamp should be 0");

        });

        it("Tests setting the values", async function() {

            db.ping(first_reading, first_timestamp, {'from' : meter } );
            let [, currentPower, currentTimestamp]
                = await db.getCurrentMeterData(meter);

            assert.equal(currentPower.toNumber(), first_reading, "Reading should be equal to `first_reading`");
            assert.equal(currentTimestamp.toNumber(), first_timestamp, "Timestamp should be equal to `first_timestamp`");
        });

        it("Tests setting the values again.", async function() {

            db.ping(second_reading, second_timestamp, {'from' : meter } );
            let [, currentPower, currentTimestamp] = await db.getCurrentMeterData(meter);

            assert.equal(currentPower.toNumber(), second_reading, "Reading should be equal to `second_reading`");
            assert.equal(currentTimestamp.toNumber(), second_timestamp, "Timestamp should be equal to `second_timestamp`");

        });

        it("Gets meter data by its ID", async function() {
            let [returnedId, currentPower, currentTimestamp] = await db.getCurrentMeterDataById(meterId);
            assert.equal(web3.toAscii(returnedId), meterId, "Meter id does not match");
            assert.equal(currentPower.toNumber(), second_reading, "Reading should be equal to `second_reading`");
            assert.equal(currentTimestamp.toNumber(), second_timestamp, "Timestamp should be equal to `second_timestamp`");
        });

        it('Disables meter and tries pinging again', async function() {
            db.deactivateMeter(meter); // owner deactivates meter
            assertRevert(db.ping(second_reading, second_timestamp, {'from' : meter } ));
        });

    });

});

