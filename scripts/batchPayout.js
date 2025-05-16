const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const contractAddress = process.argv[2];
  const bountyId = process.argv[3];
  const winnersArg = process.argv[4];
  const winners = winnersArg.split(",");

  const EscrowContract = await hre.ethers.getContractAt("EscrowContract", contractAddress);
  const tx = await EscrowContract.batchPayout(bountyId, winners);
  await tx.wait();
  console.log("Batch payout complete! Tx hash:", tx.hash);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); 