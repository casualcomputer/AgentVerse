# AgentVerse

AgentVerse is a decentralized platform where organizations post bounties for AI agents, and developers compete to build and submit solutions. Think of it as Fiverr meets Kaggle, but for verifiable, domain-specific AI agents—built openly and rewarded in crypto.

## Problem

Companies need custom AI agents for specific domains but struggle to:

1. Find qualified AI engineers
2. Verify agent quality objectively
3. Streamline payments across borders

Meanwhile, AI engineers want to:

1. Get paid for their skills
2. Work on diverse real-world challenges
3. Access fair compensation regardless of location

## Solution

AgentVerse connects businesses with AI engineers through:

1. **On-chain bounties** - Companies post requirements with cryptocurrency rewards
2. **Automated verification** - Test suites objectively evaluate agent quality
3. **Trustless rewards** - Smart contracts automatically release payment for successful submissions

## Quick Setup

### Prerequisites

- Node.js 16+
- Python 3.9+
- A wallet with Bahamut testnet FTN tokens

### Installation

1. Clone this repository

```
git clone https://github.com/yourusername/AgentVerse.git
cd AgentVerse
```

2. Install JavaScript dependencies

```
npm install
```

3. Install Python dependencies

```
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`

```
cp .env.example .env
# Edit .env with your private key and other settings
```

### Deployment

1. Deploy the smart contract to Bahamut testnet

```
npx hardhat run scripts/deploy.js --network bahamut_testnet
```

2. Update the `.env` file with the deployed contract address

### Running the Application

1. Start the oracle service

```
node scripts/oracle.js
```

2. Run the Streamlit interface

```
streamlit run streamlit_app.py
```

## Project Structure

- `/contracts` - Smart contracts for bounty escrow and reward distribution
- `/scripts` - Deployment and oracle scripts
- `/agent.py` - Example CrewAI agent (Tax FAQ bot)
- `/tests` - Agent verification tests
- `streamlit_app.py` - User interface for posting bounties and viewing leaderboard

## How It Works

1. **Post Bounty** - Companies post a bounty with a description and FTN token reward
2. **Submit Agent** - Developers build and submit AI agents using CrewAI
3. **Automated Testing** - Oracle runs test suite against the submitted agent
4. **Reward Distribution** - Smart contract automatically releases payment to winning solutions

## License

MIT
