@echo off
echo Starting AgentVerse application...

:: Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found. Please create one first.
    echo Example contents:
    echo PRIVATE_KEY=your_wallet_private_key_here
    echo ESCROW_CONTRACT_ADDRESS=deployed_contract_address
    echo FTN_TOKEN_ADDRESS=token_address_on_bahamut_testnet
    echo OPENAI_API_KEY=your_openai_api_key_here
    exit /b 1
)

echo Starting Oracle service...
start "Oracle Service" cmd /c "node scripts/oracle.js"

echo Starting Streamlit interface...
start "Streamlit Interface" cmd /c "streamlit run streamlit_app.py"

echo AgentVerse is now running! 
echo Oracle service is listening for agent submissions
echo Web interface is available at http://localhost:8501
echo.
echo Press Ctrl+C to stop the services when done. 