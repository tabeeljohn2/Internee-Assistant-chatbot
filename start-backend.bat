@echo off
cd /d "%~dp0backend"
..\venv\Scripts\python.exe -m flask --app app.main run --port 5000 --debug
pause