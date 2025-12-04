"""
Unit tests for project structure validation
"""
import os
from pathlib import Path

import pytest


class TestProjectStructure:
    """Test that the project structure is set up correctly"""
    
    @pytest.fixture
    def project_root(self) -> Path:
        """Get the project root directory"""
        return Path(__file__).parent.parent.parent
    
    def test_src_directories_exist(self, project_root: Path):
        """Test that all required src directories exist"""
        required_dirs = [
            "src",
            "src/cli",
            "src/core",
            "src/application",
            "src/infrastructure",
            "src/models",
            "src/templates",
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Directory {dir_path} does not exist"
            assert full_path.is_dir(), f"{dir_path} is not a directory"
    
    def test_test_directories_exist(self, project_root: Path):
        """Test that all required test directories exist"""
        required_dirs = [
            "tests",
            "tests/unit",
            "tests/property",
            "tests/integration",
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Directory {dir_path} does not exist"
            assert full_path.is_dir(), f"{dir_path} is not a directory"
    
    def test_config_directory_exists(self, project_root: Path):
        """Test that config directory exists"""
        config_dir = project_root / "config"
        assert config_dir.exists(), "Config directory does not exist"
        assert config_dir.is_dir(), "Config is not a directory"
    
    def test_docs_directory_exists(self, project_root: Path):
        """Test that docs directory exists"""
        docs_dir = project_root / "docs"
        assert docs_dir.exists(), "Docs directory does not exist"
        assert docs_dir.is_dir(), "Docs is not a directory"
    
    def test_logs_directory_exists(self, project_root: Path):
        """Test that logs directory exists"""
        logs_dir = project_root / "logs"
        assert logs_dir.exists(), "Logs directory does not exist"
        assert logs_dir.is_dir(), "Logs is not a directory"
    
    def test_python_packages_have_init(self, project_root: Path):
        """Test that all Python packages have __init__.py files"""
        package_dirs = [
            "src",
            "src/cli",
            "src/core",
            "src/application",
            "src/infrastructure",
            "src/models",
            "src/templates",
            "tests",
            "tests/unit",
            "tests/property",
            "tests/integration",
        ]
        
        for dir_path in package_dirs:
            init_file = project_root / dir_path / "__init__.py"
            assert init_file.exists(), f"__init__.py missing in {dir_path}"
            assert init_file.is_file(), f"__init__.py in {dir_path} is not a file"
    
    def test_requirements_file_exists(self, project_root: Path):
        """Test that requirements.txt exists"""
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt does not exist"
        assert requirements_file.is_file(), "requirements.txt is not a file"
    
    def test_setup_file_exists(self, project_root: Path):
        """Test that setup.py exists"""
        setup_file = project_root / "setup.py"
        assert setup_file.exists(), "setup.py does not exist"
        assert setup_file.is_file(), "setup.py is not a file"
    
    def test_pytest_config_exists(self, project_root: Path):
        """Test that pytest.ini exists"""
        pytest_config = project_root / "pytest.ini"
        assert pytest_config.exists(), "pytest.ini does not exist"
        assert pytest_config.is_file(), "pytest.ini is not a file"
    
    def test_default_config_exists(self, project_root: Path):
        """Test that default configuration file exists"""
        config_file = project_root / "config" / "default_config.yaml"
        assert config_file.exists(), "default_config.yaml does not exist"
        assert config_file.is_file(), "default_config.yaml is not a file"
    
    def test_gitignore_exists(self, project_root: Path):
        """Test that .gitignore exists"""
        gitignore = project_root / ".gitignore"
        assert gitignore.exists(), ".gitignore does not exist"
        assert gitignore.is_file(), ".gitignore is not a file"
