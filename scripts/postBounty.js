const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const contractAddress = process.argv[2];
  const description = process.argv[3];
  const reward = hre.ethers.parseEther("1.0"); // 1 FTN
  const deadline = Math.floor(Date.now() / 1000) + 86400; // 24h from now

  const EscrowContract = await hre.ethers.getContractAt("EscrowContract", contractAddress);
  const tx = await EscrowContract.postBounty(deadline, { value: reward });
  await tx.wait();
  console.log("Bounty posted! Tx hash:", tx.hash);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); 