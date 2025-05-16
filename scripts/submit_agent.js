const { ethers } = require("ethers");
require("dotenv").config();
const crypto = require("crypto");

// Contract artifacts
const escrowContractABI = require("../artifacts/contracts/EscrowContract.sol/EscrowContract.json").abi;

// Configuration
const ESCROW_CONTRACT_ADDRESS = process.env.ESCROW_CONTRACT_ADDRESS || "";
const PRIVATE_KEY = process.env.PRIVATE_KEY || "";
const RPC_URL = "https://rpc.testnet.bahamut.io";

// Sample agent CID (in real scenario, this would be the IPFS CID of the agent code)
const AGENT_CID = "hotpotqa_agent_v1";

// Function to calculate model hash
function calculateModelHash(modelName) {
  // In a real implementation, you would have a robust way to hash model information
  // For the MVP, we'll just hash the model name string
  return "0x" + crypto.createHash("sha256").update(modelName).digest("hex");
}

async function submitAgent() {
  // Connect to provider and wallet
  const provider = new ethers.JsonRpcProvider(RPC_URL);
  const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
  const escrowContract = new ethers.Contract(ESCROW_CONTRACT_ADDRESS, escrowContractABI, wallet);
  
  const bountyId = 0; // Assuming the first bounty with ID 0
  const modelName = "gpt-3.5-turbo"; // The model used in the agent
  const modelHash = calculateModelHash(modelName);
  
  console.log(`Submitting agent with CID: ${AGENT_CID}`);
  console.log(`Model hash: ${modelHash}`);
  
  try {
    // Submit the agent
    const tx = await escrowContract.submitAgent(bountyId, AGENT_CID, modelHash);
    
    console.log(`Transaction sent! Hash: ${tx.hash}`);
    
    // Wait for transaction to be mined
    const receipt = await tx.wait();
    
    console.log(`Agent submitted successfully in block ${receipt.blockNumber}`);
    console.log("The oracle will now evaluate your agent. If it passes the tests, you'll receive the reward.");
  } catch (error) {
    console.error("Error submitting agent:", error.message);
    
    // Check if the error is about model hash not being in allowed list
    if (error.message.includes("Model not in allowed list")) {
      console.log("\nERROR: The model hash is not in the allowed list.");
      console.log("Please ask the contract owner to add this model hash to the allowed list:");
      console.log(`Model hash: ${modelHash}`);
    }
  }
}

// Run the script
submitAgent().catch(error => {
  console.error("Unhandled error:", error);
  process.exitCode = 1;
}); 