# AI Agent Marketplace

A decentralized marketplace for AI agents built on the Bahamut blockchain. This platform allows users to post bounties for AI agents, submit their solutions, and earn rewards in FTN tokens.

## Features

- 🎯 Post bounties for AI agent development
- 🤖 Submit AI agent solutions
- 💰 Earn rewards in FTN tokens
- 📊 Real-time analytics and leaderboard
- 🔒 Secure and transparent blockchain integration
- 📝 Comprehensive documentation and testing tools

## Architecture

The application follows a modular design pattern with clear separation of concerns:

```
app/
├── components/         # UI components
│   └── bounty_form.py
├── services/          # Business logic services
│   ├── blockchain.py
│   └── ipfs.py
├── config.py          # Configuration settings
└── main.py           # Main application entry point
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-agent-marketplace.git
cd ai-agent-marketplace
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:

```env
BLOCKCHAIN_RPC_URL=your_rpc_url
CONTRACT_ADDRESS=your_contract_address
PRIVATE_KEY=your_private_key
IPFS_HOST=your_ipfs_host
IPFS_PORT=your_ipfs_port
```

5. Run the application:

```bash
streamlit run app/main.py
```

## Development

### Adding New Features

1. Create new components in `app/components/`
2. Add new services in `app/services/`
3. Update configuration in `app/config.py`
4. Integrate new features in `app/main.py`

### Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
