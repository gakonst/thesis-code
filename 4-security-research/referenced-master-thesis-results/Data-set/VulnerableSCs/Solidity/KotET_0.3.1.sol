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
    owner.send(amount);
  }  

  function() {     
    if (msg.value < claimPrice) throw;
    
    uint compensation = calculateCompensation();     
    king.send(compensation);  
    king = msg.sender;        
    claimPrice = calculateNewPrice();    
  }  
  
  function calculateCompensation() private returns(uint) {
    return claimPrice+100;
  }
  
  function calculateNewPrice() private returns(uint) {
    return msg.value+100;
  }
}