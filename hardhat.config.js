require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "0000000000000000000000000000000000000000000000000000000000000000";

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    hardhat: {},
    bahamut_testnet: {
      url: "https://rpc.testnet.bahamut.io",
      accounts: [PRIVATE_KEY],
      chainId: 9610
    }
  }
};
