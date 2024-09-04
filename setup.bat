:: This bat file was translated by chatgpt from the original setup.sh bash script
:: if youre using windows, may the lord have mercy. 
@echo off

set VENV_DIR=venv
set REQUIREMENTS_FILE=requirements.txt
set REQUIREMENTS_DEV_FILE=requirements-dev.txt
set LOCAL_PACKAGE_DIR=.

:CREATE_VIRTUALENV
echo Creating virtual environment...
python -m venv %VENV_DIR%
if "%OS%" == "Windows_NT" (
    call "%VENV_DIR%\Scripts\activate"
)

:INSTALL_PACKAGES
if exist %REQUIREMENTS_FILE% (
    echo Installing Python packages from %REQUIREMENTS_FILE%...
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo %REQUIREMENTS_FILE% not found. There should be one, check once again, anyway, continuing...
)

if exist %LOCAL_PACKAGE_DIR% (
    echo Installing local package in editable mode...
    pip install --editable %LOCAL_PACKAGE_DIR%
) else (
    echo Local package directory %LOCAL_PACKAGE_DIR% not found. There should be one, check once again, anyway, continuing...
)

:INSTALL_DEV_PACKAGES
if exist %REQUIREMENTS_DEV_FILE% (
    echo Installing development packages from %REQUIREMENTS_DEV_FILE%...
    pip install -r %REQUIREMENTS_DEV_FILE%
) else (
    echo %REQUIREMENTS_DEV_FILE% not found. There should be one, check once again, anyway, bat script goes BRRRRR...
)

:INSTALL_PYTORCH
if "%OS%" == "Windows_NT" (
    echo Detected Windows OS. Installing PyTorch with CUDA support...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
) else (
    echo Not on Windows. Lucky you :)
)

echo Installation complete, yaayy
