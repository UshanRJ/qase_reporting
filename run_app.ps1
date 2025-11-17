# Qase Reporter - Web UI Launcher (PowerShell)
# This script activates the virtual environment and starts the Streamlit app

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Qase Test Run Reporter - Web UI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run the following commands first:" -ForegroundColor Yellow
    Write-Host "  1. python -m venv venv" -ForegroundColor Yellow
    Write-Host "  2. .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  3. pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please create a .env file with:" -ForegroundColor Yellow
    Write-Host "  QASE_API_TOKEN=your_token_here" -ForegroundColor White
    Write-Host "  QASE_PROJECT_CODE=your_project_code" -ForegroundColor White
    Write-Host ""
    Write-Host "The app will start but may not work without configuration." -ForegroundColor Yellow
    Write-Host ""
    Start-Sleep -Seconds 3
}

# Start Streamlit app
Write-Host "[INFO] Starting Streamlit application..." -ForegroundColor Green
Write-Host ""
streamlit run app.py

# Note: PowerShell will automatically deactivate the venv when the script exits
