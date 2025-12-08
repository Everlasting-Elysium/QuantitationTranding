#!/usr/bin/env python
"""
Verification script to check project setup
验证项目设置的脚本
"""
import os
from pathlib import Path


def print_tree(directory: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
    """Print directory tree structure"""
    if current_depth >= max_depth:
        return
    
    try:
        items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['__pycache__', 'htmlcov']:
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension, max_depth, current_depth + 1)


def verify_setup():
    """Verify that the project is set up correctly"""
    project_root = Path(__file__).parent
    
    print("=" * 70)
    print("Qlib Trading System - Project Structure Verification")
    print("量化交易系统 - 项目结构验证")
    print("=" * 70)
    print()
    
    # Check critical directories
    critical_dirs = [
        "src/cli",
        "src/core",
        "src/application",
        "src/infrastructure",
        "src/models",
        "src/templates",
        "tests/unit",
        "tests/property",
        "tests/integration",
        "config",
        "docs",
        "logs",
    ]
    
    print("✓ Checking critical directories...")
    all_exist = True
    for dir_path in critical_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - MISSING!")
            all_exist = False
    
    print()
    
    # Check critical files
    critical_files = [
        "requirements.txt",
        "setup.py",
        "pytest.ini",
        "config/default_config.yaml",
        ".gitignore",
    ]
    
    print("✓ Checking critical files...")
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - MISSING!")
            all_exist = False
    
    print()
    
    # Print project tree
    print("✓ Project structure:")
    print()
    print(project_root.name + "/")
    print_tree(project_root, max_depth=2)
    
    print()
    print("=" * 70)
    
    if all_exist:
        print("✓ All checks passed! Project structure is set up correctly.")
        print("✓ 所有检查通过！项目结构设置正确。")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        print("✗ 部分检查失败。请查看上面的输出。")
        return 1


if __name__ == "__main__":
    exit(verify_setup())
