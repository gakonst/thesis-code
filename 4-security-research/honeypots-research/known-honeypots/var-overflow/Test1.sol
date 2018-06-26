// https://etherscan.io/address/0x791d0463b8813b827807a36852e4778be01b704e#code
/// On link 2 it is a honeypot but not for the reason you mention. The while loop should terminate when i2 grows larger than 1 eth, but it is declared as a var so will default to uint8. 1 eth = 1018 which means i2 will overflow before it gets there, and so the other break clause is triggered and you get paid out 255wei... what’s also interesting is whenever I see a honeypot (I’ve seen 2 other variants) there are also what look like automated attempts at triggering them - wonder if there are scripts out there calling any function that transfers ETH in the hope they’ll find an occasional bug. 
pragma solidity ^0.4.18;

contract Test1
{
    address owner = msg.sender;
    
    function withdraw()
    payable
    public
    {
        require(msg.sender==owner);
        owner.transfer(this.balance);
    }
    
    function() payable {}
    
    function Test()
    payable
    public
    {
        if(msg.value>=1 ether)
        {
            
            var i1 = 1;
            var i2 = 0;
            var amX2 = msg.value*2;
            
            while(true)
            {
                if(i1<i2)break;
                if(i1>amX2)break;
                
                i2=i1;
                i1++;
            }
            msg.sender.transfer(i2);
        }
    }
}
