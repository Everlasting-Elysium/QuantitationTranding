#!/usr/bin/env python3
"""
下载qlib数据脚本 / Download qlib data script
"""
import sys
from pathlib import Path

def download_data():
    """下载qlib中国A股数据"""
    try:
        # 方法1: 使用qlib scripts
        import subprocess
        
        target_dir = Path.home() / ".qlib" / "qlib_data" / "cn_data"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"正在下载数据到 / Downloading data to: {target_dir}")
        print("这可能需要几分钟... / This may take a few minutes...")
        
        # 使用qlib提供的脚本下载
        cmd = [
            sys.executable,
            "-m",
            "qlib.run.get_data",
            "qlib_data",
            "--target_dir",
            str(target_dir),
            "--region",
            "cn"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 数据下载成功 / Data downloaded successfully")
            return True
        else:
            print(f"✗ 下载失败 / Download failed: {result.stderr}")
            
            # 尝试备用方法
            print("\n尝试备用下载方法 / Trying alternative download method...")
            print("请手动运行以下命令 / Please manually run:")
            print(f"  python scripts/get_data.py qlib_data --target_dir {target_dir} --region cn")
            return False
            
    except Exception as e:
        print(f"✗ 错误 / Error: {e}")
        return False

if __name__ == "__main__":
    download_data()
