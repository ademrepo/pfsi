$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot
Set-Location ".."  # 16avril/

if (-not (Test-Path ".\\venv\\Scripts\\Activate.ps1")) {
  python -m venv venv
}

. .\\venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts\\init_db.py

Write-Host ""
Write-Host "Setup OK."
Write-Host "Backend:  python manage.py runserver"
Write-Host "Frontend: cd ..\\frontend; npm install; npm run dev"

