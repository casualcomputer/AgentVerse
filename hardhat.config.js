require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();
require("@nomiclabs/hardhat-ethers");

const PRIVATE_KEY = process.env.PRIVATE_KEY || "0000000000000000000000000000000000000000000000000000000000000000";

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.19",
  networks: {
    hardhat: {},
    bahamut: {
      url: "https://rpc.testnet.bahamut.io/",
      accounts: ["0xYOUR_PRIVATE_KEY"] // Use a testnet wallet with FTN
    }
  }
};
