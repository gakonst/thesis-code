pragma solidity ^0.4.21;


library Department {

    /** Virtual Struct
     *  Type        Name          Index         Bits
     * bool      active             0            1
     * uint7     headcount          1            7
     * uint80    power              8            80
     * uint80    delegatedPower     88           80
     * uint80    clearedPower       168          248
     *    Total = 248 bits = 31 bytes~
     */

    /**Here we create bit masks for all of our funky data sizes*/
    uint private constant mask1         =  1;                //binary 1
    uint private constant mask7         = (1 << 7) - 1;     //binary ...
    uint private constant mask80        = (1 << 80) - 1;     //binary ...

    /**Here we create shift indices for each property. It is simply 1 shifted left by the Index listed above.*/
    uint private constant _active = 1 << 0;
    uint private constant _headcount = 1 << 1;
    uint private constant _power = 1 << 8;
    uint private constant _delegatedPower  = 1 << 88;
    uint private constant _clearedPower  = 1 << 168;


    /**Generic Getter/Setter which does the bit magic.*/
    function getProperty(bytes32 DepartmentData, uint mask, uint shift)
        private
        pure
        returns (uint property)
    {
        property = mask & ( uint(DepartmentData) / shift );
    }

    function setProperty(
        bytes32 DepartmentData,
        uint mask,
        uint shift,
        uint value
    )
        private
        pure
        returns (bytes32 updated)
    {
        updated = bytes32((~(mask*shift) & uint(DepartmentData)) | ((value & mask) * shift));
    }

    /// SETTER FUNCTIONS
    function activateDepartment(bytes32 DepartmentData)
        internal
        pure
        returns (bytes32)
    {
        return setProperty(DepartmentData, mask1, _active, 1);
    }

    function deactivateDepartment(bytes32 DepartmentData)
        internal
        pure
        returns (bytes32)
    {
        return setProperty(DepartmentData, mask1, _active, 0);
    }


    function setHeadcount(bytes32 DepartmentData, uint8 headcount)
        internal
        pure
        returns (bytes32)
    {
        return setProperty(DepartmentData, mask7,  _headcount, headcount);
    }

    function setPower(bytes32 DepartmentData, uint80 power)
        internal
        pure
        returns (bytes32)
    {
        return setProperty(DepartmentData, mask80,  _power, power);
    }

    // Delegated power can be modified by many sources, so we do not set it but we increase it.
    function increaseDelegatedPower(bytes32 DepartmentData, uint80 power)
        internal
        pure
        returns (bytes32)
   {
       // get current power and increase it
       uint80 currentPower = getDelegatedPower(DepartmentData);
       return setProperty(DepartmentData, mask80,  _delegatedPower, currentPower + power);

   }

    // Cleared power can be modified by many sources, so we do not set it but we increase it.
    function increaseClearedPower(bytes32 DepartmentData, uint80 power)
        internal
        pure
        returns (bytes32)
   {
       // get current power and increase it
       uint80 currentPower = getClearedPower(DepartmentData);
       return setProperty(DepartmentData, mask80,  _clearedPower, currentPower + power);
   }

    /// GETTER FUNCTIONS
    function isActive(bytes32 DepartmentData)
        internal
        pure
        returns (bool)
    {
        return (getProperty(DepartmentData, mask1, _active) == 1);
    }

    function getHeadcount(bytes32 DepartmentData)
        internal
        pure
        returns (uint8)
    {
        return uint8(getProperty(DepartmentData, mask7, _headcount));
    }

    function getPower(bytes32 DepartmentData)
        internal
        pure
        returns (uint80)
    {
        return uint80(getProperty(DepartmentData, mask80, _power));
    }

    function getDelegatedPower(bytes32 DepartmentData)
        internal
        pure
        returns (uint80)
    {
        return uint80(getProperty(DepartmentData, mask80, _delegatedPower));
    }

    function getClearedPower(bytes32 DepartmentData)
        internal
        pure
        returns (uint80)
    {
        return uint80(getProperty(DepartmentData, mask80, _clearedPower));
    }

}

