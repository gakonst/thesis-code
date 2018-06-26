// https://etherscan.io/address/0x95d34980095380851902ccd9a1fb4c813c2cb639#code -> Log contract at: https://etherscan.io/address/0xf8681dad1ce4f1f414fb07fc07f81a3a82e91d8fkju

// thoughts on logger: https://www.reddit.com/r/ethdev/comments/7xu4vr/oh_dear_somebody_just_got_tricked_on_the_same/dubakau/
// https://etherscan.io/address/0xd116d1349c1382b0b302086a4e4219ae4f8634ff#code


// https://www.reddit.com/r/ethereum/comments/7xvoui/exposing_ethereum_honeypots/
// For anyone not familiar with the interworkings of the DAO hack, the line msg.sender.call.value sends the remaining gas with the call function, whereas msg.sender.send(value) only sends a fixed stipend of 2300 gas. Normally, msg.sender would be a typical wallet address, but in the case where it is a smart contract address the fallback function is invoked. The key here is that the ether being sent is not subtracted from the balance until after it is sent. If it was subtracted before, this recursive attack would not work. So all the fallback function has to do is call the withdraw function and add in logic to make sure it doesn't take more ether than the contract holds.

// So what's wrong here? The answer lies in the TransferLog.AddMessage call. You may have noticed that the Log contract source was posted to etherscan, only that wasn't the real source code. Notice how the contstructor of PrivateBank sets the address of the real Log contract. All the creator of this contract had to do was make sure that the real Log contract had a function with the same signature as the AddMessage function posted. The real source code probably looks something like: 

// function AddMessage(address _sender, uint256 _amount, string _message) {
//         // note that this is not valid solidity
//             require(_sender == owner || _message == "Deposit");
//                 // and so on ... 
// }
// 
// This translates to: if the sender isn't me or someone isn't depositing ether then fail, which will revert all state changes, thus never allowing you to withdraw your ether.

pragma solidity ^0.4.19;

contract Private_Bank
{
    mapping (address => uint) public balances;
    
    uint public MinDeposit = 1 ether;
    
    Log TransferLog;
    
    function Private_Bank(address _log)
    {
        TransferLog = Log(_log);
    }
    
    function Deposit()
    public
    payable
    {
        if(msg.value >= MinDeposit)
        {
            balances[msg.sender]+=msg.value;
            TransferLog.AddMessage(msg.sender,msg.value,"Deposit");
        }
    }
    
    function CashOut(uint _am)
    {
        if(_am<=balances[msg.sender])
        {
            
            if(msg.sender.call.value(_am)())
            {
                balances[msg.sender]-=_am;
                TransferLog.AddMessage(msg.sender,_am,"CashOut");
            }
        }
    }
    
    function() public payable{}    
    
}

contract Log 
{
   
    struct Message
    {
        address Sender;
        string  Data;
        uint Val;
        uint  Time;
    }
    
    Message[] public History;
    
    Message LastMsg;
    
    function AddMessage(address _adr,uint _val,string _data)
    public
    {
        LastMsg.Sender = _adr;
        LastMsg.Time = now;
        LastMsg.Val = _val;
        LastMsg.Data = _data;
        History.push(LastMsg);
    }
}
