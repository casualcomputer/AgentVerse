contract EscrowWithDeadline {
  struct Bounty {
    address sponsor;
    uint256 reward;
    uint256 deadline;   // UNIX timestamp
    bool    paidOut;
  }
  mapping(uint256 => Bounty) public bounties;
  mapping(uint256 => address[]) public submissions;
  address public oracle;
  uint256 public nextId;

  modifier onlyOracle() { require(msg.sender == oracle, "Not oracle"); _; }

  event BountyPosted(uint256 id, address sponsor, uint256 reward, uint256 deadline);
  event AgentSubmitted(uint256 id, address agent);
  event BatchPaid(uint256 id, address[] winners, uint256 share);

  constructor(address _oracle) { oracle = _oracle; }

  function postBounty(uint256 _deadline) external payable returns (uint256 id) {
    require(_deadline > block.timestamp, "Deadline in future");
    id = nextId++;
    bounties[id] = Bounty(msg.sender, msg.value, _deadline, false);
    emit BountyPosted(id, msg.sender, msg.value, _deadline);
  }

  function submitAgent(uint256 id) external {
    Bounty storage b = bounties[id];
    require(block.timestamp < b.deadline, "Too late");
    submissions[id].push(msg.sender);
    emit AgentSubmitted(id, msg.sender);
  }

  // called _once_ by oracle after deadline
  function batchPayout(uint256 id, address[] calldata winners) external onlyOracle {
    Bounty storage b = bounties[id];
    require(block.timestamp >= b.deadline, "Too early");
    require(!b.paidOut, "Already paid");
    b.paidOut = true;
    uint256 share = b.reward / winners.length;
    for (uint i = 0; i < winners.length; i++) {
      payable(winners[i]).transfer(share);
    }
    emit BatchPaid(id, winners, share);
  }
}
