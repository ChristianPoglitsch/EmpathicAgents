@echo off
setlocal

set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "LOCAL_PACKAGE_DIR=."

:CreateVirtualenv
echo Creating virtual environment...
python -m venv "%VENV_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"

:InstallPackages
if exist "%REQUIREMENTS_FILE%" (
    echo Installing Python packages from %REQUIREMENTS_FILE%...
    pip install -r "%REQUIREMENTS_FILE%"
) else (
    echo %REQUIREMENTS_FILE% not found. There should be one, check once again, anyway, continuing...
)

if exist "%LOCAL_PACKAGE_DIR%" (
    echo Installing local package in editable mode...
    pip install --editable "%LOCAL_PACKAGE_DIR%"
) else (
    echo Local package directory %LOCAL_PACKAGE_DIR% not found. There should be one, check once again, anyway, continuing...
)

:InstallPytorch
echo Detected Windows OS. Installing PyTorch with CUDA support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo Installation complete, yaayy

endlocal
