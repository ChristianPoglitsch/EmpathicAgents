#!/bin/bash

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
REQUIREMENTS_DEV_FILE="requirements-dev.txt"
LOCAL_PACKAGE_DIR="."

create_virtualenv() {
    echo "Creating virtual environment..."
    python -m venv "$VENV_DIR"
    if [[ "$OS" == "Windows_NT" ]]; then
        source "$VENV_DIR/Scripts/activate"
    else 
        source "$VENV_DIR/bin/activate"
    fi
}

install_packages() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing Python packages from $REQUIREMENTS_FILE..."
        pip install -r "$REQUIREMENTS_FILE"
    else
        echo "$REQUIREMENTS_FILE not found. There should be one, check once again, anyway, continuing..."
    fi

    if [ -d "$LOCAL_PACKAGE_DIR" ]; then
        echo "Installing local package in editable mode..."
        pip install --editable "$LOCAL_PACKAGE_DIR"
    else
        echo "Local package directory $LOCAL_PACKAGE_DIR not found. There should be one, check once again, anyway, continuing..."
    fi
}

install_dev_packages() {
    if [ -f "$REQUIREMENTS_DEV_FILE" ]; then
        echo "Installing development packages from $REQUIREMENTS_DEV_FILE..."
        pip install -r "$REQUIREMENTS_DEV_FILE"
    else
        echo "$REQUIREMENTS_DEV_FILE not found. There should be one, check once again, anyway, bash script goes BRRRRR..."
    fi
}

install_pytorch() {
    if [[ "$OS" == "Windows_NT" ]]; then
        echo "Detected Windows OS. Installing PyTorch with CUDA support..."
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    else
        echo "Not on Windows. Lucky you :)"
    fi
}



create_virtualenv
install_packages
install_dev_packages
install_pytorch

echo "Installation complete, yaayy"