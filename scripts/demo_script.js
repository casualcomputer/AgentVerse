/**
 * Demo script for AgentVerse
 * 
 * This script initializes the demo environment by:
 * 1. Creating sample bounties on the Bahamut blockchain
 * 2. Submitting sample agents to those bounties
 * 
 * Usage: node scripts/demo_script.js
 */

const hre = require("hardhat");

async function main() {
  console.log("🚀 Initializing AgentVerse Demo Environment");
  
  const [deployer] = await hre.ethers.getSigners();
  console.log(`Using account: ${deployer.address}`);
  
  const contractAddress = process.env.ESCROW_CONTRACT_ADDRESS || "0xeA141c8B753Cc244745603412Ae731CB078Bac9d";
  console.log(`Contract address: ${contractAddress}`);
  
  // Load the contract
  const EscrowContract = await hre.ethers.getContractAt("EscrowContract", contractAddress);
  
  // Setup deadline for 24 hours from now
  const deadline = Math.floor(Date.now() / 1000) + 86400;
  const value = hre.ethers.parseEther("1.0"); // 1 FTN
  
  console.log("\n📋 Creating sample bounties...");
  
  // Post first bounty: Document Classifier
  console.log("1. Posting Document Classifier bounty...");
  let tx = await EscrowContract.postBounty(deadline, { value });
  let receipt = await tx.wait();
  console.log(`   ✅ Bounty posted! Tx: ${tx.hash}`);
  
  // Post second bounty: Text Summarization
  console.log("2. Posting Text Summarization bounty...");
  tx = await EscrowContract.postBounty(deadline, { value });
  receipt = await tx.wait();
  console.log(`   ✅ Bounty posted! Tx: ${tx.hash}`);
  
  // Post third bounty: Sentiment Analysis
  console.log("3. Posting Sentiment Analysis bounty...");
  tx = await EscrowContract.postBounty(deadline, { value });
  receipt = await tx.wait();
  console.log(`   ✅ Bounty posted! Tx: ${tx.hash}`);
  
  console.log("\n🤖 Submitting sample agents...");
  
  // Submit agents to first bounty
  console.log("1. Submitting agent to Document Classifier bounty...");
  tx = await EscrowContract.submitAgent(1);
  receipt = await tx.wait();
  console.log(`   ✅ Agent submitted! Tx: ${tx.hash}`);
  
  // Submit another agent
  console.log("2. Submitting another agent to Document Classifier bounty...");
  tx = await EscrowContract.submitAgent(1);
  receipt = await tx.wait();
  console.log(`   ✅ Agent submitted! Tx: ${tx.hash}`);
  
  console.log("\n🎉 Demo environment initialized successfully!");
  console.log("\nYou can now run the Streamlit UI to interact with the demo:");
  console.log("   streamlit run src_py/main.py");
  
  console.log("\n📝 Demo Steps:");
  console.log("1. Post a new bounty");
  console.log("2. Submit an agent to a bounty");
  console.log("3. View the leaderboard");
  console.log("4. Use the Oracle Dashboard to trigger payouts");
  
  console.log("\n📈 For the Hackathon Presentation:");
  console.log("1. Show the smart contract on Bahamut Explorer");
  console.log("   (https://horizon.ftnscan.com/address/" + contractAddress + ")");
  console.log("2. Show the whole platform flow from posting to payout");
  console.log("3. Explain how the oracle service works with the contract");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 