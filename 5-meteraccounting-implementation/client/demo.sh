#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
    killall python3
    echo "[-] Exited and killed all processes"
}


# Setup Phase
./admin.py -c conf/acl-roles.json --action grant -f --debug
./meter-operator.py -c conf/demo/simple_meters.json --fund --debug
./meter-operator.py -c conf/demo/simple_virtualmeters.json --fund --debug
./accounting-operator.py -c conf/demo/simple_departments.json --init --debug

# Launches Meters
./multiple-meters.py -c conf/demo/simple_meters.json --debug &
./multiple-virtualmeters.py -c conf/demo/simple_virtualmeters.json --debug &

# Launches accountant to do billing
./accountant.py -c conf/demo/simple_departments.json --debug

