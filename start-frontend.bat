@echo off
cd /d "%~dp0frontend"
..\venv\Scripts\python.exe -m http.server 3000
pause