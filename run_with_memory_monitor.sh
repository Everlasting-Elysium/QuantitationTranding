#!/bin/bash
# 带内存监控的启动脚本 / Startup script with memory monitoring
# 
# 使用方法 / Usage:
#   ./run_with_memory_monitor.sh
#
# 或者 / Or:
#   bash run_with_memory_monitor.sh

echo "=================================="
echo "量化交易系统 (带内存监控)"
echo "Quantitative Trading System (with Memory Monitoring)"
echo "=================================="
echo ""

# 检查conda环境 / Check conda environment
if ! conda info --envs | grep -q "QuantitationTranding"; then
    echo "❌ 错误: QuantitationTranding conda环境不存在"
    echo "❌ Error: QuantitationTranding conda environment not found"
    echo ""
    echo "请先创建环境 / Please create the environment first:"
    echo "  conda create -n QuantitationTranding python=3.8"
    echo "  conda activate QuantitationTranding"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# 显示内存信息 / Show memory info
echo "系统内存信息 / System Memory Info:"
free -h | grep -E "Mem|Swap" || echo "无法获取内存信息 / Cannot get memory info"
echo ""

# 激活conda环境并运行 / Activate conda environment and run
echo "启动程序... / Starting program..."
echo ""

conda run -n QuantitationTranding python main.py

# 显示退出状态 / Show exit status
EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 程序正常退出 / Program exited normally"
else
    echo "❌ 程序异常退出，退出码: $EXIT_CODE / Program exited with error, code: $EXIT_CODE"
fi

exit $EXIT_CODE
