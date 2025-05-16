const { ethers } = require("ethers");
const { spawn } = require("child_process");
require("dotenv").config();

// Contract artifacts
const escrowContractABI = require("../artifacts/contracts/EscrowContract.sol/EscrowContract.json").abi;

// Configuration
const ESCROW_CONTRACT_ADDRESS = process.env.ESCROW_CONTRACT_ADDRESS || ""; // Replace with deployed contract address
const PRIVATE_KEY = process.env.PRIVATE_KEY || "";
const RPC_URL = "https://rpc.testnet.bahamut.io";

// Connect to provider and wallet
const provider = new ethers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);
const escrowContract = new ethers.Contract(ESCROW_CONTRACT_ADDRESS, escrowContractABI, wallet);

console.log("Oracle started. Listening for AgentSubmitted events...");

// Listen for AgentSubmitted events
escrowContract.on("AgentSubmitted", async (bountyId, submitter, agentCID, modelHash, event) => {
  console.log(`\n--- New Agent Submission ---`);
  console.log(`Bounty ID: ${bountyId}`);
  console.log(`Submitter: ${submitter}`);
  console.log(`Agent CID: ${agentCID}`);
  console.log(`Model Hash: ${modelHash}`);
  
  try {
    // 1. Download/clone the agent code from IPFS or other storage using the CID
    console.log("Downloading agent code from IPFS...");
    // In a real implementation, you would pull the code using the CID
    // For the MVP, assume we have a local path for testing
    const agentPath = "./test_agents/" + agentCID;
    
    // 2. Run tests on the agent
    console.log("Running tests on agent...");
    const testResult = await runTests(agentPath);
    
    // 3. If tests pass with sufficient score, release the reward
    if (testResult.pass && testResult.score >= 80) {
      console.log(`Tests passed with score: ${testResult.score}%. Releasing reward...`);
      
      // Call the smart contract to release the reward
      const tx = await escrowContract.releaseReward(
        bountyId,
        submitter,
        agentCID,
        testResult.score
      );
      
      await tx.wait();
      console.log(`Reward released! Transaction hash: ${tx.hash}`);
    } else {
      console.log(`Tests failed or score too low: ${testResult.score}%. No reward released.`);
    }
  } catch (error) {
    console.error("Error processing agent submission:", error);
  }
});

// Function to run tests on the agent
async function runTests(agentPath) {
  return new Promise((resolve, reject) => {
    // Run pytest on the agent
    const pytest = spawn("python", ["-m", "pytest", "-xvs", `${agentPath}/tests/test_agent.py`]);
    
    let output = "";
    
    pytest.stdout.on("data", (data) => {
      output += data.toString();
      console.log(data.toString());
    });
    
    pytest.stderr.on("data", (data) => {
      console.error(data.toString());
    });
    
    pytest.on("close", (code) => {
      console.log(`pytest process exited with code ${code}`);
      
      if (code !== 0) {
        resolve({ pass: false, score: 0 });
        return;
      }
      
      // Parse test results to calculate score
      // This is a simple implementation - in a real system you'd want more robust parsing
      const score = parseScore(output);
      resolve({ pass: true, score });
    });
  });
}

// Simple function to parse test output and extract score
function parseScore(output) {
  // In a real implementation, you would parse the pytest output to calculate the score
  // For the MVP, just return a fixed score (80%) for tests that pass
  return 80;
}

// Handle errors and cleanup
process.on("SIGINT", async () => {
  console.log("Shutting down oracle...");
  process.exit(0);
});

// Error handling
process.on("uncaughtException", (error) => {
  console.error("Uncaught exception:", error);
}); 