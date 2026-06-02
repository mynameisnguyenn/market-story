@echo off
title Market Story
cd /d "%~dp0"
echo.
echo   Starting the Market Story dashboard...
echo   A browser tab will open at http://localhost:8501 in a few seconds.
echo   Leave this window open while you use the dashboard. Close it to stop.
echo.
python -m streamlit run app.py --server.headless false
pause
