


const _ = require('lodash')

const MeterDB = artifacts.require("./MeterDBStructs.sol");

import assertRevert from './helpers/assertRevert.js';


contract("MeterDB.sol", async function(accounts) {

    let db;
    let first_reading = 100; // 100 kWh
    let first_timestamp = parseInt(Date.now() / 1000);
    let second_reading = 200;
    let second_timestamp = parseInt(Date.now() / 1000);
    let meterId = "U3.Z40.W";

    let [owner, operator, meter, m1, m2, m3] = accounts;

    it("Activates a meter and pigns a value", async function() {
        db = await MeterDB.new();
        await db.activateMeter(meter, meterId);
        await db.ping(first_reading, first_timestamp, {'from' : meter } );
        await db.ping(second_reading, second_timestamp, {'from' : meter } );
    });

}); 

