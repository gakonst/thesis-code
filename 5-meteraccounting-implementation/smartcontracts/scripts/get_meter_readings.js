const MeterDB = artifacts.require('MeterDB')

function toAscii(input) {
    return web3.toAscii(input).replace(/\u0000/g, '');
}

module.exports = function(callback) { 

    meters = {} 
    if (process.argv[6]) { 
        meters = {"meterId" : process.argv[6]}
    }

    const db = MeterDB.at(MeterDB.address);
    // Get all events that match the `meterId` for the contract
    db.Pinged(meters, {fromBlock: 0, toBlock: 'latest' }).get( (err, res ) => {
        if (!err) {
            res.forEach(log => {
                // event Pinged(address indexed meterAddress, bytes8 indexed meterId, uint80 power, uint80 timestamp);
                args = log.args;
                power = args.power;
                timestamp = args.timestamp;
                meterId = args.meterId;

                console.log('Meter '+toAscii(meterId)+': '+power+' kWh at '+timestamp);
            });
        }
    });
}
