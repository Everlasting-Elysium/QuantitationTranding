"""
QlibWrapper使用示例
演示如何使用QlibWrapper进行qlib初始化和数据访问
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.infrastructure import QlibWrapper, QlibInitializationError, QlibDataError, setup_logging


def main():
    """主函数"""
    # 1. 设置日志系统
    print("=" * 60)
    print("QlibWrapper使用示例")
    print("=" * 60)
    
    setup_logging(log_dir="./logs", log_level="INFO")
    
    # 2. 创建QlibWrapper实例
    qlib_wrapper = QlibWrapper()
    
    # 3. 初始化qlib
    print("\n1. 初始化qlib...")
    try:
        qlib_wrapper.init(
            provider_uri="~/.qlib/qlib_data/cn_data",
            region="cn",
            auto_mount=True
        )
        print("✓ qlib初始化成功")
    except QlibInitializationError as e:
        print(f"✗ qlib初始化失败: {e}")
        return
    
    # 4. 检查初始化状态
    print(f"\n2. 检查初始化状态...")
    print(f"   是否已初始化: {qlib_wrapper.is_initialized()}")
    print(f"   数据路径: {qlib_wrapper.get_provider_uri()}")
    print(f"   市场区域: {qlib_wrapper.get_region()}")
    
    # 5. 验证数据可用性
    print(f"\n3. 验证数据可用性...")
    try:
        is_valid, message, time_range = qlib_wrapper.validate_data(instruments="csi300")
        if is_valid:
            print(f"✓ {message}")
            if time_range:
                print(f"   数据时间范围: {time_range[0]} 至 {time_range[1]}")
        else:
            print(f"✗ {message}")
    except QlibDataError as e:
        print(f"✗ 数据验证失败: {e}")
    
    # 6. 获取数据信息
    print(f"\n4. 获取数据信息...")
    try:
        data_info = qlib_wrapper.get_data_info()
        print(f"   数据路径: {data_info['provider_uri']}")
        print(f"   市场区域: {data_info['region']}")
        print(f"   数据开始: {data_info['data_start']}")
        print(f"   数据结束: {data_info['data_end']}")
        print(f"   交易日数: {data_info['trading_days']}")
    except QlibDataError as e:
        print(f"✗ 获取数据信息失败: {e}")
    
    # 7. 获取股票列表
    print(f"\n5. 获取CSI300股票列表...")
    try:
        instruments = qlib_wrapper.get_instruments(market="csi300")
        print(f"✓ 获取到 {len(instruments)} 只股票")
        print(f"   前5只股票: {instruments[:5]}")
    except QlibDataError as e:
        print(f"✗ 获取股票列表失败: {e}")
    
    # 8. 获取交易日历
    print(f"\n6. 获取2023年交易日历...")
    try:
        calendar = qlib_wrapper.get_calendar(
            start_time="2023-01-01",
            end_time="2023-12-31"
        )
        print(f"✓ 获取到 {len(calendar)} 个交易日")
        print(f"   第一个交易日: {calendar[0]}")
        print(f"   最后一个交易日: {calendar[-1]}")
    except QlibDataError as e:
        print(f"✗ 获取交易日历失败: {e}")
    
    # 9. 获取市场数据
    print(f"\n7. 获取2023年1月CSI300收盘价数据...")
    try:
        data = qlib_wrapper.get_data(
            instruments="csi300",
            fields=["$close", "$volume"],
            start_time="2023-01-01",
            end_time="2023-01-31"
        )
        print(f"✓ 获取数据成功")
        print(f"   数据形状: {data.shape}")
        print(f"   数据列: {data.columns.tolist()}")
        print(f"\n   数据预览:")
        print(data.head())
    except QlibDataError as e:
        print(f"✗ 获取数据失败: {e}")
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
