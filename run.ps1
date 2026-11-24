Write-Host "===================================================" -ForegroundColor Magenta
Write-Host "  Ejitas Luxury Fashion E-Commerce Server" -ForegroundColor Gold
Write-Host "===================================================" -ForegroundColor Magenta
Write-Host "Activating Python Virtual Environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"
Write-Host "Starting FastAPI & Uvicorn Server at http://127.0.0.1:8000 ..." -ForegroundColor Green
Write-Host "Interactive Swagger API Docs available at http://127.0.0.1:8000/docs" -ForegroundColor Yellow
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
