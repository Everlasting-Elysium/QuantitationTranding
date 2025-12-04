"""
LoggerSystem 使用示例
演示如何使用日志系统进行日志记录
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from infrastructure.logger_system import LoggerSystem, get_logger, setup_logging


def demo_basic_usage():
    """演示基本使用方法"""
    print("=== 演示1: 基本使用 ===\n")
    
    # 方法1: 使用便捷函数
    setup_logging(
        log_dir="./logs",
        log_level="INFO",
        max_bytes=10485760,  # 10MB
        backup_count=5
    )
    
    # 获取日志记录器
    logger = get_logger("demo_module")
    
    # 记录不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    
    print("日志已写入 ./logs/qlib_trading.log\n")


def demo_different_modules():
    """演示多个模块使用日志"""
    print("=== 演示2: 多模块日志 ===\n")
    
    # 不同模块获取各自的日志记录器
    data_logger = get_logger("data_manager")
    model_logger = get_logger("model_trainer")
    backtest_logger = get_logger("backtest_engine")
    
    # 各模块记录日志
    data_logger.info("开始加载数据...")
    data_logger.info("数据加载完成，共1000条记录")
    
    model_logger.info("开始训练模型...")
    model_logger.info("训练完成，准确率: 85.5%")
    
    backtest_logger.info("开始回测...")
    backtest_logger.info("回测完成，收益率: 15.2%")
    
    print("多个模块的日志已记录\n")


def demo_error_logging():
    """演示错误日志记录"""
    print("=== 演示3: 错误日志 ===\n")
    
    logger = get_logger("error_demo")
    
    try:
        # 模拟一个错误
        result = 10 / 0
    except ZeroDivisionError as e:
        # 使用exception方法记录异常，会自动包含堆栈信息
        logger.exception("计算过程中发生错误")
        logger.error(f"错误详情: {e}")
    
    print("错误日志已记录，包含完整堆栈信息\n")


def demo_log_level_control():
    """演示日志级别控制"""
    print("=== 演示4: 日志级别控制 ===\n")
    
    logger_system = LoggerSystem()
    logger = get_logger("level_demo")
    
    # 初始级别为INFO
    print("当前日志级别: INFO")
    logger.debug("这条DEBUG信息不会被记录")
    logger.info("这条INFO信息会被记录")
    
    # 动态调整为DEBUG级别
    logger_system.set_level("DEBUG")
    print("\n日志级别已调整为: DEBUG")
    logger.debug("现在DEBUG信息也会被记录了")
    logger.info("INFO信息继续被记录")
    
    # 调整为WARNING级别
    logger_system.set_level("WARNING")
    print("\n日志级别已调整为: WARNING")
    logger.info("这条INFO信息不会被记录")
    logger.warning("只有WARNING及以上级别会被记录")
    
    print()


def demo_log_file_management():
    """演示日志文件管理"""
    print("=== 演示5: 日志文件管理 ===\n")
    
    logger_system = LoggerSystem()
    
    # 获取所有日志文件
    log_files = logger_system.get_log_files()
    print(f"当前日志文件数量: {len(log_files)}")
    for log_file in log_files:
        size = log_file.stat().st_size
        print(f"  - {log_file.name}: {size} bytes")
    
    print()


def demo_structured_logging():
    """演示结构化日志记录"""
    print("=== 演示6: 结构化日志 ===\n")
    
    logger = get_logger("structured_demo")
    
    # 记录训练过程
    logger.info("=" * 50)
    logger.info("开始模型训练")
    logger.info("-" * 50)
    logger.info("模型类型: LightGBM")
    logger.info("数据集: CSI300")
    logger.info("训练周期: 2020-01-01 至 2022-12-31")
    logger.info("-" * 50)
    
    # 模拟训练过程
    for epoch in range(1, 4):
        logger.info(f"Epoch {epoch}/3")
        logger.info(f"  训练损失: {0.5 / epoch:.4f}")
        logger.info(f"  验证损失: {0.6 / epoch:.4f}")
    
    logger.info("-" * 50)
    logger.info("训练完成")
    logger.info("=" * 50)
    
    print("结构化日志已记录\n")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("LoggerSystem 使用示例")
    print("=" * 60 + "\n")
    
    # 运行各个演示
    demo_basic_usage()
    demo_different_modules()
    demo_error_logging()
    demo_log_level_control()
    demo_log_file_management()
    demo_structured_logging()
    
    print("=" * 60)
    print("所有演示完成！")
    print("请查看 ./logs/qlib_trading.log 文件查看完整日志")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
