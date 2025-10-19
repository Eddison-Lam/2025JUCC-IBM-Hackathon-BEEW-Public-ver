@echo off
python --version 2>NUL | findstr /R "3\.[1-9][1-9]" >NUL
if %errorlevel% equ 0 (
    echo Python 3.11.9+ found.
) else (
    echo Installing Python...
    winget install -e --id Python.Python.3.12 --silent
)

mysql --version 2>NUL | findstr "8.0.42" >NUL
if %errorlevel% equ 0 (
    echo MySQL 8.0.42 found.
) else (
    echo Download MySQL installer from https://dev.mysql.com/downloads/ and run manually; auto-silent install requires MSI args like msiexec /i mysql-installer.msi /quiet.
)
pause