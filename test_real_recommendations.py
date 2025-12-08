#!/usr/bin/env python3
"""
测试真实推荐功能 / Test Real Recommendations
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.application.performance_analyzer import PerformanceAnalyzer
from src.infrastructure.qlib_wrapper import QlibWrapper

def test_real_recommendations():
    """测试真实的股票推荐"""
    print("=" * 80)
    print("测试真实股票推荐功能 / Testing Real Stock Recommendations")
    print("=" * 80)
    
    try:
        # 初始化qlib
        print("\n1. 初始化qlib...")
        qlib_wrapper = QlibWrapper()
        data_path = Path.home() / ".qlib" / "qlib_data" / "cn_data"
        
        if not data_path.exists():
            print(f"❌ 数据路径不存在: {data_path}")
            return False
        
        qlib_wrapper.init(provider_uri=str(data_path), region="cn")
        print("✓ qlib初始化成功")
        
        # 获取数据信息
        print("\n2. 检查数据信息...")
        data_info = qlib_wrapper.get_data_info()
        print(f"✓ 数据范围: {data_info['data_start']} 到 {data_info['data_end']}")
        print(f"✓ 交易日数: {data_info['trading_days']}")
        
        # 创建性能分析器
        print("\n3. 创建性能分析器...")
        analyzer = PerformanceAnalyzer(qlib_wrapper)
        print("✓ 性能分析器创建成功")
        
        # 分析历史表现
        # 注意：数据只到2020年9月，所以我们分析2017-2020的数据
        print("\n4. 分析沪深300历史表现（2017-2020）...")
        print("   (这可能需要几分钟，请耐心等待...)")
        
        # 使用数据范围内的时间
        from datetime import datetime, timedelta
        end_date = datetime(2020, 9, 25)  # 数据结束日期
        start_date = end_date - timedelta(days=3*365)  # 往前推3年
        
        report = analyzer.analyze_historical_performance_custom(
            market="CN",
            asset_type="stock",
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            instruments="csi300"
        )
        
        print(f"✓ 成功分析 {report.total_assets_analyzed} 只股票")
        
        # 显示推荐
        print("\n5. 推荐结果:")
        print("=" * 80)
        print("基于历史表现的前10名推荐:")
        print("=" * 80)
        
        for i, asset in enumerate(report.top_performers[:10], 1):
            print(f"\n{i}. {asset.symbol}")
            if asset.name:
                print(f"   名称: {asset.name}")
            print(f"   年化收益: {asset.annual_return * 100:.2f}%")
            print(f"   夏普比率: {asset.sharpe_ratio:.2f}")
            print(f"   最大回撤: {asset.max_drawdown * 100:.2f}%")
        
        print("\n" + "=" * 80)
        print("✅ 测试成功！推荐功能正常工作")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_recommendations()
    sys.exit(0 if success else 1)
