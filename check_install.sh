#!/bin/bash

# For Python
if command -v python3 &> /dev/null && python3 --version | grep -qE '3\.(1[1-9]|[2-9][0-9])'; then
    echo "Python 3.11.9+ found."
else
    echo "Installing Python..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python@3.12
    else
        sudo apt update && sudo apt install -y python3.12
    fi
fi

# For MySQL (install 8.0 if available; exact 8.0.42 may need source build)
if command -v mysql &> /dev/null && mysql --version | grep -q "8.0.42"; then
    echo "MySQL 8.0.42 found."
else
    echo "Installing MySQL..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install mysql@8.0
    else
        sudo apt update && sudo apt install -y mysql-server-8.0
    fi
    # Secure install: sudo mysql_secure_installation
fi