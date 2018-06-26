pragma solidity ^0.4.21;

import '../libs/auth/DSAuth.sol';

/**
 * @title Registry
 * @dev Allows an operator to register a name for an address. Is used to retrieve a contract's address by its name
 */

contract Registry is DSAuth {

    /* Events */
    event Enabled(address indexed contractAddress, bytes32 indexed contractId);
    event Disabled(address indexed contractAddress, bytes32 indexed contractId);

    /* Storage */
    mapping (address => bytes32) public addressToID;
    mapping (bytes32 => address) public idToAddress;


    /* Public Functions */

    /// @dev Stores a contract id/address pair
    /// @param _address The address of the contract to be registered
    /// @param _id The id of the contract to be registered
    function enable(address _address, bytes32 _id) public auth {
        require(!isActive(_address));
        addressToID[_address] = _id;
        idToAddress[_id] = _address;

        emit Enabled(_address, _id);
    }

    /// @dev Stores multiple contract id/address pairs
    /// @param _addresses Array of addresses of the contracts to be registered
    /// @param _ids Array of ids of the contracts to be registered
    function enableBatch(address[] _addresses, bytes32[] _ids) external {
        uint length = _addresses.length;
        require(length == _ids.length);

        for (uint i=0; i<length; i++) {
            enable(_addresses[i], _ids[i]);
        }
    }

    /// @dev Deletes a contract from the registry
    /// @param _address the address of the contract to be deleted
    function disable(address _address) public auth {
        require(isActive(_address));

        bytes32 id = addressToID[_address];

        delete addressToID[_address];
        delete idToAddress[id];

        emit Disabled(_address, id);
    }

    /// @dev Resolves a contract's name given its address
    /// @param _address the address of the contract to be retrieved
    /// @return id the id of the contract
    function resolve(address _address) external view returns (bytes32) {
        return addressToID[_address];
    }

    /// @dev Resolves a contract's address given its id
    /// @param _id the id of the contract to be retrieved
    /// @return _address the address of the contract
    function resolveName(bytes32 _id) external view returns (address) {
        return idToAddress[_id];
    }

    /* Private Functions */

    function isActive(address _address) private view returns (bool active) {
        return addressToID[_address] != 0x0;
    }

}
