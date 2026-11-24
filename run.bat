@echo off
echo ===================================================
echo   Ejitas Luxury Fashion E-Commerce Server
echo ===================================================
echo Activating Python Virtual Environment...
call .\venv\Scripts\activate.bat
echo Starting FastAPI & Uvicorn Server at http://127.0.0.1:8000 ...
echo Swagger API Documentation available at http://127.0.0.1:8000/docs
echo.
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
