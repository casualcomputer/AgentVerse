# AgentVerse Demo Guide

This guide will help you demonstrate your AgentVerse project for the Bahamut track at the Consensus hackathon.

## 1. Setup

### Prerequisites

- Node.js (v16 or higher)
- Python 3.8+ with pip
- Hardhat
- Metamask with Bahamut network configured

### Install Dependencies

```bash
# Install JavaScript dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file with:

```
PRIVATE_KEY=your_private_key_here
ESCROW_CONTRACT_ADDRESS=0xeA141c8B753Cc244745603412Ae731CB078Bac9d
```

## 2. Prepare for Demo

### Initialize Demo Environment

This will create sample bounties and submissions to showcase:

```bash
# Run the demo initialization script
node scripts/demo_script.js
```

### Start the Applications

Start the components in different terminal windows:

```bash
# Terminal 1: Start the Streamlit UI
streamlit run src_py/main.py

# Terminal 2: Start the Oracle Service
python src_py/oracle_service.py
```

## 3. Demo Flow

Follow this sequence for a smooth hackathon presentation:

### A. Show Smart Contract (30 seconds)

1. Go to [Bahamut Explorer](https://horizon.ftnscan.com/address/0xeA141c8B753Cc244745603412Ae731CB078Bac9d)
2. Show the contract and key functions (postBounty, submitAgent, batchPayout)
3. Show past transactions to demonstrate working contract

### B. Post a Bounty (30 seconds)

1. Navigate to "Post Bounty" in the UI
2. Fill out bounty details:
   - Title: "Image Classification Agent"
   - Description: "Need an agent that can classify images into 10 categories"
3. Submit the bounty
4. Show the transaction confirmation and contract interaction

### C. Submit an Agent (30 seconds)

1. Navigate to "Submit Agent"
2. Select an existing bounty
3. Paste sample agent code:

```python
class Agent:
    def __init__(self):
        self.name = "ImageClassifier-v1"

    def predict(self, input_data):
        # Classification logic would go here
        return {"class": "dog", "confidence": 0.95}
```

4. Submit the agent
5. Show the transaction confirmation and contract interaction

### D. Oracle & Payouts (30 seconds)

1. Navigate to "Oracle Dashboard"
2. Authenticate as admin
3. Select a bounty to process
4. Select winning agent(s)
5. Trigger the payout
6. Show the transaction confirmation and contract interaction

### E. Wrap-up (30 seconds)

1. Explain how the system combines:
   - AI (agents for specific tasks)
   - Blockchain (Bahamut for trust, transparency, and payments)
   - Oracle (for off-chain evaluation)
2. Highlight the benefit to both companies and AI developers

## 4. Key Points to Emphasize

1. **Bahamut Integration**: Emphasize how you're using Bahamut for:

   - Smart contract deployment
   - Transparent bounty management
   - Secure payments

2. **AI + Blockchain**: Show how you've combined:

   - AI agent capabilities
   - Blockchain-based incentives
   - Trustless collaboration

3. **Real-world Utility**: Explain how this:

   - Helps companies find specialized AI agents
   - Helps AI developers monetize their skills
   - Creates new opportunities in the Bahamut ecosystem

4. **Technical Implementation**:
   - Smart contract for escrow and payouts
   - Python backend for agent evaluation
   - Streamlit UI for easy interaction

## 5. Troubleshooting

- **Transaction failing?** Check your PRIVATE_KEY and make sure you have FTN in your wallet
- **UI not connecting?** Make sure the contract address is correct in your `.env` file
- **Oracle not running?** Check Python dependencies and database connection

## 6. Presentation Resources

- **Bahamut Explorer**: https://horizon.ftnscan.com/
- **Contract Address**: 0xeA141c8B753Cc244745603412Ae731CB078Bac9d
- **Repository**: Your GitHub Repository Link
