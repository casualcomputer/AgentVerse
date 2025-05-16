@echo off
echo Running database tests...

:: Set PYTHONPATH to include the parent directory
set PYTHONPATH=%CD%\..;%PYTHONPATH%

:: Run the tests
python -m unittest test_database.py -v

echo.
echo Press any key to exit...
pause > nul 