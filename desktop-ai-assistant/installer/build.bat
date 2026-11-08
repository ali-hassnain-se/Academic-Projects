@echo off
REM Builds the app folder with PyInstaller.
REM Run from anywhere, with the project's venv ACTIVE (CMD or PowerShell):
REM     installer\build.bat           normal build (no console window)
REM     installer\build.bat debug     build WITH a console window, to read errors
setlocal
set "ROOT=%~dp0.."
cd /d "%ROOT%"

set "MODE=--windowed"
if /i "%~1"=="debug" set "MODE=--console"

echo === Building DesktopAIAssistant (%MODE%) ===
python -m PyInstaller --noconfirm --clean %MODE% ^
  --name DesktopAIAssistant ^
  --icon "%ROOT%\assets\icon.ico" ^
  --add-data "%ROOT%\assets;assets" ^
  --hidden-import keyring.backends.Windows ^
  --hidden-import pynput.keyboard._win32 ^
  --hidden-import pynput.mouse._win32 ^
  --distpath "%ROOT%\dist" ^
  --workpath "%ROOT%\build" ^
  --specpath "%ROOT%\build" ^
  "%ROOT%\main.py"

if errorlevel 1 (
  echo.
  echo BUILD FAILED. Read the messages above.
  exit /b 1
)

echo.
echo Done. Run it with:  dist\DesktopAIAssistant\DesktopAIAssistant.exe
echo Next: open installer\setup.iss in Inno Setup and press Ctrl+F9.
