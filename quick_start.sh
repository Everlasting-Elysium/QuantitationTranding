#!/bin/bash
# 快速启动脚本 / Quick Start Script
# 
# This script provides a quick way to initialize and start the system.
# 本脚本提供快速初始化和启动系统的方式。

set -e  # 遇到错误立即退出 / Exit on error

# 颜色定义 / Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息 / Print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 打印标题 / Print header
echo ""
echo "======================================================================"
echo "  🚀 量化交易系统 - 快速启动 / Quick Start"
echo "======================================================================"
echo ""

# 检查Python / Check Python
print_info "检查Python环境 / Checking Python environment..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    print_error "未找到Python / Python not found"
    echo "请先安装Python 3.8+ / Please install Python 3.8+ first"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_success "Python版本 / Python version: $PYTHON_VERSION"

# 运行初始化脚本 / Run initialization script
print_info "运行初始化脚本 / Running initialization script..."
echo ""
$PYTHON_CMD init_system.py

# 检查初始化是否成功 / Check if initialization succeeded
if [ $? -eq 0 ]; then
    echo ""
    print_success "系统初始化完成！ / System initialization completed!"
    echo ""
    
    # 询问是否启动主程序 / Ask if start main program
    read -p "是否现在启动主程序？(y/n) / Start main program now? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "启动主程序 / Starting main program..."
        echo ""
        $PYTHON_CMD main.py
    else
        print_info "您可以稍后运行以下命令启动系统 / You can start the system later with:"
        echo "  $PYTHON_CMD main.py"
    fi
else
    echo ""
    print_error "初始化未完全成功 / Initialization not fully successful"
    print_info "请查看上述错误信息 / Please check error messages above"
    exit 1
fi
