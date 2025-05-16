const hre = require("hardhat");
const crypto = require("crypto");

// Calculate model hash for allowed models
function calculateModelHash(modelName) {
  return "0x" + crypto.createHash("sha256").update(modelName).digest("hex");
}

async function main() {
  // You'll need to deploy or use an existing ERC20 token for FTN on Bahamut testnet
  // For the MVP, we can use a placeholder address and update it later
  const ftnTokenAddress = "0x0000000000000000000000000000000000000000"; // Replace with actual token address
  
  // Deploy the EscrowContract
  const EscrowContract = await hre.ethers.getContractFactory("EscrowContract");
  const escrow = await EscrowContract.deploy(ftnTokenAddress);

  await escrow.waitForDeployment();
  
  const address = await escrow.getAddress();
  console.log(`EscrowContract deployed to: ${address}`);
  
  // Add allowed model hashes
  const allowedModels = [
    "gpt-3.5-turbo",
    "gpt-4",
    "llama-2-7b",
    "claude-3-opus"
  ];
  
  for (const model of allowedModels) {
    const modelHash = calculateModelHash(model);
    await escrow.addAllowedModel(modelHash);
    console.log(`Added allowed model hash for ${model}: ${modelHash}`);
  }

  console.log("Deployment completed!");
  
  // Print instructions for next steps
  console.log("\n=== NEXT STEPS ===");
  console.log("1. Update your .env file with these values:");
  console.log(`ESCROW_CONTRACT_ADDRESS=${address}`);
  console.log("2. Deploy or use an existing ERC20 token as FTN");
  console.log("3. Update your .env file with the FTN token address");
  console.log("4. Start the oracle service: node scripts/oracle.js");
  console.log("5. Run the frontend: streamlit run streamlit_app.py");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); 