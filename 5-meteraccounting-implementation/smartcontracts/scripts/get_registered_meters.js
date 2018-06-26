const MeterDB = artifacts.require('MeterDB')

function toAscii(input) {
    return web3.toAscii(input).replace(/\u0000/g, '');
}

module.exports = function(callback) { 

    const db = MeterDB.at(MeterDB.address);

    db.Activated({}, {fromBlock: 0, toBlock: 'latest' }).get( (err, res ) => {
        if (!err) {
            res.forEach(log => {
                // console.log(log)
                args = log.args;

                console.log('Meter', toAscii(args.meterId), 'registered at', args.meterAddress);

            });
        }
    });
}
