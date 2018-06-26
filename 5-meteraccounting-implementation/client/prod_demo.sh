#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
    killall python3 # cleanup python instances
    echo "[-] Exited and killed all client processes"
    kill $(pgrep node) # cleanup node instance for next demo
}


# Setup Phase
./admin.py -c conf/acl-roles.json --action grant -f --debug
./meter-operator.py -c conf/prod/meters.json --fund --debug
./meter-operator.py -c conf/prod/virtual_meters.json --fund --debug
./accounting-operator.py -c conf/prod/department_config.json --init --debug

# Launches Meters
./multiple-meters.py -c conf/prod/meters.json --debug &
## need to sleep a few seconds until all meters have started pinging
echo 'Sleeping until meters have started pinging'
sleep 10
./multiple-virtualmeters.py -c conf/prod/virtual_meters.json --debug &

# Launches accountant to do billing
./accountant.py -c conf/prod/department_config.json --debug

