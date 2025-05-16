const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const contractAddress = process.argv[2];
  const bountyId = process.argv[3];

  const EscrowContract = await hre.ethers.getContractAt("EscrowContract", contractAddress);
  const tx = await EscrowContract.submitAgent(bountyId);
  await tx.wait();
  console.log("Agent submitted! Tx hash:", tx.hash);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); 