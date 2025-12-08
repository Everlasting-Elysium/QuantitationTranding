"""
Main CLI Interface / 主命令行界面

This module provides the main command-line interface for the quantitative trading system.
本模块提供量化交易系统的主命令行界面。
"""

import sys
from typing import Optional, Dict, Callable, Any
from datetime import datetime
from .interactive_prompt import InteractivePrompt


class MainCLI:
    """
    Main command-line interface controller.
    主命令行界面控制器。
    
    Responsibilities / 职责:
    - Display main menu / 显示主菜单
    - Route user selections to corresponding functions / 将用户选择路由到相应功能
    - Handle global commands (help, exit, etc.) / 处理全局命令（帮助、退出等）
    
    Validates: Requirements 12.1, 12.4, 13.4
    """
    
    def __init__(self):
        """Initialize the main CLI / 初始化主CLI"""
        self.prompt = InteractivePrompt()
        self.running = True
        
        # 延迟初始化管理器，避免启动时的开销
        # Lazy initialization of managers to avoid startup overhead
        self._training_manager = None
        self._data_manager = None
        self._model_factory = None
        self._mlflow_tracker = None
        self._config_manager = None
        
        # 内存监控器引用（由main函数启动）
        # Memory monitor reference (started by main function)
        self._memory_monitor = None
        
        # Menu options and their handlers
        # 菜单选项及其处理器
        self.menu_options: Dict[str, Dict[str, any]] = {
            "0": {
                "name": "🎯 引导式工作流程 / Guided Workflow",
                "handler": self._handle_guided_workflow,
                "description": "完整的投资流程引导（推荐新手使用）/ Complete investment process guidance (Recommended for beginners)",
                "highlight": True
            },
            "1": {
                "name": "模型训练 / Model Training",
                "handler": self._handle_training,
                "description": "训练新的预测模型 / Train new prediction models"
            },
            "2": {
                "name": "历史回测 / Historical Backtest",
                "handler": self._handle_backtest,
                "description": "对模型进行历史回测 / Backtest models on historical data"
            },
            "3": {
                "name": "信号生成 / Signal Generation",
                "handler": self._handle_signal_generation,
                "description": "生成交易信号 / Generate trading signals"
            },
            "4": {
                "name": "数据管理 / Data Management",
                "handler": self._handle_data_management,
                "description": "下载和管理市场数据 / Download and manage market data"
            },
            "5": {
                "name": "模型管理 / Model Management",
                "handler": self._handle_model_management,
                "description": "查看和管理训练好的模型 / View and manage trained models"
            },
            "6": {
                "name": "报告查看 / View Reports",
                "handler": self._handle_reports,
                "description": "查看训练和回测报告 / View training and backtest reports"
            },
            "7": {
                "name": "🔧 系统管理 / System Management",
                "handler": self._handle_system_management,
                "description": "内存监控、缓存清理等系统管理功能 / Memory monitoring, cache cleanup, etc."
            },
            "h": {
                "name": "帮助 / Help",
                "handler": self._show_help,
                "description": "显示帮助信息 / Show help information"
            },
            "q": {
                "name": "退出 / Quit",
                "handler": self._quit,
                "description": "退出系统 / Exit the system"
            }
        }
    
    def run(self) -> None:
        """
        Run the main CLI loop.
        运行主CLI循环。
        
        Validates: Requirements 12.1, 12.4
        """
        self._show_welcome()
        
        while self.running:
            try:
                self.show_menu()
                choice = self._get_user_choice()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\n⚠️  检测到中断信号 / Interrupt signal detected")
                if self.prompt.confirm("确定要退出吗？ / Are you sure you want to exit?", default=False):
                    self.running = False
                    print("\n👋 再见！ / Goodbye!\n")
            except Exception as e:
                print(f"\n❌ 发生错误 / Error occurred: {str(e)}")
                print("请重试或输入 'h' 查看帮助 / Please try again or enter 'h' for help\n")
    
    def show_menu(self) -> None:
        """
        Display the main menu.
        显示主菜单。
        
        Validates: Requirements 12.1, 22.1
        """
        print("\n" + "=" * 70)
        print("📊 量化交易系统 - 主菜单 / Quantitative Trading System - Main Menu")
        print("=" * 70)
        print()
        
        # Display highlighted option (guided workflow)
        # 显示高亮选项（引导式工作流程）
        if "0" in self.menu_options:
            option = self.menu_options["0"]
            print("  " + "⭐" * 35)
            print(f"  {option['name']}")
            print(f"  {option['description']}")
            print("  " + "⭐" * 35)
            print()
        
        # Display numbered options
        # 显示编号选项
        for key in ["1", "2", "3", "4", "5", "6"]:
            option = self.menu_options[key]
            print(f"  {key}. {option['name']}")
            print(f"     {option['description']}")
            print()
        
        # Display special options
        # 显示特殊选项
        print(f"  h. {self.menu_options['h']['name']}")
        print(f"  q. {self.menu_options['q']['name']}")
        print()
        print("=" * 70)
    
    def _get_user_choice(self) -> str:
        """
        Get user's menu choice.
        获取用户的菜单选择。
        
        Returns:
            User's choice / 用户的选择
        """
        choice = input("请选择功能 / Please select an option: ").strip().lower()
        return choice
    
    def handle_choice(self, choice: str) -> None:
        """
        Handle user's menu choice.
        处理用户的菜单选择。
        
        Args:
            choice: User's menu choice / 用户的菜单选择
            
        Validates: Requirements 12.1, 12.4
        """
        if choice in self.menu_options:
            handler = self.menu_options[choice]["handler"]
            handler()
        else:
            print(f"\n❌ 无效的选择: '{choice}' / Invalid choice: '{choice}'")
            print("请输入有效的选项编号或 'h' 查看帮助 / Please enter a valid option or 'h' for help\n")
    
    def _show_welcome(self) -> None:
        """
        Display welcome message.
        显示欢迎消息。
        
        Validates: Requirements 22.1
        """
        print("\n" + "=" * 70)
        print("🎉 欢迎使用量化交易系统！ / Welcome to Quantitative Trading System!")
        print("=" * 70)
        print()
        print("本系统基于 qlib 框架，提供完整的量化交易解决方案。")
        print("This system is based on qlib framework, providing complete quantitative trading solutions.")
        print()
        print("功能特性 / Features:")
        print("  • 智能模型训练 / Intelligent model training")
        print("  • 历史数据回测 / Historical backtesting")
        print("  • 实时信号生成 / Real-time signal generation")
        print("  • 数据管理工具 / Data management tools")
        print("  • 模型版本管理 / Model version management")
        print()
        print("⭐ 新功能 / New Feature:")
        print("  🎯 引导式工作流程 - 完整的投资流程引导（推荐新手使用）")
        print("  🎯 Guided Workflow - Complete investment process guidance (Recommended for beginners)")
        print("     选择选项 0 开始 / Select option 0 to start")
        print()
        print("提示：输入 'h' 可随时查看帮助信息 / Tip: Enter 'h' anytime for help")
        print("=" * 70)
    
    def _show_help(self) -> None:
        """
        Display help information.
        显示帮助信息。
        
        Validates: Requirements 13.4
        """
        print("\n" + "=" * 70)
        print("📖 帮助信息 / Help Information")
        print("=" * 70)
        print()
        
        print("【系统概述 / System Overview】")
        print("本系统是一个基于 qlib 的智能量化交易平台，提供从数据管理、")
        print("模型训练、历史回测到信号生成的完整工作流程。")
        print()
        print("This is an intelligent quantitative trading platform based on qlib,")
        print("providing a complete workflow from data management, model training,")
        print("historical backtesting to signal generation.")
        print()
        
        print("【主要功能 / Main Features】")
        print()
        
        # 特别突出引导式工作流程 / Highlight guided workflow
        if "0" in self.menu_options:
            option = self.menu_options["0"]
            print("⭐ 推荐功能 / Recommended Feature:")
            print(f"0. {option['name']}")
            print(f"   {option['description']}")
            print("   适合：新手用户、完整流程需求")
            print("   Suitable for: Beginners, complete workflow needs")
            print()
        
        print("其他功能 / Other Features:")
        for key in ["1", "2", "3", "4", "5", "6"]:
            option = self.menu_options[key]
            print(f"{key}. {option['name']}")
            print(f"   {option['description']}")
            print()
        
        print("【使用流程 / Usage Workflow】")
        print("1. 数据管理：首先下载和准备市场数据")
        print("   Data Management: First download and prepare market data")
        print()
        print("2. 模型训练：使用历史数据训练预测模型")
        print("   Model Training: Train prediction models using historical data")
        print()
        print("3. 历史回测：在历史数据上测试模型表现")
        print("   Historical Backtest: Test model performance on historical data")
        print()
        print("4. 信号生成：使用训练好的模型生成交易信号")
        print("   Signal Generation: Generate trading signals using trained models")
        print()
        
        print("【快捷键 / Shortcuts】")
        print("  h - 显示此帮助信息 / Show this help information")
        print("  q - 退出系统 / Quit the system")
        print("  Ctrl+C - 中断当前操作 / Interrupt current operation")
        print()
        
        print("【获取更多帮助 / Get More Help】")
        print("  • 查看文档：docs/ 目录下的详细文档")
        print("    View documentation: Detailed docs in docs/ directory")
        print("  • 查看示例：examples/ 目录下的示例代码")
        print("    View examples: Example code in examples/ directory")
        print("  • 在线文档：https://qlib.readthedocs.io/")
        print("    Online docs: https://qlib.readthedocs.io/")
        print()
        print("=" * 70)
        
        input("\n按回车键继续 / Press Enter to continue...")
    
    def _quit(self) -> None:
        """
        Quit the application.
        退出应用程序。
        """
        if self.prompt.confirm("确定要退出吗？ / Are you sure you want to exit?", default=False):
            self.running = False
            print("\n" + "=" * 70)
            print("👋 感谢使用量化交易系统！ / Thank you for using the system!")
            print("=" * 70)
            print()
    
    # Feature handlers - to be implemented in future tasks
    # 功能处理器 - 将在未来的任务中实现
    
    def _handle_training(self) -> None:
        """
        Handle model training menu.
        处理模型训练菜单。
        
        Validates: Requirements 2.1, 2.2, 14.1, 14.5
        """
        print("\n" + "=" * 70)
        print("🎓 模型训练 / Model Training")
        print("=" * 70)
        print()
        
        # 显示训练子菜单 / Display training submenu
        training_choice = self.prompt.ask_choice(
            "请选择训练方式 / Please select training method:",
            [
                "使用模型模板训练 / Train with model template",
                "自定义参数训练 / Train with custom parameters",
                "返回主菜单 / Return to main menu"
            ]
        )
        
        if training_choice == "返回主菜单 / Return to main menu":
            return
        elif training_choice == "使用模型模板训练 / Train with model template":
            self._train_from_template()
        else:
            self._train_with_custom_params()
    
    def _handle_backtest(self) -> None:
        """
        Handle backtest menu.
        处理回测菜单。
        
        Validates: Requirements 4.1, 4.2
        """
        print("\n" + "=" * 70)
        print("📈 历史回测 / Historical Backtest")
        print("=" * 70)
        print()
        
        # 显示回测子菜单 / Display backtest submenu
        backtest_choice = self.prompt.ask_choice(
            "请选择回测操作 / Please select backtest operation:",
            [
                "运行新回测 / Run new backtest",
                "查看回测结果 / View backtest results",
                "返回主菜单 / Return to main menu"
            ]
        )
        
        if backtest_choice == "返回主菜单 / Return to main menu":
            return
        elif backtest_choice == "运行新回测 / Run new backtest":
            self._run_backtest()
        else:
            self._view_backtest_results()
    
    def _handle_signal_generation(self) -> None:
        """
        Handle signal generation menu.
        处理信号生成菜单。
        
        Validates: Requirements 6.1, 6.4, 15.2
        """
        print("\n" + "=" * 70)
        print("📡 信号生成 / Signal Generation")
        print("=" * 70)
        print()
        
        # 显示信号生成子菜单 / Display signal generation submenu
        signal_choice = self.prompt.ask_choice(
            "请选择操作 / Please select an operation:",
            [
                "生成新信号 / Generate new signals",
                "查看信号历史 / View signal history",
                "返回主菜单 / Return to main menu"
            ]
        )
        
        if signal_choice == "返回主菜单 / Return to main menu":
            return
        elif signal_choice == "生成新信号 / Generate new signals":
            self._generate_new_signals()
        else:
            self._view_signal_history()
    
    def _handle_data_management(self) -> None:
        """
        Handle data management menu.
        处理数据管理菜单。
        
        Validates: Requirements 9.1, 9.2
        """
        print("\n" + "=" * 70)
        print("💾 数据管理 / Data Management")
        print("=" * 70)
        print()
        
        # 显示数据管理子菜单 / Display data management submenu
        data_choice = self.prompt.ask_choice(
            "请选择数据管理操作 / Please select data management operation:",
            [
                "下载市场数据 / Download market data",
                "验证数据完整性 / Validate data integrity",
                "查看数据信息 / View data information",
                "检查数据覆盖 / Check data coverage",
                "返回主菜单 / Return to main menu"
            ]
        )
        
        if data_choice == "返回主菜单 / Return to main menu":
            return
        elif data_choice == "下载市场数据 / Download market data":
            self._download_market_data()
        elif data_choice == "验证数据完整性 / Validate data integrity":
            self._validate_data_integrity()
        elif data_choice == "查看数据信息 / View data information":
            self._view_data_info()
        else:  # 检查数据覆盖 / Check data coverage
            self._check_data_coverage()
    
    def _handle_model_management(self) -> None:
        """
        Handle model management menu.
        处理模型管理菜单。
        
        Validates: Requirements 7.3, 7.4, 7.5
        """
        while True:
            print("\n" + "=" * 70)
            print("🗂️  模型管理 / Model Management")
            print("=" * 70)
            print()
            
            # 显示模型管理子菜单 / Display model management submenu
            management_choice = self.prompt.ask_choice(
                "请选择模型管理操作 / Please select model management operation:",
                [
                    "查看模型列表 / View model list",
                    "查看模型详情 / View model details",
                    "设置生产模型 / Set production model",
                    "删除模型 / Delete model",
                    "返回主菜单 / Return to main menu"
                ]
            )
            
            if management_choice == "返回主菜单 / Return to main menu":
                break
            elif management_choice == "查看模型列表 / View model list":
                self._view_model_list()
            elif management_choice == "查看模型详情 / View model details":
                self._view_model_details()
            elif management_choice == "设置生产模型 / Set production model":
                self._set_production_model()
            else:  # 删除模型 / Delete model
                self._delete_model()
    
    def _handle_reports(self) -> None:
        """
        Handle reports viewing menu.
        处理报告查看菜单。
        
        Note: This will be implemented in future tasks.
        注意：这将在未来的任务中实现。
        """
        print("\n" + "=" * 70)
        print("📊 报告查看 / View Reports")
        print("=" * 70)
        print()
        print("⚠️  此功能将在后续任务中实现。")
        print("⚠️  This feature will be implemented in a future task.")
        print()
        print("功能预览 / Feature Preview:")
        print("  • 查看训练报告 / View training reports")
        print("  • 查看回测报告 / View backtest reports")
        print("  • 查看性能对比 / View performance comparison")
        print("  • 导出报告 / Export reports")
        print()
        input("按回车键返回主菜单 / Press Enter to return to main menu...")
    
    # Signal generation-related helper methods / 信号生成相关的辅助方法
    
    def _get_signal_generator(self):
        """
        Get or initialize the signal generator.
        获取或初始化信号生成器。
        
        Returns:
            SignalGenerator instance / 信号生成器实例
        """
        if not hasattr(self, '_signal_generator') or self._signal_generator is None:
            try:
                from ..application.signal_generator import SignalGenerator
                from ..infrastructure.qlib_wrapper import QlibWrapper
                
                # 初始化qlib封装器 / Initialize qlib wrapper
                if not hasattr(self, '_qlib_wrapper') or self._qlib_wrapper is None:
                    self._qlib_wrapper = QlibWrapper()
                    # 确保qlib已初始化 / Ensure qlib is initialized
                    if not self._qlib_wrapper.is_initialized():
                        print("\n⚠️  Qlib未初始化，正在初始化... / Qlib not initialized, initializing...")
                        self._qlib_wrapper.init(
                            provider_uri="~/.qlib/qlib_data/cn_data",
                            region="cn"
                        )
                
                # 获取模型注册表 / Get model registry
                model_registry = self._get_model_registry()
                
                # 创建信号生成器 / Create signal generator
                self._signal_generator = SignalGenerator(
                    model_registry=model_registry,
                    qlib_wrapper=self._qlib_wrapper
                )
                
            except Exception as e:
                print(f"\n❌ 初始化信号生成器失败 / Failed to initialize signal generator: {str(e)}")
                raise
        
        return self._signal_generator
    
    def _generate_new_signals(self) -> None:
        """
        Generate new trading signals.
        生成新的交易信号。
        
        Validates: Requirements 6.1, 6.4
        """
        try:
            print("\n" + "=" * 70)
            print("🚀 生成新信号 / Generate New Signals")
            print("=" * 70)
            print()
            
            # 获取信号生成器和模型注册表 / Get signal generator and model registry
            signal_generator = self._get_signal_generator()
            model_registry = self._get_model_registry()
            
            # 1. 选择模型 / Select model
            print("正在加载可用模型... / Loading available models...")
            models = model_registry.list_models()
            
            if not models:
                print("❌ 没有可用的模型 / No models available")
                print("请先训练模型 / Please train a model first")
                input("\n按回车键返回 / Press Enter to return...")
                return
            
            # 显示模型列表 / Display model list
            print("\n可用的模型 / Available Models:")
            print("-" * 70)
            model_choices = []
            for i, model in enumerate(models, 1):
                print(f"\n{i}. {model.model_name} (v{model.version})")
                print(f"   模型ID / Model ID: {model.model_id}")
                print(f"   模型类型 / Model Type: {model.model_type}")
                print(f"   训练日期 / Training Date: {model.training_date}")
                print(f"   状态 / Status: {model.status}")
                if model.performance_metrics:
                    print(f"   性能指标 / Performance Metrics:")
                    for metric, value in list(model.performance_metrics.items())[:3]:  # 只显示前3个指标
                        if isinstance(value, float):
                            print(f"     - {metric}: {value:.6f}")
                        else:
                            print(f"     - {metric}: {value}")
                model_choices.append(f"{model.model_name} (v{model.version})")
            
            print("-" * 70)
            
            # 选择模型 / Select model
            model_choice = self.prompt.ask_choice(
                "\n请选择要使用的模型 / Please select a model:",
                model_choices + ["返回 / Return"]
            )
            
            if model_choice == "返回 / Return":
                return
            
            # 获取选中的模型 / Get selected model
            selected_index = model_choices.index(model_choice)
            selected_model = models[selected_index]
            
            # 2. 配置信号生成参数 / Configure signal generation parameters
            print("\n" + "=" * 70)
            print("⚙️  配置信号生成参数 / Configure Signal Generation Parameters")
            print("=" * 70)
            print()
            
            # 信号生成日期 / Signal generation date
            signal_date = self.prompt.ask_date(
                "请输入信号生成日期 / Please enter signal generation date",
                default=datetime.now().strftime("%Y-%m-%d")
            )
            
            # 股票池 / Stock pool
            instruments = self.prompt.ask_choice(
                "\n请选择股票池 / Please select stock pool:",
                [
                    "csi300 (沪深300)",
                    "csi500 (中证500)",
                    "csi800 (中证800)",
                    "自定义 / Custom"
                ]
            )
            
            if instruments == "自定义 / Custom":
                instruments = self.prompt.ask_text(
                    "请输入股票池代码 / Please enter stock pool code:",
                    default="csi300"
                )
            else:
                instruments = instruments.split()[0]  # 提取代码部分 / Extract code part
            
            # 买入候选数量 / Number of buy candidates
            top_n = self.prompt.ask_integer(
                "\n请输入买入候选数量 / Please enter number of buy candidates:",
                min_val=1,
                max_val=100,
                default=10
            )
            
            # 3. 创建模拟投资组合 / Create simulated portfolio
            from ..models.trading_models import Portfolio
            
            # 询问是否使用现有持仓 / Ask if using existing positions
            use_existing_positions = self.prompt.confirm(
                "\n是否有现有持仓？ / Do you have existing positions?",
                default=False
            )
            
            portfolio = Portfolio(
                cash=1000000.0,  # 默认100万现金 / Default 1 million cash
                positions={},
                total_value=1000000.0
            )
            
            if use_existing_positions:
                print("\n⚠️  现有持仓输入功能将在后续版本中完善")
                print("⚠️  Existing positions input will be improved in future versions")
                print("当前将使用空持仓 / Will use empty positions")
            
            # 4. 确认配置 / Confirm configuration
            print("\n" + "=" * 70)
            print("📝 信号生成配置确认 / Signal Generation Configuration Confirmation")
            print("=" * 70)
            print(f"模型 / Model: {selected_model.model_name} (v{selected_model.version})")
            print(f"模型ID / Model ID: {selected_model.model_id}")
            print(f"信号日期 / Signal Date: {signal_date}")
            print(f"股票池 / Stock Pool: {instruments}")
            print(f"买入候选数 / Buy Candidates: {top_n}")
            print(f"初始资金 / Initial Cash: {portfolio.cash:,.2f}")
            print("=" * 70)
            
            if not self.prompt.confirm("\n确认生成信号？ / Confirm to generate signals?", default=True):
                print("❌ 信号生成已取消 / Signal generation cancelled")
                return
            
            # 5. 生成信号 / Generate signals
            print("\n" + "=" * 70)
            print("🚀 开始生成信号 / Starting Signal Generation")
            print("=" * 70)
            print()
            
            print("⏳ 信号生成中，请稍候... / Generating signals, please wait...")
            print()
            
            # 执行信号生成 / Execute signal generation
            signals = signal_generator.generate_signals(
                model_id=selected_model.model_id,
                date=signal_date,
                portfolio=portfolio,
                top_n=top_n,
                instruments=instruments
            )
            
            # 6. 显示信号结果 / Display signal results
            self._display_signals(signals, signal_generator)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  信号生成已中断 / Signal generation interrupted")
        except Exception as e:
            print(f"\n❌ 信号生成失败 / Signal generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _display_signals(self, signals, signal_generator) -> None:
        """
        Display generated signals.
        显示生成的信号。
        
        Args:
            signals: List of Signal objects / 信号对象列表
            signal_generator: SignalGenerator instance / 信号生成器实例
            
        Validates: Requirements 6.4, 15.2
        """
        print("\n" + "=" * 70)
        print("✅ 信号生成完成！ / Signal Generation Completed!")
        print("=" * 70)
        print()
        
        if not signals:
            print("⚠️  未生成任何信号 / No signals generated")
            print("可能原因 / Possible reasons:")
            print("  • 当前日期没有可用数据 / No data available for current date")
            print("  • 所有候选股票都不满足风险控制条件 / All candidates fail risk control")
            print("  • 模型预测结果为空 / Model predictions are empty")
            return
        
        # 按操作类型分组显示 / Display grouped by action type
        buy_signals = [s for s in signals if s.action == "buy"]
        sell_signals = [s for s in signals if s.action == "sell"]
        hold_signals = [s for s in signals if s.action == "hold"]
        
        print(f"总信号数 / Total Signals: {len(signals)}")
        print(f"  买入信号 / Buy Signals: {len(buy_signals)}")
        print(f"  卖出信号 / Sell Signals: {len(sell_signals)}")
        print(f"  持有信号 / Hold Signals: {len(hold_signals)}")
        print()
        
        # 显示买入信号 / Display buy signals
        if buy_signals:
            print("=" * 70)
            print("📈 买入信号 / Buy Signals")
            print("=" * 70)
            for i, signal in enumerate(buy_signals, 1):
                print(f"\n{i}. {signal.stock_code}")
                print(f"   预测分数 / Score: {signal.score:.4f}")
                print(f"   置信度 / Confidence: {signal.confidence:.2%}")
                if signal.target_weight:
                    print(f"   建议权重 / Target Weight: {signal.target_weight:.2f}%")
                if signal.reason:
                    print(f"   原因 / Reason: {signal.reason}")
        
        # 显示卖出信号 / Display sell signals
        if sell_signals:
            print("\n" + "=" * 70)
            print("📉 卖出信号 / Sell Signals")
            print("=" * 70)
            for i, signal in enumerate(sell_signals, 1):
                print(f"\n{i}. {signal.stock_code}")
                print(f"   预测分数 / Score: {signal.score:.4f}")
                print(f"   置信度 / Confidence: {signal.confidence:.2%}")
                if signal.quantity:
                    print(f"   持仓数量 / Quantity: {signal.quantity}")
                if signal.reason:
                    print(f"   原因 / Reason: {signal.reason}")
        
        # 显示持有信号 / Display hold signals
        if hold_signals:
            print("\n" + "=" * 70)
            print("🔄 持有信号 / Hold Signals")
            print("=" * 70)
            for i, signal in enumerate(hold_signals, 1):
                print(f"\n{i}. {signal.stock_code}")
                print(f"   预测分数 / Score: {signal.score:.4f}")
                print(f"   置信度 / Confidence: {signal.confidence:.2%}")
                if signal.quantity:
                    print(f"   持仓数量 / Quantity: {signal.quantity}")
                if signal.reason:
                    print(f"   原因 / Reason: {signal.reason}")
        
        print("\n" + "=" * 70)
        
        # 询问是否查看详细解释 / Ask if view detailed explanations
        if self.prompt.confirm("\n是否查看信号详细解释？ / View detailed signal explanations?", default=False):
            self._show_signal_explanations(signals, signal_generator)
        
        # 询问是否导出信号 / Ask if export signals
        if self.prompt.confirm("\n是否导出信号到文件？ / Export signals to file?", default=False):
            self._export_signals(signals)
    
    def _show_signal_explanations(self, signals, signal_generator) -> None:
        """
        Show detailed explanations for signals.
        显示信号的详细解释。
        
        Args:
            signals: List of Signal objects / 信号对象列表
            signal_generator: SignalGenerator instance / 信号生成器实例
            
        Validates: Requirements 15.2
        """
        print("\n" + "=" * 70)
        print("📖 信号详细解释 / Detailed Signal Explanations")
        print("=" * 70)
        
        # 只显示买入和卖出信号的解释 / Only show explanations for buy and sell signals
        action_signals = [s for s in signals if s.action in ["buy", "sell"]]
        
        if not action_signals:
            print("\n⚠️  没有需要解释的信号 / No signals to explain")
            return
        
        for i, signal in enumerate(action_signals, 1):
            try:
                print(f"\n{'-' * 70}")
                print(f"{i}. {signal.stock_code} - {signal.action.upper()}")
                print(f"{'-' * 70}")
                
                # 获取信号解释 / Get signal explanation
                explanation = signal_generator.explain_signal(signal)
                
                # 显示主要因素 / Display main factors
                print("\n主要影响因素 / Main Factors:")
                for factor_name, contribution in explanation.main_factors:
                    print(f"  • {factor_name}: {contribution:.1%}")
                
                # 显示风险等级 / Display risk level
                risk_emoji = {
                    "low": "🟢",
                    "medium": "🟡",
                    "high": "🔴"
                }
                risk_text = {
                    "low": "低风险 / Low Risk",
                    "medium": "中等风险 / Medium Risk",
                    "high": "高风险 / High Risk"
                }
                print(f"\n风险等级 / Risk Level: {risk_emoji.get(explanation.risk_level, '⚪')} {risk_text.get(explanation.risk_level, explanation.risk_level)}")
                
                # 显示描述 / Display description
                if explanation.description:
                    print(f"\n详细说明 / Description:")
                    print(f"  {explanation.description}")
                
            except Exception as e:
                print(f"\n❌ 无法获取信号解释 / Failed to get explanation: {str(e)}")
        
        print("\n" + "=" * 70)
    
    def _export_signals(self, signals) -> None:
        """
        Export signals to file.
        导出信号到文件。
        
        Args:
            signals: List of Signal objects / 信号对象列表
        """
        try:
            import json
            from pathlib import Path
            from datetime import datetime
            
            # 创建输出目录 / Create output directory
            output_dir = Path("outputs/signals")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成文件名 / Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"signals_{timestamp}.json"
            filepath = output_dir / filename
            
            # 转换信号为字典 / Convert signals to dict
            signals_data = []
            for signal in signals:
                signal_dict = {
                    "stock_code": signal.stock_code,
                    "action": signal.action,
                    "score": float(signal.score),
                    "confidence": float(signal.confidence),
                    "timestamp": signal.timestamp,
                    "reason": signal.reason if hasattr(signal, 'reason') else None,
                    "quantity": float(signal.quantity) if signal.quantity else None,
                    "target_weight": float(signal.target_weight) if signal.target_weight else None
                }
                signals_data.append(signal_dict)
            
            # 写入文件 / Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(signals_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ 信号已导出 / Signals exported")
            print(f"   文件路径 / File path: {filepath}")
            
        except Exception as e:
            print(f"\n❌ 导出失败 / Export failed: {str(e)}")
    
    def _view_signal_history(self) -> None:
        """
        View signal history.
        查看信号历史。
        """
        print("\n" + "=" * 70)
        print("📊 查看信号历史 / View Signal History")
        print("=" * 70)
        print()
        print("⚠️  此功能将在后续版本中完善")
        print("⚠️  This feature will be improved in future versions")
        print()
        print("当前可以在 outputs/signals/ 目录中查看导出的信号文件")
        print("Currently you can view exported signal files in outputs/signals/ directory")
        print()
        input("按回车键返回 / Press Enter to return...")
    
    # Backtest-related helper methods / 回测相关的辅助方法
    
    def _get_backtest_manager(self):
        """
        Get or initialize the backtest manager.
        获取或初始化回测管理器。
        
        Returns:
            BacktestManager instance / 回测管理器实例
        """
        if not hasattr(self, '_backtest_manager') or self._backtest_manager is None:
            try:
                from ..application.backtest_manager import BacktestManager
                from ..infrastructure.qlib_wrapper import QlibWrapper
                
                # 初始化qlib封装器 / Initialize qlib wrapper
                if not hasattr(self, '_qlib_wrapper') or self._qlib_wrapper is None:
                    self._qlib_wrapper = QlibWrapper()
                    # 确保qlib已初始化 / Ensure qlib is initialized
                    if not self._qlib_wrapper.is_initialized():
                        print("\n⚠️  Qlib未初始化，正在初始化... / Qlib not initialized, initializing...")
                        self._qlib_wrapper.init(
                            provider_uri="~/.qlib/qlib_data/cn_data",
                            region="cn"
                        )
                
                # 创建回测管理器 / Create backtest manager
                self._backtest_manager = BacktestManager(
                    qlib_wrapper=self._qlib_wrapper
                )
                
            except Exception as e:
                print(f"\n❌ 初始化回测管理器失败 / Failed to initialize backtest manager: {str(e)}")
                raise
        
        return self._backtest_manager
    
    def _get_model_registry(self):
        """
        Get or initialize the model registry.
        获取或初始化模型注册表。
        
        Returns:
            ModelRegistry instance / 模型注册表实例
        """
        if not hasattr(self, '_model_registry') or self._model_registry is None:
            try:
                from ..application.model_registry import ModelRegistry
                
                # 创建模型注册表 / Create model registry
                self._model_registry = ModelRegistry()
                
            except Exception as e:
                print(f"\n❌ 初始化模型注册表失败 / Failed to initialize model registry: {str(e)}")
                raise
        
        return self._model_registry
    
    def _run_backtest(self) -> None:
        """
        Run a new backtest.
        运行新回测。
        
        Validates: Requirements 4.1, 4.2
        """
        try:
            print("\n" + "=" * 70)
            print("🚀 运行新回测 / Run New Backtest")
            print("=" * 70)
            print()
            
            # 获取回测管理器和模型注册表 / Get backtest manager and model registry
            backtest_manager = self._get_backtest_manager()
            model_registry = self._get_model_registry()
            
            # 1. 选择模型 / Select model
            print("正在加载可用模型... / Loading available models...")
            models = model_registry.list_models()
            
            if not models:
                print("❌ 没有可用的模型 / No models available")
                print("请先训练模型 / Please train a model first")
                input("\n按回车键返回 / Press Enter to return...")
                return
            
            # 显示模型列表 / Display model list
            print("\n可用的模型 / Available Models:")
            print("-" * 70)
            model_choices = []
            for i, model in enumerate(models, 1):
                print(f"\n{i}. {model.model_name} (v{model.version})")
                print(f"   模型ID / Model ID: {model.model_id}")
                print(f"   模型类型 / Model Type: {model.model_type}")
                print(f"   训练日期 / Training Date: {model.training_date}")
                print(f"   状态 / Status: {model.status}")
                if model.performance_metrics:
                    print(f"   性能指标 / Performance Metrics:")
                    for metric, value in model.performance_metrics.items():
                        if isinstance(value, float):
                            print(f"     - {metric}: {value:.6f}")
                        else:
                            print(f"     - {metric}: {value}")
                model_choices.append(f"{model.model_name} (v{model.version})")
            
            print("-" * 70)
            
            # 选择模型 / Select model
            model_choice = self.prompt.ask_choice(
                "\n请选择要回测的模型 / Please select a model for backtest:",
                model_choices + ["返回 / Return"]
            )
            
            if model_choice == "返回 / Return":
                return
            
            # 获取选中的模型 / Get selected model
            selected_index = model_choices.index(model_choice)
            selected_model = models[selected_index]
            
            # 2. 配置回测参数 / Configure backtest parameters
            print("\n" + "=" * 70)
            print("⚙️  配置回测参数 / Configure Backtest Parameters")
            print("=" * 70)
            print()
            
            # 回测时间段 / Backtest period
            print("回测时间段配置 / Backtest Period Configuration:")
            start_date = self.prompt.ask_date(
                "请输入回测开始日期 / Please enter backtest start date",
                default="2023-01-01"
            )
            
            end_date = self.prompt.ask_date(
                "请输入回测结束日期 / Please enter backtest end date",
                default="2023-12-31"
            )
            
            # 股票池 / Stock pool
            print("\n股票池配置 / Stock Pool Configuration:")
            instruments = self.prompt.ask_choice(
                "请选择股票池 / Please select stock pool:",
                [
                    "csi300 (沪深300)",
                    "csi500 (中证500)",
                    "csi800 (中证800)",
                    "自定义 / Custom"
                ]
            )
            
            if instruments == "自定义 / Custom":
                instruments = self.prompt.ask_text(
                    "请输入股票池代码 / Please enter stock pool code:",
                    default="csi300"
                )
            else:
                instruments = instruments.split()[0]  # 提取代码部分 / Extract code part
            
            # 策略参数 / Strategy parameters
            print("\n策略参数配置 / Strategy Parameters Configuration:")
            topk = self.prompt.ask_integer(
                "请输入持仓股票数量 (topk) / Please enter number of stocks to hold (topk):",
                min_val=1,
                max_val=100,
                default=50
            )
            
            n_drop = self.prompt.ask_integer(
                "请输入每次调仓卖出数量 (n_drop) / Please enter number of stocks to drop per rebalance (n_drop):",
                min_val=0,
                max_val=topk,
                default=5
            )
            
            # 基准指数 / Benchmark index
            print("\n基准指数配置 / Benchmark Index Configuration:")
            use_benchmark = self.prompt.confirm(
                "是否使用基准指数进行对比？ / Use benchmark index for comparison?",
                default=True
            )
            
            benchmark = None
            if use_benchmark:
                benchmark_choice = self.prompt.ask_choice(
                    "请选择基准指数 / Please select benchmark index:",
                    [
                        "SH000300 (沪深300指数)",
                        "SH000905 (中证500指数)",
                        "SH000852 (中证1000指数)",
                        "自定义 / Custom"
                    ]
                )
                
                if benchmark_choice == "自定义 / Custom":
                    benchmark = self.prompt.ask_text(
                        "请输入基准指数代码 / Please enter benchmark index code:",
                        default="SH000300"
                    )
                else:
                    benchmark = benchmark_choice.split()[0]  # 提取代码部分 / Extract code part
            
            # 3. 确认配置 / Confirm configuration
            print("\n" + "=" * 70)
            print("📝 回测配置确认 / Backtest Configuration Confirmation")
            print("=" * 70)
            print(f"模型 / Model: {selected_model.model_name} (v{selected_model.version})")
            print(f"模型ID / Model ID: {selected_model.model_id}")
            print(f"回测时间段 / Backtest Period: {start_date} 至 / to {end_date}")
            print(f"股票池 / Stock Pool: {instruments}")
            print(f"持仓数量 / Position Size: {topk}")
            print(f"调仓卖出数量 / Rebalance Drop: {n_drop}")
            print(f"基准指数 / Benchmark: {benchmark if benchmark else '无 / None'}")
            print("=" * 70)
            
            if not self.prompt.confirm("\n确认开始回测？ / Confirm to start backtest?", default=True):
                print("❌ 回测已取消 / Backtest cancelled")
                return
            
            # 4. 执行回测 / Execute backtest
            print("\n" + "=" * 70)
            print("🚀 开始执行回测 / Starting Backtest Execution")
            print("=" * 70)
            print()
            
            # 构建回测配置 / Build backtest configuration
            from ..application.backtest_manager import BacktestConfig
            
            backtest_config = BacktestConfig(
                strategy_config={
                    "instruments": instruments,
                    "topk": topk,
                    "n_drop": n_drop,
                },
                executor_config={
                    "time_per_step": "day",
                },
                benchmark=benchmark if benchmark else ""
            )
            
            # 显示回测进度提示 / Display backtest progress hint
            print("⏳ 回测进行中，请稍候... / Backtest in progress, please wait...")
            print("   这可能需要几分钟时间 / This may take several minutes")
            print()
            
            # 执行回测 / Execute backtest
            result = backtest_manager.run_backtest(
                model_id=selected_model.model_id,
                start_date=start_date,
                end_date=end_date,
                config=backtest_config
            )
            
            # 5. 显示回测结果 / Display backtest results
            self._display_backtest_result(result)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  回测已中断 / Backtest interrupted")
        except Exception as e:
            print(f"\n❌ 回测失败 / Backtest failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _display_backtest_result(self, result) -> None:
        """
        Display backtest result.
        显示回测结果。
        
        Args:
            result: BacktestResult object / 回测结果对象
        """
        print("\n" + "=" * 70)
        print("✅ 回测完成！ / Backtest Completed!")
        print("=" * 70)
        print()
        
        # 显示性能指标 / Display performance metrics
        if result.metrics:
            print("性能指标 / Performance Metrics:")
            print("-" * 70)
            
            # 基本收益指标 / Basic return metrics
            if "total_return" in result.metrics:
                print(f"  总收益率 / Total Return: {result.metrics['total_return']:.2%}")
            if "annual_return" in result.metrics:
                print(f"  年化收益率 / Annual Return: {result.metrics['annual_return']:.2%}")
            
            # 风险指标 / Risk metrics
            if "volatility" in result.metrics:
                print(f"  波动率 / Volatility: {result.metrics['volatility']:.2%}")
            if "max_drawdown" in result.metrics:
                print(f"  最大回撤 / Max Drawdown: {result.metrics['max_drawdown']:.2%}")
            
            # 风险调整收益指标 / Risk-adjusted return metrics
            if "sharpe_ratio" in result.metrics:
                print(f"  夏普比率 / Sharpe Ratio: {result.metrics['sharpe_ratio']:.4f}")
            
            # 交易指标 / Trading metrics
            if "win_rate" in result.metrics:
                print(f"  胜率 / Win Rate: {result.metrics['win_rate']:.2%}")
            
            # 基准对比指标 / Benchmark comparison metrics
            if "benchmark_return" in result.metrics:
                print(f"\n  基准收益率 / Benchmark Return: {result.metrics['benchmark_return']:.2%}")
            if "excess_return" in result.metrics:
                print(f"  超额收益 / Excess Return: {result.metrics['excess_return']:.2%}")
            if "information_ratio" in result.metrics:
                print(f"  信息比率 / Information Ratio: {result.metrics['information_ratio']:.4f}")
            
            # 其他指标 / Other metrics
            if "backtest_time" in result.metrics:
                print(f"\n  回测时长 / Backtest Time: {result.metrics['backtest_time']:.2f} 秒 / seconds")
            
            print("-" * 70)
        
        # 显示交易统计 / Display trade statistics
        if result.trades:
            print(f"\n交易统计 / Trade Statistics:")
            print(f"  总交易次数 / Total Trades: {len(result.trades)}")
        
        print("\n" + "=" * 70)
        print("💡 提示 / Tips:")
        print("  • 回测结果已保存到 outputs/backtests/ 目录")
        print("    Backtest results saved to outputs/backtests/ directory")
        print("  • 可以在主菜单选择 '报告查看' 查看详细报告")
        print("    You can select 'View Reports' in main menu for detailed reports")
        print("=" * 70)
    
    def _view_backtest_results(self) -> None:
        """
        View previous backtest results.
        查看之前的回测结果。
        """
        print("\n" + "=" * 70)
        print("📊 查看回测结果 / View Backtest Results")
        print("=" * 70)
        print()
        print("⚠️  此功能将在后续版本中完善")
        print("⚠️  This feature will be improved in future versions")
        print()
        print("当前可以在 outputs/backtests/ 目录中查看保存的回测结果")
        print("Currently you can view saved backtest results in outputs/backtests/ directory")
        print()
        input("按回车键返回 / Press Enter to return...")
    
    # Training-related helper methods / 训练相关的辅助方法
    
    def _get_training_manager(self):
        """
        Get or initialize the training manager.
        获取或初始化训练管理器。
        
        Returns:
            TrainingManager instance / 训练管理器实例
        """
        if self._training_manager is None:
            try:
                from ..application.training_manager import TrainingManager
                from ..core.data_manager import DataManager
                from ..core.model_factory import ModelFactory
                from ..infrastructure.mlflow_tracker import MLflowTracker
                from ..core.config_manager import ConfigManager
                
                # 初始化配置管理器 / Initialize config manager
                if self._config_manager is None:
                    self._config_manager = ConfigManager()
                    config = self._config_manager.get_default_config()
                
                # 初始化数据管理器 / Initialize data manager
                if self._data_manager is None:
                    self._data_manager = DataManager()
                
                # 初始化模型工厂 / Initialize model factory
                if self._model_factory is None:
                    self._model_factory = ModelFactory()
                
                # 初始化MLflow追踪器（如果配置了）/ Initialize MLflow tracker (if configured)
                if self._mlflow_tracker is None:
                    try:
                        self._mlflow_tracker = MLflowTracker()
                    except Exception as e:
                        print(f"⚠️  MLflow未配置或初始化失败，将不记录实验 / MLflow not configured or failed to initialize: {str(e)}")
                        self._mlflow_tracker = None
                
                # 创建训练管理器 / Create training manager
                self._training_manager = TrainingManager(
                    data_manager=self._data_manager,
                    model_factory=self._model_factory,
                    mlflow_tracker=self._mlflow_tracker
                )
                
            except Exception as e:
                print(f"\n❌ 初始化训练管理器失败 / Failed to initialize training manager: {str(e)}")
                raise
        
        return self._training_manager
    
    def _train_from_template(self) -> None:
        """
        Train model from template.
        从模板训练模型。
        
        Validates: Requirements 2.1, 2.2, 14.1, 14.5
        """
        try:
            print("\n" + "=" * 70)
            print("📋 使用模型模板训练 / Train with Model Template")
            print("=" * 70)
            print()
            
            # 获取训练管理器 / Get training manager
            training_manager = self._get_training_manager()
            
            # 1. 列出可用模板 / List available templates
            print("正在加载模型模板... / Loading model templates...")
            templates = training_manager.list_templates()
            
            if not templates:
                print("❌ 没有可用的模型模板 / No model templates available")
                input("\n按回车键返回 / Press Enter to return...")
                return
            
            # 显示模板信息 / Display template information
            print("\n可用的模型模板 / Available Model Templates:")
            print("-" * 70)
            template_choices = []
            for i, template in enumerate(templates, 1):
                print(f"\n{i}. {template.name}")
                print(f"   模型类型 / Model Type: {template.model_type}")
                print(f"   适用场景 / Use Case: {template.use_case}")
                print(f"   描述 / Description: {template.description}")
                if template.expected_performance:
                    print(f"   预期表现 / Expected Performance:")
                    for metric, value in template.expected_performance.items():
                        print(f"     - {metric}: {value}")
                template_choices.append(template.name)
            
            print("-" * 70)
            
            # 2. 选择模板 / Select template
            template_choice = self.prompt.ask_choice(
                "\n请选择模型模板 / Please select a model template:",
                template_choices + ["返回 / Return"]
            )
            
            if template_choice == "返回 / Return":
                return
            
            # 3. 收集数据集配置 / Collect dataset configuration
            print("\n" + "=" * 70)
            print("📊 配置数据集 / Configure Dataset")
            print("=" * 70)
            print()
            
            # 股票池 / Stock pool
            instruments = self.prompt.ask_choice(
                "请选择股票池 / Please select stock pool:",
                [
                    "csi300 (沪深300)",
                    "csi500 (中证500)",
                    "csi800 (中证800)",
                    "自定义 / Custom"
                ]
            )
            
            if instruments == "自定义 / Custom":
                instruments = self.prompt.ask_text(
                    "请输入股票池代码 / Please enter stock pool code:",
                    default="csi300"
                )
            else:
                instruments = instruments.split()[0]  # 提取代码部分 / Extract code part
            
            # 时间范围 / Time range
            print("\n时间范围配置 / Time Range Configuration:")
            start_time = self.prompt.ask_date(
                "请输入开始日期 / Please enter start date",
                default="2020-01-01"
            )
            
            end_time = self.prompt.ask_date(
                "请输入结束日期 / Please enter end date",
                default="2023-12-31"
            )
            
            # 4. 询问是否自定义参数 / Ask if custom parameters needed
            use_custom_params = self.prompt.confirm(
                "\n是否需要自定义模型参数？ / Do you want to customize model parameters?",
                default=False
            )
            
            custom_params = None
            if use_custom_params:
                print("\n⚠️  自定义参数功能将在后续版本中完善")
                print("⚠️  Custom parameters feature will be improved in future versions")
                print("当前将使用模板默认参数 / Will use template default parameters")
            
            # 5. 实验名称 / Experiment name
            experiment_name = self.prompt.ask_text(
                "\n请输入实验名称 / Please enter experiment name:",
                default=f"{template_choice}_{instruments}"
            )
            
            # 6. 确认配置 / Confirm configuration
            print("\n" + "=" * 70)
            print("📝 训练配置确认 / Training Configuration Confirmation")
            print("=" * 70)
            print(f"模板名称 / Template: {template_choice}")
            print(f"股票池 / Stock Pool: {instruments}")
            print(f"开始日期 / Start Date: {start_time}")
            print(f"结束日期 / End Date: {end_time}")
            print(f"实验名称 / Experiment Name: {experiment_name}")
            print("=" * 70)
            
            if not self.prompt.confirm("\n确认开始训练？ / Confirm to start training?", default=True):
                print("❌ 训练已取消 / Training cancelled")
                return
            
            # 7. 开始训练 / Start training
            print("\n" + "=" * 70)
            print("🚀 开始训练模型 / Starting Model Training")
            print("=" * 70)
            print()
            
            # 构建数据集配置 / Build dataset configuration
            from ..application.training_manager import DatasetConfig
            
            dataset_config = DatasetConfig(
                instruments=instruments,
                start_time=start_time,
                end_time=end_time,
                features=[],  # 将使用模型默认特征 / Will use model default features
                label="Ref($close, -2) / Ref($close, -1) - 1"  # 默认标签 / Default label
            )
            
            # 显示训练进度提示 / Display training progress hint
            print("⏳ 训练进行中，请稍候... / Training in progress, please wait...")
            print("   这可能需要几分钟时间 / This may take several minutes")
            print()
            
            # 执行训练 / Execute training
            result = training_manager.train_from_template(
                template_name=template_choice,
                dataset_config=dataset_config,
                experiment_name=experiment_name,
                custom_params=custom_params
            )
            
            # 8. 显示训练结果 / Display training results
            self._display_training_result(result)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  训练已中断 / Training interrupted")
        except Exception as e:
            print(f"\n❌ 训练失败 / Training failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _train_with_custom_params(self) -> None:
        """
        Train model with custom parameters.
        使用自定义参数训练模型。
        
        Validates: Requirements 2.1, 2.2
        """
        print("\n" + "=" * 70)
        print("⚙️  自定义参数训练 / Train with Custom Parameters")
        print("=" * 70)
        print()
        print("⚠️  此功能将在后续版本中完善")
        print("⚠️  This feature will be improved in future versions")
        print()
        print("当前建议使用模板训练功能")
        print("Currently recommend using template training feature")
        print()
        input("按回车键返回 / Press Enter to return...")
    
    def _display_training_result(self, result) -> None:
        """
        Display training result.
        显示训练结果。
        
        Args:
            result: TrainingResult object / 训练结果对象
        """
        print("\n" + "=" * 70)
        print("✅ 训练完成！ / Training Completed!")
        print("=" * 70)
        print()
        print(f"模型ID / Model ID: {result.model_id}")
        print(f"训练时长 / Training Time: {result.training_time:.2f} 秒 / seconds")
        print(f"模型路径 / Model Path: {result.model_path}")
        print()
        
        if result.metrics:
            print("评估指标 / Evaluation Metrics:")
            print("-" * 70)
            for metric_name, metric_value in result.metrics.items():
                if isinstance(metric_value, float):
                    print(f"  {metric_name}: {metric_value:.6f}")
                else:
                    print(f"  {metric_name}: {metric_value}")
            print("-" * 70)
        
        if result.experiment_id:
            print(f"\n实验ID / Experiment ID: {result.experiment_id}")
            print(f"运行ID / Run ID: {result.run_id}")
            print("\n💡 提示：可以使用 MLflow UI 查看详细的训练记录")
            print("💡 Tip: You can use MLflow UI to view detailed training records")
            print("   运行命令 / Run command: mlflow ui")
        
        print("\n" + "=" * 70)


    # Data management-related helper methods / 数据管理相关的辅助方法
    
    def _get_data_manager(self):
        """
        Get or initialize the data manager.
        获取或初始化数据管理器。
        
        Returns:
            DataManager instance / 数据管理器实例
        """
        if self._data_manager is None:
            try:
                from ..core.data_manager import DataManager
                from ..infrastructure.qlib_wrapper import QlibWrapper
                
                # 初始化qlib封装器 / Initialize qlib wrapper
                if not hasattr(self, '_qlib_wrapper') or self._qlib_wrapper is None:
                    self._qlib_wrapper = QlibWrapper()
                
                # 创建数据管理器 / Create data manager
                self._data_manager = DataManager(qlib_wrapper=self._qlib_wrapper)
                
            except Exception as e:
                print(f"\n❌ 初始化数据管理器失败 / Failed to initialize data manager: {str(e)}")
                raise
        
        return self._data_manager
    
    def _download_market_data(self) -> None:
        """
        Download market data.
        下载市场数据。
        
        Validates: Requirements 9.1
        """
        try:
            print("\n" + "=" * 70)
            print("📥 下载市场数据 / Download Market Data")
            print("=" * 70)
            print()
            
            # 1. 选择市场区域 / Select market region
            region_choice = self.prompt.ask_choice(
                "请选择市场区域 / Please select market region:",
                [
                    "cn (中国市场 / China Market)",
                    "us (美国市场 / US Market)",
                    "返回 / Return"
                ]
            )
            
            if region_choice == "返回 / Return":
                return
            
            region = region_choice.split()[0]  # 提取代码部分 / Extract code part
            
            # 2. 配置目标目录 / Configure target directory
            default_dir = f"~/.qlib/qlib_data/{region}_data"
            target_dir = self.prompt.ask_text(
                f"\n请输入数据保存目录 / Please enter data save directory:",
                default=default_dir
            )
            
            # 3. 选择数据间隔 / Select data interval
            interval_choice = self.prompt.ask_choice(
                "\n请选择数据间隔 / Please select data interval:",
                [
                    "1d (日线数据 / Daily data)",
                    "1min (分钟数据 / Minute data)",
                    "返回 / Return"
                ]
            )
            
            if interval_choice == "返回 / Return":
                return
            
            interval = interval_choice.split()[0]  # 提取代码部分 / Extract code part
            
            # 4. 询问是否指定时间范围 / Ask if specify time range
            use_time_range = self.prompt.confirm(
                "\n是否指定下载时间范围？ / Specify download time range?",
                default=False
            )
            
            start_date = None
            end_date = None
            if use_time_range:
                start_date = self.prompt.ask_date(
                    "请输入开始日期 / Please enter start date:",
                    default="2020-01-01"
                )
                end_date = self.prompt.ask_date(
                    "请输入结束日期 / Please enter end date:",
                    default=datetime.now().strftime("%Y-%m-%d")
                )
            
            # 5. 确认配置 / Confirm configuration
            print("\n" + "=" * 70)
            print("📝 下载配置确认 / Download Configuration Confirmation")
            print("=" * 70)
            print(f"市场区域 / Market Region: {region}")
            print(f"目标目录 / Target Directory: {target_dir}")
            print(f"数据间隔 / Data Interval: {interval}")
            if start_date and end_date:
                print(f"时间范围 / Time Range: {start_date} 至 / to {end_date}")
            else:
                print(f"时间范围 / Time Range: 全部可用数据 / All available data")
            print("=" * 70)
            
            if not self.prompt.confirm("\n确认开始下载？ / Confirm to start download?", default=True):
                print("❌ 下载已取消 / Download cancelled")
                return
            
            # 6. 执行下载 / Execute download
            print("\n" + "=" * 70)
            print("🚀 开始下载数据 / Starting Data Download")
            print("=" * 70)
            print()
            
            # 获取数据管理器 / Get data manager
            data_manager = self._get_data_manager()
            
            # 显示下载说明 / Display download instructions
            print("⏳ 准备下载数据... / Preparing to download data...")
            print()
            print("📌 重要提示 / Important Notes:")
            print("=" * 70)
            print()
            print("由于qlib数据下载需要使用命令行工具，请按照以下步骤操作：")
            print("Since qlib data download requires command-line tools, please follow these steps:")
            print()
            print("1. 打开新的终端窗口 / Open a new terminal window")
            print()
            print("2. 运行以下命令下载数据 / Run the following command to download data:")
            print()
            print("   " + "-" * 66)
            
            # 构建下载命令 / Build download command
            if region == "cn":
                print(f"   python -m qlib.run.get_data qlib_data \\")
                print(f"       --target_dir {target_dir} \\")
                print(f"       --region {region} \\")
                print(f"       --interval {interval}")
            else:
                print(f"   python -m qlib.run.get_data qlib_data \\")
                print(f"       --target_dir {target_dir} \\")
                print(f"       --region {region} \\")
                print(f"       --interval {interval}")
            
            print("   " + "-" * 66)
            print()
            print("3. 等待下载完成 / Wait for download to complete")
            print()
            print("4. 下载完成后，返回本系统验证数据 / After download, return to validate data")
            print()
            print("=" * 70)
            print()
            
            # 尝试调用下载功能 / Try to call download function
            try:
                data_manager.download_data(
                    region=region,
                    target_dir=target_dir,
                    interval=interval,
                    start_date=start_date,
                    end_date=end_date
                )
            except Exception as e:
                print(f"⚠️  自动下载失败 / Automatic download failed: {str(e)}")
                print("请使用上述命令手动下载 / Please use the above command to download manually")
            
            print("\n💡 提示 / Tips:")
            print("  • 首次下载可能需要较长时间 / First download may take a long time")
            print("  • 确保网络连接稳定 / Ensure stable network connection")
            print("  • 下载完成后可以在数据管理菜单中验证数据")
            print("    After download, you can validate data in data management menu")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  下载已中断 / Download interrupted")
        except Exception as e:
            print(f"\n❌ 下载失败 / Download failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _validate_data_integrity(self) -> None:
        """
        Validate data integrity.
        验证数据完整性。
        
        Validates: Requirements 9.2
        """
        try:
            print("\n" + "=" * 70)
            print("✅ 验证数据完整性 / Validate Data Integrity")
            print("=" * 70)
            print()
            
            # 获取数据管理器 / Get data manager
            data_manager = self._get_data_manager()
            
            # 1. 检查数据管理器是否已初始化 / Check if data manager is initialized
            if not data_manager.is_initialized():
                print("⚠️  数据管理器未初始化 / Data manager not initialized")
                print()
                
                # 询问是否初始化 / Ask if initialize
                if not self.prompt.confirm("是否现在初始化？ / Initialize now?", default=True):
                    return
                
                # 配置初始化参数 / Configure initialization parameters
                region_choice = self.prompt.ask_choice(
                    "\n请选择市场区域 / Please select market region:",
                    [
                        "cn (中国市场 / China Market)",
                        "us (美国市场 / US Market)",
                        "返回 / Return"
                    ]
                )
                
                if region_choice == "返回 / Return":
                    return
                
                region = region_choice.split()[0]  # 提取代码部分 / Extract code part
                
                default_path = f"~/.qlib/qlib_data/{region}_data"
                data_path = self.prompt.ask_text(
                    f"\n请输入数据路径 / Please enter data path:",
                    default=default_path
                )
                
                # 初始化数据管理器 / Initialize data manager
                print("\n⏳ 正在初始化数据管理器... / Initializing data manager...")
                try:
                    data_manager.initialize(
                        data_path=data_path,
                        region=region
                    )
                    print("✅ 数据管理器初始化成功 / Data manager initialized successfully")
                except Exception as e:
                    print(f"❌ 初始化失败 / Initialization failed: {str(e)}")
                    print("\n可能的原因 / Possible reasons:")
                    print("  • 数据路径不存在 / Data path does not exist")
                    print("  • 数据未下载 / Data not downloaded")
                    print("  • 数据格式不正确 / Data format incorrect")
                    print("\n请先下载数据 / Please download data first")
                    return
            
            # 2. 配置验证参数 / Configure validation parameters
            print("\n" + "=" * 70)
            print("⚙️  配置验证参数 / Configure Validation Parameters")
            print("=" * 70)
            print()
            
            # 询问是否指定时间范围 / Ask if specify time range
            use_time_range = self.prompt.confirm(
                "是否指定验证时间范围？ / Specify validation time range?",
                default=False
            )
            
            start_date = None
            end_date = None
            if use_time_range:
                start_date = self.prompt.ask_date(
                    "请输入开始日期 / Please enter start date:",
                    default="2020-01-01"
                )
                end_date = self.prompt.ask_date(
                    "请输入结束日期 / Please enter end date:",
                    default=datetime.now().strftime("%Y-%m-%d")
                )
            
            # 选择股票池 / Select stock pool
            instruments_choice = self.prompt.ask_choice(
                "\n请选择股票池 / Please select stock pool:",
                [
                    "csi300 (沪深300)",
                    "csi500 (中证500)",
                    "csi800 (中证800)",
                    "all (全部股票 / All stocks)",
                    "自定义 / Custom"
                ]
            )
            
            if instruments_choice == "自定义 / Custom":
                instruments = self.prompt.ask_text(
                    "请输入股票池代码 / Please enter stock pool code:",
                    default="csi300"
                )
            else:
                instruments = instruments_choice.split()[0]  # 提取代码部分 / Extract code part
            
            # 3. 执行验证 / Execute validation
            print("\n" + "=" * 70)
            print("🚀 开始验证数据 / Starting Data Validation")
            print("=" * 70)
            print()
            
            print("⏳ 验证进行中，请稍候... / Validation in progress, please wait...")
            print()
            
            # 执行数据验证 / Execute data validation
            result = data_manager.validate_data(
                start_date=start_date,
                end_date=end_date,
                instruments=instruments
            )
            
            # 4. 显示验证结果 / Display validation results
            print("\n" + "=" * 70)
            if result.is_valid:
                print("✅ 数据验证通过！ / Data Validation Passed!")
            else:
                print("❌ 数据验证失败！ / Data Validation Failed!")
            print("=" * 70)
            print()
            
            print(f"验证消息 / Validation Message:")
            print(f"  {result.message}")
            print()
            
            if result.data_start and result.data_end:
                print(f"数据时间范围 / Data Time Range:")
                print(f"  开始日期 / Start Date: {result.data_start}")
                print(f"  结束日期 / End Date: {result.data_end}")
                print(f"  交易日数 / Trading Days: {result.trading_days}")
                print()
            
            if result.issues:
                print("发现的问题 / Issues Found:")
                print("-" * 70)
                for i, issue in enumerate(result.issues, 1):
                    print(f"  {i}. {issue}")
                print("-" * 70)
                print()
                
                print("💡 建议 / Suggestions:")
                print("  • 如果数据缺失，请重新下载数据")
                print("    If data is missing, please re-download data")
                print("  • 如果数据损坏，请删除后重新下载")
                print("    If data is corrupted, please delete and re-download")
                print("  • 检查数据路径是否正确")
                print("    Check if data path is correct")
            else:
                print("✅ 未发现问题，数据完整性良好")
                print("✅ No issues found, data integrity is good")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  验证已中断 / Validation interrupted")
        except Exception as e:
            print(f"\n❌ 验证失败 / Validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _view_data_info(self) -> None:
        """
        View data information.
        查看数据信息。
        
        Validates: Requirements 9.1, 9.2
        """
        try:
            print("\n" + "=" * 70)
            print("📊 查看数据信息 / View Data Information")
            print("=" * 70)
            print()
            
            # 获取数据管理器 / Get data manager
            data_manager = self._get_data_manager()
            
            # 检查数据管理器是否已初始化 / Check if data manager is initialized
            if not data_manager.is_initialized():
                print("⚠️  数据管理器未初始化 / Data manager not initialized")
                print()
                print("请先在数据管理菜单中验证数据以初始化数据管理器")
                print("Please validate data in data management menu to initialize data manager first")
                return
            
            # 获取数据信息 / Get data information
            print("⏳ 正在获取数据信息... / Getting data information...")
            print()
            
            data_info = data_manager.get_data_info()
            
            # 显示数据信息 / Display data information
            print("=" * 70)
            print("📈 数据信息 / Data Information")
            print("=" * 70)
            print()
            
            print(f"数据提供者 / Data Provider:")
            print(f"  {data_info.provider_uri}")
            print()
            
            print(f"市场区域 / Market Region:")
            print(f"  {data_info.region}")
            print()
            
            print(f"数据时间范围 / Data Time Range:")
            print(f"  开始日期 / Start Date: {data_info.data_start}")
            print(f"  结束日期 / End Date: {data_info.data_end}")
            print(f"  交易日数 / Trading Days: {data_info.trading_days}")
            print()
            
            if data_info.instruments_count:
                print(f"股票数量 / Number of Instruments:")
                print(f"  {data_info.instruments_count}")
                print()
            
            if data_info.last_updated:
                print(f"最后更新 / Last Updated:")
                print(f"  {data_info.last_updated}")
                print()
            
            print("=" * 70)
            print()
            
            print("💡 提示 / Tips:")
            print("  • 数据时间范围决定了可以进行训练和回测的时间段")
            print("    Data time range determines the period for training and backtesting")
            print("  • 如需更新数据，请使用数据下载功能")
            print("    To update data, please use data download function")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作已中断 / Operation interrupted")
        except Exception as e:
            print(f"\n❌ 获取数据信息失败 / Failed to get data information: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _check_data_coverage(self) -> None:
        """
        Check data coverage for a specific time range.
        检查特定时间范围的数据覆盖。
        
        Validates: Requirements 9.2
        """
        try:
            print("\n" + "=" * 70)
            print("🔍 检查数据覆盖 / Check Data Coverage")
            print("=" * 70)
            print()
            
            # 获取数据管理器 / Get data manager
            data_manager = self._get_data_manager()
            
            # 检查数据管理器是否已初始化 / Check if data manager is initialized
            if not data_manager.is_initialized():
                print("⚠️  数据管理器未初始化 / Data manager not initialized")
                print()
                print("请先在数据管理菜单中验证数据以初始化数据管理器")
                print("Please validate data in data management menu to initialize data manager first")
                return
            
            # 1. 配置检查参数 / Configure check parameters
            print("请输入需要检查的时间范围 / Please enter the time range to check:")
            print()
            
            required_start = self.prompt.ask_date(
                "请输入开始日期 / Please enter start date:",
                default="2020-01-01"
            )
            
            required_end = self.prompt.ask_date(
                "请输入结束日期 / Please enter end date:",
                default="2023-12-31"
            )
            
            # 选择股票池 / Select stock pool
            instruments_choice = self.prompt.ask_choice(
                "\n请选择股票池 / Please select stock pool:",
                [
                    "csi300 (沪深300)",
                    "csi500 (中证500)",
                    "csi800 (中证800)",
                    "all (全部股票 / All stocks)",
                    "自定义 / Custom"
                ]
            )
            
            if instruments_choice == "自定义 / Custom":
                instruments = self.prompt.ask_text(
                    "请输入股票池代码 / Please enter stock pool code:",
                    default="csi300"
                )
            else:
                instruments = instruments_choice.split()[0]  # 提取代码部分 / Extract code part
            
            # 2. 执行检查 / Execute check
            print("\n" + "=" * 70)
            print("🚀 开始检查数据覆盖 / Starting Data Coverage Check")
            print("=" * 70)
            print()
            
            print("⏳ 检查进行中，请稍候... / Check in progress, please wait...")
            print()
            
            # 执行数据覆盖检查 / Execute data coverage check
            is_covered, message = data_manager.check_data_coverage(
                required_start=required_start,
                required_end=required_end,
                instruments=instruments
            )
            
            # 3. 显示检查结果 / Display check results
            print("\n" + "=" * 70)
            if is_covered:
                print("✅ 数据覆盖检查通过！ / Data Coverage Check Passed!")
            else:
                print("❌ 数据覆盖不足！ / Data Coverage Insufficient!")
            print("=" * 70)
            print()
            
            print(message)
            print()
            
            if not is_covered:
                print("💡 建议 / Suggestions:")
                print("  • 下载更多历史数据以覆盖所需时间范围")
                print("    Download more historical data to cover required time range")
                print("  • 调整训练或回测的时间范围")
                print("    Adjust training or backtesting time range")
                print("  • 检查数据下载是否完整")
                print("    Check if data download is complete")
            else:
                print("✅ 数据覆盖充足，可以进行训练和回测")
                print("✅ Data coverage is sufficient for training and backtesting")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  检查已中断 / Check interrupted")
        except Exception as e:
            print(f"\n❌ 检查失败 / Check failed: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    # Model management-related helper methods / 模型管理相关的辅助方法
    
    def _view_model_list(self) -> None:
        """
        View list of all registered models.
        查看所有已注册模型的列表。
        
        Validates: Requirements 7.3
        """
        try:
            print("\n" + "=" * 70)
            print("📋 模型列表 / Model List")
            print("=" * 70)
            print()
            
            # 获取模型注册表 / Get model registry
            model_registry = self._get_model_registry()
            
            # 1. 询问是否需要过滤 / Ask if filtering is needed
            use_filter = self.prompt.confirm(
                "是否需要过滤模型？ / Do you want to filter models?",
                default=False
            )
            
            model_filter = None
            if use_filter:
                from ..application.model_registry import ModelFilter
                
                # 按状态过滤 / Filter by status
                status_choice = self.prompt.ask_choice(
                    "\n请选择模型状态 / Please select model status:",
                    [
                        "全部 / All",
                        "registered (已注册 / Registered)",
                        "candidate (候选 / Candidate)",
                        "production (生产 / Production)",
                        "archived (已归档 / Archived)"
                    ]
                )
                
                status = None if status_choice == "全部 / All" else status_choice.split()[0]
                
                # 按模型类型过滤 / Filter by model type
                type_choice = self.prompt.ask_choice(
                    "\n请选择模型类型 / Please select model type:",
                    [
                        "全部 / All",
                        "lgbm (LightGBM)",
                        "linear (线性模型 / Linear)",
                        "mlp (多层感知机 / MLP)",
                        "其他 / Other"
                    ]
                )
                
                model_type = None if type_choice == "全部 / All" else type_choice.split()[0]
                
                model_filter = ModelFilter(
                    status=status,
                    model_type=model_type
                )
            
            # 2. 获取模型列表 / Get model list
            print("\n⏳ 正在加载模型列表... / Loading model list...")
            models = model_registry.list_models(filter=model_filter)
            
            if not models:
                print("\n❌ 没有找到符合条件的模型 / No models found matching criteria")
                return
            
            # 3. 显示模型列表 / Display model list
            print(f"\n找到 {len(models)} 个模型 / Found {len(models)} models")
            print("=" * 70)
            
            for i, model in enumerate(models, 1):
                # 状态图标 / Status icon
                status_icon = {
                    "registered": "📝",
                    "candidate": "⭐",
                    "production": "🚀",
                    "archived": "📦"
                }.get(model.status, "❓")
                
                print(f"\n{i}. {status_icon} {model.model_name} (v{model.version})")
                print(f"   模型ID / Model ID: {model.model_id}")
                print(f"   模型类型 / Model Type: {model.model_type}")
                print(f"   训练日期 / Training Date: {model.training_date}")
                print(f"   状态 / Status: {model.status}")
                
                # 显示关键性能指标 / Display key performance metrics
                if model.performance_metrics:
                    print(f"   性能指标 / Performance Metrics:")
                    # 只显示前3个最重要的指标 / Only show top 3 most important metrics
                    important_metrics = ["ic_mean", "icir", "rank_ic_mean"]
                    shown_count = 0
                    for metric in important_metrics:
                        if metric in model.performance_metrics and shown_count < 3:
                            value = model.performance_metrics[metric]
                            if isinstance(value, float):
                                print(f"     - {metric}: {value:.6f}")
                            else:
                                print(f"     - {metric}: {value}")
                            shown_count += 1
                    
                    # 如果还有其他指标，显示数量 / If there are more metrics, show count
                    remaining = len(model.performance_metrics) - shown_count
                    if remaining > 0:
                        print(f"     ... 还有 {remaining} 个指标 / ... {remaining} more metrics")
            
            print("\n" + "=" * 70)
            print()
            
            # 4. 显示统计信息 / Display statistics
            status_counts = {}
            for model in models:
                status_counts[model.status] = status_counts.get(model.status, 0) + 1
            
            print("状态统计 / Status Statistics:")
            for status, count in status_counts.items():
                print(f"  {status}: {count}")
            
            print()
            print("💡 提示 / Tips:")
            print("  • 选择 '查看模型详情' 可以查看完整的模型信息")
            print("    Select 'View model details' to see complete model information")
            print("  • ⭐ 候选模型表示性能优于当前生产模型")
            print("    ⭐ Candidate models indicate better performance than current production model")
            print("  • 🚀 生产模型是当前用于实际预测的模型")
            print("    🚀 Production model is currently used for actual predictions")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作已中断 / Operation interrupted")
        except Exception as e:
            print(f"\n❌ 查看模型列表失败 / Failed to view model list: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _view_model_details(self) -> None:
        """
        View detailed information of a specific model.
        查看特定模型的详细信息。
        
        Validates: Requirements 7.4
        """
        try:
            print("\n" + "=" * 70)
            print("🔍 查看模型详情 / View Model Details")
            print("=" * 70)
            print()
            
            # 获取模型注册表 / Get model registry
            model_registry = self._get_model_registry()
            
            # 1. 获取模型列表 / Get model list
            print("正在加载模型列表... / Loading model list...")
            models = model_registry.list_models()
            
            if not models:
                print("\n❌ 没有可用的模型 / No models available")
                return
            
            # 2. 选择模型 / Select model
            print("\n可用的模型 / Available Models:")
            print("-" * 70)
            model_choices = []
            for i, model in enumerate(models, 1):
                status_icon = {
                    "registered": "📝",
                    "candidate": "⭐",
                    "production": "🚀",
                    "archived": "📦"
                }.get(model.status, "❓")
                
                print(f"{i}. {status_icon} {model.model_name} (v{model.version}) - {model.status}")
                model_choices.append(f"{model.model_name} (v{model.version})")
            
            print("-" * 70)
            
            model_choice = self.prompt.ask_choice(
                "\n请选择要查看的模型 / Please select a model to view:",
                model_choices + ["返回 / Return"]
            )
            
            if model_choice == "返回 / Return":
                return
            
            # 获取选中的模型 / Get selected model
            selected_index = model_choices.index(model_choice)
            selected_model = models[selected_index]
            
            # 3. 获取模型元数据 / Get model metadata
            print("\n⏳ 正在加载模型详情... / Loading model details...")
            metadata = model_registry.get_model_metadata(selected_model.model_id)
            
            # 4. 显示详细信息 / Display detailed information
            print("\n" + "=" * 70)
            print("📊 模型详细信息 / Model Detailed Information")
            print("=" * 70)
            print()
            
            # 基本信息 / Basic information
            print("【基本信息 / Basic Information】")
            print(f"  模型ID / Model ID: {selected_model.model_id}")
            print(f"  模型名称 / Model Name: {selected_model.model_name}")
            print(f"  版本 / Version: {selected_model.version}")
            print(f"  模型类型 / Model Type: {selected_model.model_type}")
            print(f"  训练日期 / Training Date: {selected_model.training_date}")
            print(f"  状态 / Status: {selected_model.status}")
            if "registered_at" in metadata:
                print(f"  注册时间 / Registered At: {metadata['registered_at']}")
            print()
            
            # 数据集信息 / Dataset information
            if "dataset_info" in metadata:
                dataset = metadata["dataset_info"]
                print("【数据集信息 / Dataset Information】")
                print(f"  股票池 / Instruments: {dataset.get('instruments', 'N/A')}")
                print(f"  开始时间 / Start Time: {dataset.get('start_time', 'N/A')}")
                print(f"  结束时间 / End Time: {dataset.get('end_time', 'N/A')}")
                print(f"  标签 / Label: {dataset.get('label', 'N/A')}")
                if dataset.get('features'):
                    print(f"  特征数量 / Number of Features: {len(dataset['features'])}")
                print()
            
            # 超参数 / Hyperparameters
            if "hyperparameters" in metadata and metadata["hyperparameters"]:
                print("【超参数 / Hyperparameters】")
                for param, value in metadata["hyperparameters"].items():
                    if isinstance(value, (dict, list)):
                        print(f"  {param}: {type(value).__name__}")
                    else:
                        print(f"  {param}: {value}")
                print()
            
            # 性能指标 / Performance metrics
            if selected_model.performance_metrics:
                print("【性能指标 / Performance Metrics】")
                for metric, value in selected_model.performance_metrics.items():
                    if isinstance(value, float):
                        print(f"  {metric}: {value:.6f}")
                    else:
                        print(f"  {metric}: {value}")
                print()
            
            # 文件路径 / File paths
            print("【文件路径 / File Paths】")
            print(f"  模型文件 / Model File: {selected_model.model_path}")
            print(f"  元数据文件 / Metadata File: {selected_model.metadata_path}")
            print()
            
            print("=" * 70)
            print()
            
            # 5. 提供操作选项 / Provide operation options
            action_choice = self.prompt.ask_choice(
                "请选择操作 / Please select an operation:",
                [
                    "设置为生产模型 / Set as production model",
                    "导出模型信息 / Export model information",
                    "返回 / Return"
                ]
            )
            
            if action_choice == "设置为生产模型 / Set as production model":
                if self.prompt.confirm(
                    f"\n确认将 {selected_model.model_name} (v{selected_model.version}) 设置为生产模型？\n"
                    f"Confirm to set {selected_model.model_name} (v{selected_model.version}) as production model?",
                    default=False
                ):
                    model_registry.set_production_model(selected_model.model_id)
                    print("\n✅ 生产模型设置成功！ / Production model set successfully!")
            elif action_choice == "导出模型信息 / Export model information":
                self._export_model_info(selected_model, metadata)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作已中断 / Operation interrupted")
        except Exception as e:
            print(f"\n❌ 查看模型详情失败 / Failed to view model details: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _set_production_model(self) -> None:
        """
        Set a model as the production model.
        将模型设置为生产模型。
        
        Validates: Requirements 7.5
        """
        try:
            print("\n" + "=" * 70)
            print("🚀 设置生产模型 / Set Production Model")
            print("=" * 70)
            print()
            
            # 获取模型注册表 / Get model registry
            model_registry = self._get_model_registry()
            
            # 1. 显示当前生产模型 / Display current production model
            current_production = model_registry.get_production_model()
            
            if current_production:
                print("当前生产模型 / Current Production Model:")
                print(f"  {current_production.model_name} (v{current_production.version})")
                print(f"  模型ID / Model ID: {current_production.model_id}")
                print(f"  训练日期 / Training Date: {current_production.training_date}")
                if current_production.performance_metrics:
                    print(f"  性能指标 / Performance Metrics:")
                    for metric, value in list(current_production.performance_metrics.items())[:3]:
                        if isinstance(value, float):
                            print(f"    - {metric}: {value:.6f}")
                        else:
                            print(f"    - {metric}: {value}")
                print()
            else:
                print("⚠️  当前没有生产模型 / No production model currently set")
                print()
            
            # 2. 获取候选模型和其他模型 / Get candidate models and other models
            print("正在加载可用模型... / Loading available models...")
            
            from ..application.model_registry import ModelFilter
            
            # 获取候选模型 / Get candidate models
            candidate_models = model_registry.list_models(
                filter=ModelFilter(status="candidate")
            )
            
            # 获取已注册模型 / Get registered models
            registered_models = model_registry.list_models(
                filter=ModelFilter(status="registered")
            )
            
            all_models = candidate_models + registered_models
            
            if not all_models:
                print("\n❌ 没有可用的模型 / No models available")
                print("请先训练模型 / Please train a model first")
                return
            
            # 3. 显示可选模型 / Display available models
            print(f"\n可选模型 / Available Models ({len(all_models)}):")
            print("-" * 70)
            
            model_choices = []
            for i, model in enumerate(all_models, 1):
                status_icon = "⭐" if model.status == "candidate" else "📝"
                
                print(f"\n{i}. {status_icon} {model.model_name} (v{model.version})")
                print(f"   模型ID / Model ID: {model.model_id}")
                print(f"   训练日期 / Training Date: {model.training_date}")
                print(f"   状态 / Status: {model.status}")
                
                if model.performance_metrics:
                    print(f"   性能指标 / Performance Metrics:")
                    for metric, value in list(model.performance_metrics.items())[:3]:
                        if isinstance(value, float):
                            print(f"     - {metric}: {value:.6f}")
                        else:
                            print(f"     - {metric}: {value}")
                
                # 如果是候选模型，显示与当前生产模型的对比 / If candidate, show comparison
                if model.status == "candidate" and current_production:
                    ic_new = model.performance_metrics.get("ic_mean", 0)
                    ic_prod = current_production.performance_metrics.get("ic_mean", 0)
                    if ic_new > ic_prod:
                        improvement = ((ic_new - ic_prod) / abs(ic_prod)) * 100 if ic_prod != 0 else 0
                        print(f"   💡 性能提升 / Performance Improvement: +{improvement:.2f}%")
                
                model_choices.append(f"{model.model_name} (v{model.version})")
            
            print("-" * 70)
            
            # 4. 选择模型 / Select model
            model_choice = self.prompt.ask_choice(
                "\n请选择要设置为生产模型的模型 / Please select a model to set as production:",
                model_choices + ["返回 / Return"]
            )
            
            if model_choice == "返回 / Return":
                return
            
            # 获取选中的模型 / Get selected model
            selected_index = model_choices.index(model_choice)
            selected_model = all_models[selected_index]
            
            # 5. 确认设置 / Confirm setting
            print("\n" + "=" * 70)
            print("📝 设置确认 / Setting Confirmation")
            print("=" * 70)
            print()
            
            if current_production:
                print("当前生产模型 / Current Production Model:")
                print(f"  {current_production.model_name} (v{current_production.version})")
                print()
                print("将被替换为 / Will be replaced by:")
            else:
                print("将设置为生产模型 / Will be set as production model:")
            
            print(f"  {selected_model.model_name} (v{selected_model.version})")
            print(f"  模型ID / Model ID: {selected_model.model_id}")
            print()
            
            if not self.prompt.confirm("确认设置？ / Confirm setting?", default=True):
                print("❌ 设置已取消 / Setting cancelled")
                return
            
            # 6. 执行设置 / Execute setting
            print("\n⏳ 正在设置生产模型... / Setting production model...")
            model_registry.set_production_model(selected_model.model_id)
            
            print("\n" + "=" * 70)
            print("✅ 生产模型设置成功！ / Production Model Set Successfully!")
            print("=" * 70)
            print()
            print(f"新的生产模型 / New Production Model:")
            print(f"  {selected_model.model_name} (v{selected_model.version})")
            print(f"  模型ID / Model ID: {selected_model.model_id}")
            print()
            
            if current_production:
                print(f"原生产模型已降级为候选模型 / Previous production model demoted to candidate:")
                print(f"  {current_production.model_name} (v{current_production.version})")
                print()
            
            print("💡 提示 / Tips:")
            print("  • 新的生产模型将用于后续的信号生成和回测")
            print("    New production model will be used for signal generation and backtesting")
            print("  • 可以随时切换回其他模型")
            print("    You can switch back to other models anytime")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作已中断 / Operation interrupted")
        except Exception as e:
            print(f"\n❌ 设置生产模型失败 / Failed to set production model: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _delete_model(self) -> None:
        """
        Delete a model from the registry.
        从注册表中删除模型。
        
        Note: Cannot delete production models.
        注意：不能删除生产模型。
        """
        try:
            print("\n" + "=" * 70)
            print("🗑️  删除模型 / Delete Model")
            print("=" * 70)
            print()
            
            # 获取模型注册表 / Get model registry
            model_registry = self._get_model_registry()
            
            # 1. 获取可删除的模型（非生产模型）/ Get deletable models (non-production)
            print("正在加载可删除的模型... / Loading deletable models...")
            
            from ..application.model_registry import ModelFilter
            
            # 获取已注册和已归档的模型 / Get registered and archived models
            registered_models = model_registry.list_models(
                filter=ModelFilter(status="registered")
            )
            archived_models = model_registry.list_models(
                filter=ModelFilter(status="archived")
            )
            candidate_models = model_registry.list_models(
                filter=ModelFilter(status="candidate")
            )
            
            deletable_models = registered_models + archived_models + candidate_models
            
            if not deletable_models:
                print("\n⚠️  没有可删除的模型 / No deletable models")
                print("注意：生产模型不能被删除 / Note: Production models cannot be deleted")
                return
            
            # 2. 显示可删除的模型 / Display deletable models
            print(f"\n可删除的模型 / Deletable Models ({len(deletable_models)}):")
            print("-" * 70)
            
            model_choices = []
            for i, model in enumerate(deletable_models, 1):
                status_icon = {
                    "registered": "📝",
                    "candidate": "⭐",
                    "archived": "📦"
                }.get(model.status, "❓")
                
                print(f"\n{i}. {status_icon} {model.model_name} (v{model.version})")
                print(f"   模型ID / Model ID: {model.model_id}")
                print(f"   训练日期 / Training Date: {model.training_date}")
                print(f"   状态 / Status: {model.status}")
                
                model_choices.append(f"{model.model_name} (v{model.version})")
            
            print("-" * 70)
            
            # 3. 选择要删除的模型 / Select model to delete
            model_choice = self.prompt.ask_choice(
                "\n请选择要删除的模型 / Please select a model to delete:",
                model_choices + ["返回 / Return"]
            )
            
            if model_choice == "返回 / Return":
                return
            
            # 获取选中的模型 / Get selected model
            selected_index = model_choices.index(model_choice)
            selected_model = deletable_models[selected_index]
            
            # 4. 确认删除 / Confirm deletion
            print("\n" + "=" * 70)
            print("⚠️  删除确认 / Deletion Confirmation")
            print("=" * 70)
            print()
            print("即将删除以下模型 / About to delete the following model:")
            print(f"  模型名称 / Model Name: {selected_model.model_name} (v{selected_model.version})")
            print(f"  模型ID / Model ID: {selected_model.model_id}")
            print(f"  训练日期 / Training Date: {selected_model.training_date}")
            print()
            print("⚠️  警告 / Warning:")
            print("  • 删除操作不可恢复 / Deletion cannot be undone")
            print("  • 模型文件和元数据将被永久删除 / Model files and metadata will be permanently deleted")
            print()
            
            if not self.prompt.confirm("确认删除？ / Confirm deletion?", default=False):
                print("❌ 删除已取消 / Deletion cancelled")
                return
            
            # 再次确认 / Confirm again
            if not self.prompt.confirm(
                "请再次确认删除操作 / Please confirm deletion again",
                default=False
            ):
                print("❌ 删除已取消 / Deletion cancelled")
                return
            
            # 5. 执行删除 / Execute deletion
            print("\n⏳ 正在删除模型... / Deleting model...")
            model_registry.delete_model(selected_model.model_id)
            
            print("\n" + "=" * 70)
            print("✅ 模型删除成功！ / Model Deleted Successfully!")
            print("=" * 70)
            print()
            print(f"已删除模型 / Deleted Model:")
            print(f"  {selected_model.model_name} (v{selected_model.version})")
            print(f"  模型ID / Model ID: {selected_model.model_id}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  操作已中断 / Operation interrupted")
        except Exception as e:
            print(f"\n❌ 删除模型失败 / Failed to delete model: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回 / Press Enter to return...")
    
    def _handle_guided_workflow(self) -> None:
        """
        Handle guided workflow menu.
        处理引导式工作流程菜单。
        
        Validates: Requirements 22.1, 22.2, 22.3, 22.5
        """
        try:
            print("\n" + "=" * 70)
            print("🎯 引导式工作流程 / Guided Workflow")
            print("=" * 70)
            print()
            
            # 显示引导式工作流程介绍 / Display guided workflow introduction
            print("欢迎使用引导式工作流程！")
            print("Welcome to the Guided Workflow!")
            print()
            print("本系统将引导您完成以下10个步骤：")
            print("This system will guide you through the following 10 steps:")
            print()
            print("  1. 市场和资产选择 / Market and Asset Selection")
            print("  2. 智能推荐 / Intelligent Recommendation")
            print("  3. 目标设定 / Target Setting")
            print("  4. 策略优化 / Strategy Optimization")
            print("  5. 模型训练 / Model Training")
            print("  6. 历史回测 / Historical Backtest")
            print("  7. 模拟交易 / Simulation Trading")
            print("  8. 实盘交易设置 / Live Trading Setup")
            print("  9. 实盘交易执行 / Live Trading Execution")
            print("  10. 报告配置 / Reporting Configuration")
            print()
            print("特点 / Features:")
            print("  ✓ 无需编程知识 / No programming knowledge required")
            print("  ✓ 进度自动保存 / Progress automatically saved")
            print("  ✓ 可随时暂停和继续 / Can pause and resume anytime")
            print("  ✓ 支持返回修改 / Support go back to modify")
            print("  ✓ 中英双语界面 / Bilingual interface")
            print()
            print("=" * 70)
            
            # 询问是否开始 / Ask if start
            if not self.prompt.confirm(
                "\n是否开始引导式工作流程？ / Start guided workflow?",
                default=True
            ):
                print("\n已取消 / Cancelled")
                return
            
            # 导入并启动引导式工作流程 / Import and start guided workflow
            from .guided_workflow import GuidedWorkflow
            
            # 创建工作流实例 / Create workflow instance
            workflow = GuidedWorkflow(state_dir="./workflow_states")
            
            # 启动工作流 / Start workflow
            print("\n" + "=" * 70)
            print("🚀 启动引导式工作流程 / Starting Guided Workflow")
            print("=" * 70)
            print()
            
            workflow.start(resume=True)
            
            # 工作流完成后返回主菜单 / Return to main menu after workflow completion
            print("\n" + "=" * 70)
            print("✅ 引导式工作流程已完成或暂停")
            print("✅ Guided workflow completed or paused")
            print("=" * 70)
            print()
            print("您可以：")
            print("You can:")
            print("  • 再次选择选项 0 继续未完成的工作流程")
            print("    Select option 0 again to continue incomplete workflow")
            print("  • 使用其他菜单选项进行单独操作")
            print("    Use other menu options for individual operations")
            print("  • 查看 workflow_states/ 目录中的配置总结")
            print("    View configuration summary in workflow_states/ directory")
            print()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  引导式工作流程已中断")
            print("⚠️  Guided workflow interrupted")
            print("\n进度已保存，下次可以继续")
            print("Progress saved, you can continue next time")
        except Exception as e:
            print(f"\n❌ 引导式工作流程执行失败 / Guided workflow execution failed")
            print(f"错误信息 / Error: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            input("\n按回车键返回主菜单 / Press Enter to return to main menu...")
    
    def _export_model_info(self, model_info, metadata: Dict[str, Any]) -> None:
        """
        Export model information to a file.
        导出模型信息到文件。
        
        Args:
            model_info: ModelInfo object / 模型信息对象
            metadata: Model metadata dictionary / 模型元数据字典
        """
        try:
            import json
            from pathlib import Path
            from datetime import datetime
            
            # 创建输出目录 / Create output directory
            output_dir = Path("outputs/model_info")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成文件名 / Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"model_{model_info.model_id}_{timestamp}.json"
            filepath = output_dir / filename
            
            # 准备导出数据 / Prepare export data
            export_data = {
                "model_id": model_info.model_id,
                "model_name": model_info.model_name,
                "version": model_info.version,
                "model_type": model_info.model_type,
                "training_date": model_info.training_date,
                "status": model_info.status,
                "performance_metrics": model_info.performance_metrics,
                "model_path": model_info.model_path,
                "metadata_path": model_info.metadata_path,
                "metadata": metadata,
                "exported_at": datetime.now().isoformat()
            }
            
            # 写入文件 / Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ 模型信息已导出 / Model information exported")
            print(f"   文件路径 / File path: {filepath}")
            
        except Exception as e:
            print(f"\n❌ 导出失败 / Export failed: {str(e)}")


    def _handle_system_management(self) -> None:
        """
        Handle system management menu.
        处理系统管理菜单。
        """
        while True:
            print("\n" + "="*60)
            print("系统管理 / System Management")
            print("="*60)
            
            print("\n1. 查看内存状态 / View Memory Status")
            print("2. 清理缓存 / Clear Cache")
            print("3. 强制垃圾回收 / Force Garbage Collection")
            print("4. 查看缓存统计 / View Cache Statistics")
            print("5. 内存监控设置 / Memory Monitor Settings")
            print("0. 返回主菜单 / Back to Main Menu")
            
            choice = self.prompt.ask_text(
                "\n请选择操作 / Please select an option",
                default="0"
            )
            
            if choice == "0":
                break
            elif choice == "1":
                self._show_memory_status()
            elif choice == "2":
                self._clear_cache()
            elif choice == "3":
                self._force_gc()
            elif choice == "4":
                self._show_cache_stats()
            elif choice == "5":
                self._memory_monitor_settings()
            else:
                print("\n❌ 无效选择 / Invalid choice")
    
    def _show_memory_status(self) -> None:
        """显示内存状态 / Show memory status"""
        try:
            from ..utils.memory_monitor import get_memory_monitor
            
            monitor = get_memory_monitor()
            stats = monitor.get_memory_stats()
            
            print("\n" + "="*60)
            print("内存状态 / Memory Status")
            print("="*60)
            print(f"\n物理内存使用 / Physical Memory (RSS): {stats.rss_mb:.2f} MB")
            print(f"虚拟内存使用 / Virtual Memory (VMS): {stats.vms_mb:.2f} MB")
            print(f"内存占比 / Memory Percentage: {stats.percent:.2f}%")
            print(f"系统可用内存 / Available Memory: {stats.available_mb:.2f} MB")
            
            # 检查内存状态
            is_ok, message = monitor.check_memory()
            if is_ok:
                print(f"\n✅ {message}")
            else:
                print(f"\n⚠️ {message}")
            
        except Exception as e:
            print(f"\n❌ 获取内存状态失败 / Failed to get memory status: {str(e)}")
        
        input("\n按Enter键继续... / Press Enter to continue...")
    
    def _clear_cache(self) -> None:
        """清理缓存 / Clear cache"""
        try:
            from ..utils.cache_manager import get_cache_manager
            
            confirm = self.prompt.confirm(
                "确定要清理所有缓存吗？这将删除所有缓存数据。\n"
                "Are you sure you want to clear all cache? This will delete all cached data.",
                default=False
            )
            
            if not confirm:
                print("\n已取消 / Cancelled")
                return
            
            print("\n正在清理缓存... / Clearing cache...")
            cache_manager = get_cache_manager()
            count = cache_manager.clear()
            
            print(f"\n✅ 已清理 {count} 个缓存条目 / Cleared {count} cache entries")
            
        except Exception as e:
            print(f"\n❌ 清理缓存失败 / Failed to clear cache: {str(e)}")
        
        input("\n按Enter键继续... / Press Enter to continue...")
    
    def _force_gc(self) -> None:
        """强制垃圾回收 / Force garbage collection"""
        try:
            import gc
            from ..utils.memory_monitor import get_memory_monitor
            
            monitor = get_memory_monitor()
            before_stats = monitor.get_memory_stats()
            
            print("\n正在执行垃圾回收... / Running garbage collection...")
            collected = gc.collect()
            
            after_stats = monitor.get_memory_stats()
            freed_mb = before_stats.rss_mb - after_stats.rss_mb
            
            print(f"\n✅ 垃圾回收完成 / Garbage collection completed")
            print(f"回收对象数 / Objects collected: {collected}")
            print(f"释放内存 / Memory freed: {freed_mb:.2f} MB")
            print(f"当前内存使用 / Current memory usage: {after_stats.rss_mb:.2f} MB")
            
        except Exception as e:
            print(f"\n❌ 垃圾回收失败 / Failed to run GC: {str(e)}")
        
        input("\n按Enter键继续... / Press Enter to continue...")
    
    def _show_cache_stats(self) -> None:
        """显示缓存统计 / Show cache statistics"""
        try:
            from ..utils.cache_manager import get_cache_manager
            
            cache_manager = get_cache_manager()
            stats = cache_manager.get_cache_stats()
            
            print("\n" + "="*60)
            print("缓存统计 / Cache Statistics")
            print("="*60)
            print(f"\n内存缓存数量 / Memory cache count: {stats['memory_cache_count']}")
            print(f"磁盘缓存数量 / Disk cache count: {stats['disk_cache_count']}")
            print(f"缓存总大小 / Total cache size: {stats['total_cache_size_mb']:.2f} MB")
            print(f"缓存目录 / Cache directory: {stats['cache_directory']}")
            
        except Exception as e:
            print(f"\n❌ 获取缓存统计失败 / Failed to get cache stats: {str(e)}")
        
        input("\n按Enter键继续... / Press Enter to continue...")
    
    def _memory_monitor_settings(self) -> None:
        """内存监控设置 / Memory monitor settings"""
        try:
            from ..utils.memory_monitor import get_memory_monitor
            
            monitor = get_memory_monitor()
            
            print("\n" + "="*60)
            print("内存监控设置 / Memory Monitor Settings")
            print("="*60)
            
            print("\n当前设置 / Current Settings:")
            print(f"最大内存限制 / Max memory: {monitor._max_memory_mb} MB")
            print(f"警告阈值 / Warning threshold: {monitor._warning_threshold * 100}%")
            print(f"紧急阈值 / Critical threshold: {monitor._critical_threshold * 100}%")
            print(f"检查间隔 / Check interval: {monitor._check_interval} 秒 / seconds")
            print(f"自动清理 / Auto cleanup: {'启用 / Enabled' if monitor._auto_cleanup else '禁用 / Disabled'}")
            
            print("\n操作 / Actions:")
            print("1. 立即执行清理 / Run cleanup now")
            print("2. 立即执行紧急清理 / Run emergency cleanup now")
            print("0. 返回 / Back")
            
            choice = self.prompt.ask_text(
                "\n请选择操作 / Please select an option",
                default="0"
            )
            
            if choice == "1":
                print("\n正在执行清理... / Running cleanup...")
                monitor.force_cleanup()
                print("✅ 清理完成 / Cleanup completed")
            elif choice == "2":
                confirm = self.prompt.confirm(
                    "紧急清理将清除所有缓存并执行多次垃圾回收，确定继续吗？\n"
                    "Emergency cleanup will clear all cache and run multiple GC cycles. Continue?",
                    default=False
                )
                if confirm:
                    print("\n正在执行紧急清理... / Running emergency cleanup...")
                    monitor.force_emergency_cleanup()
                    print("✅ 紧急清理完成 / Emergency cleanup completed")
            
        except Exception as e:
            print(f"\n❌ 内存监控设置失败 / Failed to access memory monitor settings: {str(e)}")
        
        input("\n按Enter键继续... / Press Enter to continue...")


def main():
    """
    Main entry point for the CLI application.
    CLI应用程序的主入口点。
    """
    # 导入内存监控器
    # Import memory monitor
    try:
        from ..utils.memory_monitor import get_memory_monitor
        from ..infrastructure.logger_system import get_logger
        
        logger = get_logger(__name__)
        
        # 启动内存监控
        # Start memory monitoring
        logger.info("启动内存监控... / Starting memory monitoring...")
        monitor = get_memory_monitor(
            max_memory_mb=4096,  # 4GB限制 / 4GB limit
            warning_threshold=0.8,  # 80%警告 / 80% warning
            critical_threshold=0.9,  # 90%紧急 / 90% critical
            check_interval=60,  # 每60秒检查 / Check every 60 seconds
            auto_cleanup=True  # 自动清理 / Auto cleanup
        )
        monitor.start_monitoring()
        logger.info("内存监控已启动 / Memory monitoring started")
        
        # 运行主程序
        # Run main program
        try:
            cli = MainCLI()
            cli.run()
        finally:
            # 停止内存监控
            # Stop memory monitoring
            logger.info("停止内存监控... / Stopping memory monitoring...")
            monitor.stop_monitoring()
            logger.info("内存监控已停止 / Memory monitoring stopped")
            
    except ImportError as e:
        # 如果内存监控模块不可用，继续运行但不启用监控
        # If memory monitor module is not available, continue without monitoring
        print(f"⚠️ 内存监控模块不可用，继续运行... / Memory monitor not available, continuing...")
        print(f"   错误 / Error: {str(e)}")
        cli = MainCLI()
        cli.run()
    except Exception as e:
        print(f"❌ 启动失败 / Startup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
