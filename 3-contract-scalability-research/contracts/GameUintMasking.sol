pragma solidity ^0.4.21;

contract GameUintMasking {

    uint[] public Characters;
    event PlayerRegistered(uint16 playerID, address player);
    event CharacterCreated(uint c, uint CharacterId);
    mapping(address => uint16) public player2ID;
    address[] registeredPlayers;


    function GameUintMasking() public {
        registeredPlayers.push(0x0);
    }

    function Register() public returns (uint16) {
        uint16 playerID = player2ID[msg.sender];
        require(playerID == 0 && registeredPlayers.length < 65535);

        playerID = uint16(registeredPlayers.length);
        registeredPlayers.push(msg.sender);
        player2ID[msg.sender] = playerID;
        emit PlayerRegistered(playerID, msg.sender);
        return playerID;
    }

	function CreateCharacter(
		uint256 creationTime,
		uint256 class,
		uint256 race,
		uint256 strength, 
		uint256 agility, 
		uint256 wisdom,
		uint256 metadata) 
		external 
    {
        uint16 playerID = player2ID[msg.sender];
        require(playerID != 0);

        uint c = uint256(playerID);
        c |= creationTime  <<  16;
        c |= class         <<  48;
        c |= race          <<  52;
        c |= strength      <<  56;
        c |= agility       <<  72;
        c |= wisdom        <<  88;
        c |= metadata      << 104;
        
        uint CharacterId = Characters.length;
        emit CharacterCreated(c, CharacterId);

        Characters.push(c);
    }

    function GetCharacterStats(uint256 index) 
        external view
        returns (
            uint16 playerID, 
            uint32 creationTime, 
            uint8 race, 
            uint8 class,
            uint16 strength,
            uint16 agility,
            uint16 wisdom,
            bytes18 metadata)
        {
        uint c = Characters[index];
        return (
            uint16(c),
            uint32(c >> 16), 
            uint8((c >> 48) & uint256(2**4-1)), 
            uint8((c >> 52) & uint256(2**4-1)),
            uint16(c >> 56),
            uint16(c >> 72),
            uint16(c>> 88),
            bytes18(c>>104)
           );
    }
}
