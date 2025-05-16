// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EscrowContract is ReentrancyGuard, Ownable {
    struct Bounty {
        address creator;
        uint256 amount;
        string description;
        bool isActive;
        address winner;
        string winningAgentCID;
        uint256 score;
    }

    IERC20 public ftnToken;
    mapping(uint256 => Bounty) public bounties;
    uint256 public bountyCount;
    mapping(bytes32 => bool) public allowedModelHashes;

    // Events
    event BountyPosted(uint256 indexed bountyId, address indexed creator, uint256 amount, string description);
    event AgentSubmitted(uint256 indexed bountyId, address indexed submitter, string agentCID, bytes32 modelHash);
    event RewardReleased(uint256 indexed bountyId, address indexed winner, uint256 amount, string winningAgentCID, uint256 score);

    constructor(address _ftnToken) Ownable(msg.sender) {
        ftnToken = IERC20(_ftnToken);
    }

    function addAllowedModel(bytes32 modelHash) external onlyOwner {
        allowedModelHashes[modelHash] = true;
    }

    function removeAllowedModel(bytes32 modelHash) external onlyOwner {
        allowedModelHashes[modelHash] = false;
    }

    function postBounty(uint256 amount, string calldata description) external nonReentrant {
        require(amount > 0, "Amount must be greater than 0");
        
        // Transfer tokens from creator to contract
        require(ftnToken.transferFrom(msg.sender, address(this), amount), "Token transfer failed");
        
        uint256 bountyId = bountyCount++;
        bounties[bountyId] = Bounty({
            creator: msg.sender,
            amount: amount,
            description: description,
            isActive: true,
            winner: address(0),
            winningAgentCID: "",
            score: 0
        });
        
        emit BountyPosted(bountyId, msg.sender, amount, description);
    }

    function submitAgent(uint256 bountyId, string calldata agentCID, bytes32 modelHash) external {
        require(bounties[bountyId].isActive, "Bounty is not active");
        require(allowedModelHashes[modelHash], "Model not in allowed list");
        
        emit AgentSubmitted(bountyId, msg.sender, agentCID, modelHash);
    }

    function releaseReward(uint256 bountyId, address winner, string calldata winningAgentCID, uint256 score) external onlyOwner nonReentrant {
        Bounty storage bounty = bounties[bountyId];
        require(bounty.isActive, "Bounty is not active");
        
        bounty.isActive = false;
        bounty.winner = winner;
        bounty.winningAgentCID = winningAgentCID;
        bounty.score = score;
        
        // Transfer tokens to winner
        require(ftnToken.transfer(winner, bounty.amount), "Token transfer failed");
        
        emit RewardReleased(bountyId, winner, bounty.amount, winningAgentCID, score);
    }

    function getBounty(uint256 bountyId) external view returns (
        address creator, 
        uint256 amount, 
        string memory description, 
        bool isActive, 
        address winner, 
        string memory winningAgentCID, 
        uint256 score
    ) {
        Bounty storage bounty = bounties[bountyId];
        return (
            bounty.creator, 
            bounty.amount, 
            bounty.description, 
            bounty.isActive, 
            bounty.winner, 
            bounty.winningAgentCID, 
            bounty.score
        );
    }
} 