@echo off
REM 快速启动脚本 (Windows) / Quick Start Script (Windows)
REM 
REM This script provides a quick way to initialize and start the system on Windows.
REM 本脚本提供在Windows上快速初始化和启动系统的方式。

setlocal enabledelayedexpansion

echo.
echo ======================================================================
echo   🚀 量化交易系统 - 快速启动 / Quick Start
echo ======================================================================
echo.

REM 检查Python / Check Python
echo [INFO] 检查Python环境 / Checking Python environment...

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python3
    ) else (
        echo [ERROR] 未找到Python / Python not found
        echo 请先安装Python 3.8+ / Please install Python 3.8+ first
        pause
        exit /b 1
    )
)

for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python版本 / Python version: %PYTHON_VERSION%
echo.

REM 运行初始化脚本 / Run initialization script
echo [INFO] 运行初始化脚本 / Running initialization script...
echo.
%PYTHON_CMD% init_system.py

REM 检查初始化是否成功 / Check if initialization succeeded
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] 系统初始化完成！ / System initialization completed!
    echo.
    
    REM 询问是否启动主程序 / Ask if start main program
    set /p START_MAIN="是否现在启动主程序？(y/n) / Start main program now? (y/n): "
    
    if /i "!START_MAIN!"=="y" (
        echo [INFO] 启动主程序 / Starting main program...
        echo.
        %PYTHON_CMD% main.py
    ) else (
        echo [INFO] 您可以稍后运行以下命令启动系统 / You can start the system later with:
        echo   %PYTHON_CMD% main.py
    )
) else (
    echo.
    echo [ERROR] 初始化未完全成功 / Initialization not fully successful
    echo [INFO] 请查看上述错误信息 / Please check error messages above
    pause
    exit /b 1
)

pause
