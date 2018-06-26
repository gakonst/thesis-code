// https://etherscan.io/address/0x73388dc2f89777cbdf53e5352f516cd703d070a6#code
// only if know the password
contract SimplePrize {
    bytes32 public constant salt = bytes32(987463829);
    bytes32 public commitment;

    function SimplePrize(bytes32 _commitment) public payable {
        commitment = _commitment;   
    }

    function createCommitment(uint answer) 
      public pure returns (bytes32) {
        return keccak256(salt, answer);
    }

    function guess (uint answer) public {
        require(createCommitment(answer) == commitment);
        msg.sender.transfer(this.balance);
    }

    function () public payable {}
}
