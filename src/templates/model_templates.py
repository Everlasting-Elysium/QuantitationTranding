"""
Model template management for the qlib trading system.

This module provides functionality to load and manage pre-configured
model templates from YAML configuration files.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from src.models.data_models import ModelTemplate


class ModelTemplateManager:
    """
    Manager for loading and accessing model templates.
    
    This class handles loading model templates from YAML configuration
    files and provides methods to retrieve templates by name.
    """
    
    def __init__(self, template_config_path: Optional[str] = None):
        """
        Initialize the template manager.
        
        Args:
            template_config_path: Path to the template configuration YAML file.
                                 If None, uses default path.
        """
        if template_config_path is None:
            # Default to config/model_templates.yaml
            template_config_path = Path(__file__).parent.parent.parent / "config" / "model_templates.yaml"
        
        self.template_config_path = Path(template_config_path)
        self._templates: Dict[str, ModelTemplate] = {}
        self._load_templates()
    
    def _load_templates(self) -> None:
        """
        Load templates from the YAML configuration file.
        
        Raises:
            FileNotFoundError: If the template configuration file doesn't exist
            ValueError: If the configuration format is invalid
        """
        if not self.template_config_path.exists():
            raise FileNotFoundError(
                f"Template configuration file not found: {self.template_config_path}"
            )
        
        with open(self.template_config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not config or 'templates' not in config:
            raise ValueError("Invalid template configuration: missing 'templates' key")
        
        for template_data in config['templates']:
            try:
                template = ModelTemplate(
                    name=template_data['name'],
                    model_type=template_data['model_type'],
                    description=template_data['description'],
                    use_case=template_data['use_case'],
                    default_params=template_data['default_params'],
                    expected_performance=template_data.get('expected_performance', {})
                )
                self._templates[template.name] = template
            except KeyError as e:
                raise ValueError(f"Invalid template configuration: missing key {e}")
    
    def get_template(self, name: str) -> ModelTemplate:
        """
        Get a template by name.
        
        Args:
            name: Name of the template to retrieve
            
        Returns:
            ModelTemplate object
            
        Raises:
            KeyError: If template with given name doesn't exist
        """
        if name not in self._templates:
            available = ", ".join(self._templates.keys())
            raise KeyError(
                f"Template '{name}' not found. Available templates: {available}"
            )
        return self._templates[name]
    
    def list_templates(self) -> List[ModelTemplate]:
        """
        Get a list of all available templates.
        
        Returns:
            List of ModelTemplate objects
        """
        return list(self._templates.values())
    
    def list_template_names(self) -> List[str]:
        """
        Get a list of all template names.
        
        Returns:
            List of template names
        """
        return list(self._templates.keys())
    
    def has_template(self, name: str) -> bool:
        """
        Check if a template exists.
        
        Args:
            name: Name of the template to check
            
        Returns:
            True if template exists, False otherwise
        """
        return name in self._templates
    
    def get_template_info(self, name: str) -> Dict[str, str]:
        """
        Get basic information about a template.
        
        Args:
            name: Name of the template
            
        Returns:
            Dictionary with template information
            
        Raises:
            KeyError: If template doesn't exist
        """
        template = self.get_template(name)
        return {
            'name': template.name,
            'model_type': template.model_type,
            'description': template.description,
            'use_case': template.use_case
        }
