#!/usr/bin/env python3
"""
一键初始化脚本 / One-Click Initialization Script

This script provides one-click initialization for the quantitative trading system.
本脚本为量化交易系统提供一键初始化功能。

Features / 功能:
- Dependency detection / 依赖检测
- Automatic data download / 自动数据下载
- Example validation / 示例验证
- Friendly progress indicators / 友好的进度提示

Validates: Requirements 11.1, 11.2, 11.4
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path
from typing import List, Tuple, Optional
import time


class Colors:
    """终端颜色代码 / Terminal color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SystemInitializer:
    """
    系统初始化器 / System Initializer
    
    Responsibilities / 职责:
    - Check and install dependencies / 检查和安装依赖
    - Download sample data / 下载示例数据
    - Validate system setup / 验证系统设置
    - Run example to verify / 运行示例验证
    
    Validates: Requirements 11.1, 11.2, 11.4
    """
    
    def __init__(self):
        """初始化系统初始化器 / Initialize system initializer"""
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data" / "cn_data"
        self.config_dir = self.project_root / "config"
        self.logs_dir = self.project_root / "logs"
        
        # 必需的依赖包 / Required dependencies
        self.required_packages = [
            ("qlib", "qlib"),
            ("numpy", "numpy"),
            ("pandas", "pandas"),
            ("sklearn", "scikit-learn"),
            ("lightgbm", "lightgbm"),
            ("torch", "torch"),
            ("mlflow", "mlflow"),
            ("matplotlib", "matplotlib"),
            ("seaborn", "seaborn"),
            ("click", "click"),
            ("rich", "rich"),
            ("yaml", "pyyaml"),
            ("pytest", "pytest"),
        ]
    
    def print_header(self, text: str) -> None:
        """
        打印标题 / Print header
        
        Args:
            text: 标题文本 / Header text
        """
        print(f"\n{Colors.HEADER}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")
    
    def print_success(self, text: str) -> None:
        """打印成功消息 / Print success message"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")
    
    def print_error(self, text: str) -> None:
        """打印错误消息 / Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str) -> None:
        """打印警告消息 / Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
    
    def print_info(self, text: str) -> None:
        """打印信息消息 / Print info message"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")
    
    def print_progress(self, current: int, total: int, task: str) -> None:
        """
        打印进度条 / Print progress bar
        
        Args:
            current: 当前进度 / Current progress
            total: 总数 / Total count
            task: 任务描述 / Task description
        """
        percent = int((current / total) * 100)
        bar_length = 40
        filled = int((bar_length * current) / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r{Colors.OKCYAN}[{bar}] {percent}% - {task}{Colors.ENDC}", end='', flush=True)
        if current == total:
            print()  # 完成后换行 / New line when complete
    
    def check_python_version(self) -> bool:
        """
        检查Python版本 / Check Python version
        
        Returns:
            bool: 版本是否满足要求 / Whether version meets requirements
            
        Validates: Requirements 11.1
        """
        self.print_info("检查Python版本 / Checking Python version...")
        
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            self.print_success(f"Python版本: {version.major}.{version.minor}.{version.micro} ✓")
            return True
        else:
            self.print_error(
                f"Python版本不满足要求 / Python version does not meet requirements\n"
                f"  当前版本 / Current: {version.major}.{version.minor}.{version.micro}\n"
                f"  要求版本 / Required: 3.8+"
            )
            return False
    
    def check_dependencies(self) -> Tuple[List[str], List[str]]:
        """
        检查依赖包 / Check dependencies
        
        Returns:
            Tuple[List[str], List[str]]: (已安装的包, 缺失的包) / (installed packages, missing packages)
            
        Validates: Requirements 11.1
        """
        self.print_info("检查依赖包 / Checking dependencies...")
        
        installed = []
        missing = []
        
        total = len(self.required_packages)
        for i, (import_name, package_name) in enumerate(self.required_packages, 1):
            self.print_progress(i, total, f"检查 {package_name}")
            
            try:
                importlib.import_module(import_name)
                installed.append(package_name)
            except ImportError:
                missing.append(package_name)
            
            time.sleep(0.1)  # 短暂延迟以显示进度 / Brief delay to show progress
        
        print()  # 换行 / New line
        
        if installed:
            self.print_success(f"已安装 {len(installed)}/{total} 个依赖包 / {len(installed)}/{total} dependencies installed")
        
        if missing:
            self.print_warning(f"缺失 {len(missing)} 个依赖包 / {len(missing)} dependencies missing:")
            for pkg in missing:
                print(f"  - {pkg}")
        
        return installed, missing
    
    def install_dependencies(self, missing_packages: List[str]) -> bool:
        """
        安装缺失的依赖包 / Install missing dependencies
        
        Args:
            missing_packages: 缺失的包列表 / List of missing packages
            
        Returns:
            bool: 安装是否成功 / Whether installation succeeded
            
        Validates: Requirements 11.1
        """
        if not missing_packages:
            return True
        
        self.print_info(f"准备安装 {len(missing_packages)} 个缺失的依赖包 / Preparing to install {len(missing_packages)} missing packages...")
        
        # 询问用户是否安装 / Ask user for confirmation
        response = input(f"\n是否自动安装缺失的依赖包？(y/n) / Install missing packages automatically? (y/n): ").strip().lower()
        
        if response != 'y':
            self.print_warning("跳过依赖安装 / Skipping dependency installation")
            self.print_info("您可以手动安装依赖 / You can install dependencies manually:")
            print(f"  pip install -r requirements.txt")
            return False
        
        try:
            self.print_info("正在安装依赖包，请稍候... / Installing dependencies, please wait...")
            
            # 使用requirements.txt安装 / Install using requirements.txt
            requirements_file = self.project_root / "requirements.txt"
            if requirements_file.exists():
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.print_success("依赖包安装成功 / Dependencies installed successfully")
                    return True
                else:
                    self.print_error(f"依赖包安装失败 / Dependency installation failed:\n{result.stderr}")
                    return False
            else:
                self.print_error(f"未找到requirements.txt文件 / requirements.txt not found")
                return False
                
        except Exception as e:
            self.print_error(f"安装依赖包时发生错误 / Error during installation: {str(e)}")
            return False
    
    def create_directories(self) -> bool:
        """
        创建必要的目录 / Create necessary directories
        
        Returns:
            bool: 创建是否成功 / Whether creation succeeded
            
        Validates: Requirements 11.2
        """
        self.print_info("创建必要的目录 / Creating necessary directories...")
        
        directories = [
            self.data_dir,
            self.config_dir,
            self.logs_dir,
            self.project_root / "outputs" / "backtests",
            self.project_root / "outputs" / "reports",
            self.project_root / "outputs" / "signals",
            self.project_root / "model_registry",
            self.project_root / "examples" / "mlruns",
        ]
        
        try:
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                self.print_success(f"创建目录 / Created: {directory.relative_to(self.project_root)}")
            
            return True
        except Exception as e:
            self.print_error(f"创建目录失败 / Failed to create directories: {str(e)}")
            return False
    
    def check_data_exists(self) -> bool:
        """
        检查数据是否存在 / Check if data exists
        
        Returns:
            bool: 数据是否存在 / Whether data exists
        """
        # 检查qlib数据目录 / Check qlib data directory
        qlib_data_dir = Path.home() / ".qlib" / "qlib_data" / "cn_data"
        
        if qlib_data_dir.exists() and any(qlib_data_dir.iterdir()):
            self.print_success(f"发现已有数据 / Found existing data: {qlib_data_dir}")
            return True
        
        # 检查项目数据目录 / Check project data directory
        if self.data_dir.exists() and any(self.data_dir.iterdir()):
            self.print_success(f"发现已有数据 / Found existing data: {self.data_dir}")
            return True
        
        return False
    
    def download_sample_data(self) -> bool:
        """
        下载示例数据 / Download sample data
        
        Returns:
            bool: 下载是否成功 / Whether download succeeded
            
        Validates: Requirements 11.2
        """
        self.print_info("准备下载示例数据 / Preparing to download sample data...")
        
        # 检查数据是否已存在 / Check if data already exists
        if self.check_data_exists():
            response = input("\n数据已存在，是否重新下载？(y/n) / Data exists, re-download? (y/n): ").strip().lower()
            if response != 'y':
                self.print_info("跳过数据下载 / Skipping data download")
                return True
        
        try:
            self.print_info("正在下载中国A股示例数据，这可能需要几分钟... / Downloading China A-share sample data, this may take a few minutes...")
            
            # 使用qlib的数据下载工具 / Use qlib's data download tool
            target_dir = Path.home() / ".qlib" / "qlib_data" / "cn_data"
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # 方法1: 使用qlib命令行工具 / Method 1: Use qlib CLI tool
            self.print_info("方法1: 使用qlib命令行工具下载 / Method 1: Download using qlib CLI...")
            
            result = subprocess.run(
                [
                    sys.executable, "-m", "qlib.run.get_data",
                    "qlib_data",
                    "--target_dir", str(target_dir),
                    "--region", "cn"
                ],
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时 / 10 minutes timeout
            )
            
            if result.returncode == 0:
                self.print_success("示例数据下载成功 / Sample data downloaded successfully")
                self.print_info(f"数据位置 / Data location: {target_dir}")
                return True
            else:
                self.print_warning("方法1失败，尝试方法2 / Method 1 failed, trying method 2...")
                
                # 方法2: 使用scripts/get_data.py / Method 2: Use scripts/get_data.py
                self.print_info("方法2: 使用get_data脚本下载 / Method 2: Download using get_data script...")
                
                get_data_script = self.project_root / "scripts" / "get_data.py"
                if get_data_script.exists():
                    result = subprocess.run(
                        [
                            sys.executable, str(get_data_script),
                            "qlib_data",
                            "--target_dir", str(target_dir),
                            "--region", "cn"
                        ],
                        capture_output=True,
                        text=True,
                        timeout=600
                    )
                    
                    if result.returncode == 0:
                        self.print_success("示例数据下载成功 / Sample data downloaded successfully")
                        return True
                
                # 如果都失败，提供手动下载指引 / If both fail, provide manual download instructions
                self.print_error("自动下载失败 / Automatic download failed")
                self.print_info("请手动下载数据 / Please download data manually:")
                print(f"\n  方法1 / Method 1:")
                print(f"    python -m qlib.run.get_data qlib_data --target_dir {target_dir} --region cn")
                print(f"\n  方法2 / Method 2:")
                print(f"    python scripts/get_data.py qlib_data --target_dir {target_dir} --region cn")
                print(f"\n  方法3 / Method 3:")
                print(f"    访问 / Visit: https://github.com/microsoft/qlib#data-preparation")
                
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("数据下载超时 / Data download timeout")
            self.print_info("请稍后重试或手动下载 / Please retry later or download manually")
            return False
        except Exception as e:
            self.print_error(f"下载数据时发生错误 / Error during download: {str(e)}")
            return False
    
    def run_example_validation(self) -> bool:
        """
        运行示例验证系统 / Run example to validate system
        
        Returns:
            bool: 验证是否成功 / Whether validation succeeded
            
        Validates: Requirements 11.4
        """
        self.print_info("运行示例验证系统 / Running example to validate system...")
        
        try:
            # 创建简单的验证脚本 / Create simple validation script
            validation_code = """
import sys
sys.path.insert(0, 'src')

try:
    # 测试导入核心模块 / Test importing core modules
    from infrastructure.qlib_wrapper import QlibWrapper
    from core.config_manager import ConfigManager
    from core.data_manager import DataManager
    
    print("✓ 核心模块导入成功 / Core modules imported successfully")
    
    # 测试qlib初始化 / Test qlib initialization
    from pathlib import Path
    data_path = Path.home() / ".qlib" / "qlib_data" / "cn_data"
    
    if data_path.exists():
        qlib_wrapper = QlibWrapper()
        qlib_wrapper.init(provider_uri=str(data_path), region="cn")
        print("✓ Qlib初始化成功 / Qlib initialized successfully")
        
        # 测试数据访问 / Test data access
        data_info = qlib_wrapper.get_data_info()
        print(f"✓ 数据访问成功 / Data access successful")
        print(f"  数据范围 / Data range: {data_info['data_start']} to {data_info['data_end']}")
        print(f"  交易日数 / Trading days: {data_info['trading_days']}")
    else:
        print("⚠ 数据目录不存在，跳过数据测试 / Data directory not found, skipping data test")
    
    print("\\n✓ 系统验证通过！ / System validation passed!")
    sys.exit(0)
    
except Exception as e:
    print(f"✗ 系统验证失败 / System validation failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
            
            # 写入临时验证脚本 / Write temporary validation script
            validation_script = self.project_root / "temp_validation.py"
            validation_script.write_text(validation_code)
            
            try:
                # 运行验证脚本 / Run validation script
                result = subprocess.run(
                    [sys.executable, str(validation_script)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.project_root)
                )
                
                # 显示输出 / Display output
                if result.stdout:
                    print(result.stdout)
                
                if result.returncode == 0:
                    self.print_success("示例验证通过 / Example validation passed")
                    return True
                else:
                    self.print_error("示例验证失败 / Example validation failed")
                    if result.stderr:
                        print(result.stderr)
                    return False
                    
            finally:
                # 清理临时文件 / Clean up temporary file
                if validation_script.exists():
                    validation_script.unlink()
                    
        except subprocess.TimeoutExpired:
            self.print_error("验证超时 / Validation timeout")
            return False
        except Exception as e:
            self.print_error(f"运行验证时发生错误 / Error during validation: {str(e)}")
            return False
    
    def generate_summary(self, success: bool) -> None:
        """
        生成初始化总结 / Generate initialization summary
        
        Args:
            success: 初始化是否成功 / Whether initialization succeeded
        """
        self.print_header("初始化总结 / Initialization Summary")
        
        if success:
            self.print_success("系统初始化完成！ / System initialization completed!")
            print()
            print("您现在可以开始使用系统了 / You can now start using the system:")
            print()
            print(f"  1. 启动主界面 / Start main interface:")
            print(f"     {Colors.OKCYAN}python main.py{Colors.ENDC}")
            print()
            print(f"  2. 查看文档 / View documentation:")
            print(f"     {Colors.OKCYAN}docs/README.md{Colors.ENDC}")
            print()
            print(f"  3. 运行示例 / Run examples:")
            print(f"     {Colors.OKCYAN}python examples/demo_training_manager.py{Colors.ENDC}")
            print()
            print(f"  4. 查看配置 / View configuration:")
            print(f"     {Colors.OKCYAN}config/default_config.yaml{Colors.ENDC}")
            print()
        else:
            self.print_error("系统初始化未完全成功 / System initialization not fully successful")
            print()
            print("请检查上述错误信息并手动完成以下步骤 / Please check errors above and complete these steps manually:")
            print()
            print(f"  1. 安装依赖 / Install dependencies:")
            print(f"     {Colors.WARNING}pip install -r requirements.txt{Colors.ENDC}")
            print()
            print(f"  2. 下载数据 / Download data:")
            print(f"     {Colors.WARNING}python -m qlib.run.get_data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn{Colors.ENDC}")
            print()
            print(f"  3. 重新运行初始化 / Re-run initialization:")
            print(f"     {Colors.WARNING}python init_system.py{Colors.ENDC}")
            print()
        
        print(f"{Colors.HEADER}{'=' * 70}{Colors.ENDC}\n")
    
    def run(self) -> bool:
        """
        运行完整的初始化流程 / Run complete initialization process
        
        Returns:
            bool: 初始化是否成功 / Whether initialization succeeded
            
        Validates: Requirements 11.1, 11.2, 11.4
        """
        self.print_header("🚀 量化交易系统 - 一键初始化 / Quantitative Trading System - One-Click Initialization")
        
        print("欢迎使用量化交易系统！ / Welcome to Quantitative Trading System!")
        print("本脚本将帮助您完成系统初始化。 / This script will help you initialize the system.")
        print()
        
        # 步骤1: 检查Python版本 / Step 1: Check Python version
        self.print_header("步骤 1/5: 检查Python版本 / Step 1/5: Check Python Version")
        if not self.check_python_version():
            self.generate_summary(False)
            return False
        
        # 步骤2: 检查依赖 / Step 2: Check dependencies
        self.print_header("步骤 2/5: 检查依赖包 / Step 2/5: Check Dependencies")
        installed, missing = self.check_dependencies()
        
        if missing:
            if not self.install_dependencies(missing):
                self.print_warning("部分依赖未安装，但可以继续 / Some dependencies not installed, but can continue")
        
        # 步骤3: 创建目录 / Step 3: Create directories
        self.print_header("步骤 3/5: 创建必要目录 / Step 3/5: Create Directories")
        if not self.create_directories():
            self.generate_summary(False)
            return False
        
        # 步骤4: 下载数据 / Step 4: Download data
        self.print_header("步骤 4/5: 下载示例数据 / Step 4/5: Download Sample Data")
        data_success = self.download_sample_data()
        
        if not data_success:
            self.print_warning("数据下载未成功，但可以稍后手动下载 / Data download not successful, but can download manually later")
        
        # 步骤5: 运行验证 / Step 5: Run validation
        self.print_header("步骤 5/5: 验证系统设置 / Step 5/5: Validate System Setup")
        validation_success = self.run_example_validation()
        
        # 生成总结 / Generate summary
        overall_success = validation_success
        self.generate_summary(overall_success)
        
        return overall_success


def main():
    """主函数 / Main function"""
    try:
        initializer = SystemInitializer()
        success = initializer.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠ 初始化已中断 / Initialization interrupted{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ 初始化失败 / Initialization failed: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
