Write-Host "Running database tests..." -ForegroundColor Green

# Set PYTHONPATH to include the parent directory
$env:PYTHONPATH = "$PSScriptRoot\..;$env:PYTHONPATH"

# Run the tests
python -m unittest test_database.py -v

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 