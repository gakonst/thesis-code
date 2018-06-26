contract Governmental {
  address public owner;
  address public lastInvestor;
  uint public jackpot = 1 ether;
  uint public lastInvestmentTimestamp;
  uint public ONE_MINUTE = 1 minutes;

  function Governmental() {
    owner = msg.sender;
    if (msg.value<1 ether) throw;
  }
  
  function invest() {
    if (msg.value<jackpot/2) throw;
    lastInvestor = msg.sender;
    jackpot += msg.value/2;
    lastInvestmentTimestamp = block.timestamp;
  }
  
  function resetInvestment() {
    if (block.timestamp < lastInvestmentTimestamp+ONE_MINUTE)
      throw;
      
    lastInvestor.send(jackpot);    
    owner.send(this.balance-1 ether);
    
    lastInvestor = 0;
    jackpot = 1 ether;
    lastInvestmentTimestamp = 0;
  }
}
