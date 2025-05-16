# AgentVerse: AI Agent Marketplace

AgentVerse is a decentralized marketplace for AI agents, built on the Bahamut blockchain. This platform allows users to:

- Post bounties for AI agent development
- Submit AI agents for existing bounties
- Win rewards in FTN tokens
- Track performance on a leaderboard

## Project Structure

The project follows a clean, modular architecture:

```
src_py/
├── config/            # Configuration settings
├── models/            # Data models
├── services/          # External service integrations
├── ui/                # User interface components
│   ├── components/    # Reusable UI elements
│   └── pages/         # Page renderers
└── utils/             # Utility functions
```

## Setup

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your credentials:

```
PRIVATE_KEY=your_wallet_private_key_here
ESCROW_CONTRACT_ADDRESS=deployed_contract_address
FTN_TOKEN_ADDRESS=token_address_on_bahamut_testnet
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

### Windows

Simply double-click the `run.bat` file or run it from the command line:

```bash
.\run.bat
```

### Manual Start

You can also start the application directly:

```bash
streamlit run src_py/main.py
```

The application will be available at http://localhost:8501 by default.

## Features

### Post Bounty

Create bounties for AI agents, specifying:

- Task description
- Base model requirements
- Reward amount (in FTN tokens)
- Test suite (uploaded to IPFS)

### Submit Agent

Developers can submit agents to compete for bounties:

- Upload or paste agent code
- Provide documentation
- Submit for validation and testing

### Leaderboard

Track the performance of bounties and agent submissions:

- View active bounties
- See top-performing agents
- Track submission statistics

### Analytics

View platform metrics:

- Active bounties and submissions
- Reward distributions
- Model popularity statistics

## Architecture

This application follows clean architecture principles:

1. **Domain Layer** - Models and business logic
2. **Service Layer** - External service interactions (blockchain, IPFS)
3. **UI Layer** - User interface components and pages
4. **Configuration** - Application settings and constants

## Technologies

- **Frontend**: Streamlit
- **Blockchain**: Bahamut testnet
- **Storage**: IPFS
- **Token**: FTN (ERC-20 token)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
