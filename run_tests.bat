@echo off
call venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;%CD%\src
pytest tests/
pause