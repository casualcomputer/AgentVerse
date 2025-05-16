@echo off
echo Starting AgentVerse application...

:: Check if .env file exists
if not exist .env (
    echo Creating sample .env file...
    echo PRIVATE_KEY=your_wallet_private_key_here > .env
    echo ESCROW_CONTRACT_ADDRESS=deployed_contract_address >> .env
    echo FTN_TOKEN_ADDRESS=token_address_on_bahamut_testnet >> .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
)

:: Navigate to the root directory and run the app
cd ..
echo Starting Streamlit interface...
streamlit run src_py/main.py

echo Press Ctrl+C to stop the services when done. 