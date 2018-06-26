pragma solidity ^0.4.2;

contract KotET {   
  address public king;  
  uint public claimPrice = 100;
  address owner;

  function KotET() { 
    owner = msg.sender;  
    king = msg.sender;
    if (msg.value<1 ether) throw;
  }
   
  function sweepCommission(uint amount)  {
    bool res = owner.send(amount);
  }  

  function() payable {     
    if (msg.value < claimPrice) throw;
    
    uint compensation = calculateCompensation();     
    bool res = king.send(compensation);  
    king = msg.sender;        
    claimPrice = calculateNewPrice();    
  }  
  
  function calculateCompensation() private returns(uint) {
    return claimPrice+100;
  }
  
  function calculateNewPrice() private returns(uint) {
    return msg.value+200;
  }
}