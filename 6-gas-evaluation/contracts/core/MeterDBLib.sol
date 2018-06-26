pragma solidity ^0.4.21;


import '../libs/Meter.sol';

/**
 * @title MeterDB
 * @dev This contract stores the energy values for all meters
 */

contract MeterDBLib {
    using Meter for bytes32;

    /* Events */
    event Activated(address indexed meterAddress, bytes8 indexed meterId);
    event Deactivated(address indexed meterAddress);
    event Pinged(address indexed meterAddress, bytes8 indexed meterId, uint48 power, uint32 timestamp);

    /* Storage */
    mapping (address => bytes32) public meters;
    mapping (bytes8 => address) public meterAddressById;
    address[] public meterAddresses;

    /* Modifiers */
    modifier onlyMeter() {
        require(isActive(msg.sender));
        _;
    }

    /// @dev Checks if an address is registered as a meter
    /// @param _address the address to check
    /// @return active True if a meter is activated by an operator
    function isActive(address _address) public view returns (bool active) {
        active = meters[_address].isActive();
        return active;
    }

    /* Functions */

    /// @dev allows an authorized operator to enable multiple meters
    /// @param _addresses array of addresses of the meters to be enabled
    /// @param _ids array of identifier of the meters to be enabled 
    function activateMeterBatch(address[] _addresses, bytes8[] _ids) public {
        uint length = _addresses.length;
        require(length == _ids.length);

        for (uint i=0; i< length; i++) {
            activateMeter(_addresses[i], _ids[i]);
        }
    }

    /// @dev allows an authorized operator to enable a meter
    /// @param _address The address of the meter to be enabled
    /// @param _id The identifier of the meter to be enabled (ELTXX, VMXX, KMZXX in our case)
    function activateMeter(address _address, bytes8 _id) public {
       require(!isActive(_address)); 
       bytes32 meter = meter.activateMeter();
       meter = meter.setId(_id);

       meters[_address] = meter;
       meterAddresses.push(_address);
       meterAddressById[_id] = _address;

       emit Activated(_address, _id);
    }

    /// @dev allows an authorized operator to disable a meter
    /// @param _address The address of the meter to be disabled
    function deactivateMeter(address _address) external  {
        require(isActive(_address)); 
        delete meters[_address];

        emit Deactivated(_address);
    }

    /// @dev Gets the consumption of a meter given an address
    /// @param _address The address of the meter to inspect
    /// @return id The meter id
    /// @return power The meter power consumption
    /// @return timestamp The timestamp at which the power reading was stored
    function getCurrentMeterData(address _address) public view returns (bytes8, uint48, uint32) {
        bytes32 meter = meters[_address];
        return (
            meter.getId(),
            meter.getCurrentPower(),
            meter.getCurrentTimestamp()
       );
    }

    /// @dev Gets the consumption of a meter given an id
    /// @param _id The id of the meter to inspect
    /// @return id The meter id
    /// @return power The meter power consumption
    /// @return timestamp The timestamp at which the power reading was stored
    function getCurrentMeterDataById(bytes8 _id) external view returns (bytes8, uint48, uint32) {
        return getCurrentMeterData(meterAddressById[_id]);
    }

    /// @dev Pings the consumption of a meter at a given timestamp
    /// @param power The power consumption **in kWh** -- subject to change, depends on client implementation
    /// @param timestamp The timestamp in **seconds**
    function ping(uint48 power, uint32 timestamp) external onlyMeter {
        meters[msg.sender] = meters[msg.sender].setPower(power).setTimestamp(timestamp);
        emit Pinged(msg.sender, meters[msg.sender].getId(), power, timestamp);
    }

}
