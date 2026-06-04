@echo off
title Market Story
cd /d "%~dp0"
rem Bare "python" resolves to the Microsoft Store stub on this machine (Anaconda isn't on
rem PATH), so the launcher must call the Anaconda interpreter by full path.
set "PY=%USERPROFILE%\anaconda3\python.exe"
if not exist "%PY%" set "PY=python"
echo.
echo   Starting the Market Story dashboard...
echo   A browser tab opens at http://localhost:8501 in a few seconds.
echo   Closing this window stops the dashboard.
echo.
"%PY%" -m streamlit run app.py --server.headless false --server.port 8501
