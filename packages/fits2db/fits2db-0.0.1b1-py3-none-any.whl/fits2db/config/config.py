"""
This module contains the configuration validation for the FITS to database application.
"""

from .config_model import ConfigFileValidator, ApplicationConfig, ConfigType

from typing import Union
import yaml
import os
from jinja2 import Environment, FileSystemLoader


def get_configs(path: Union[str, os.PathLike]) -> ConfigType:
    """Loads config file from given path

    Args:
        path (Union[str, os.PathLike]): Path to config yaml file

    Returns:
        ConfigType: Data from config file loaded and validated
    """
    config_validator = ConfigFileValidator(path=path)
    with open(config_validator.path, "r", encoding="utf-8") as file:
        try:
            config_data = yaml.safe_load(file)
        except yaml.YAMLError as err:
            print("YAML loading error:", err)
            return {}

    try:
        data = ApplicationConfig(**config_data).model_dump()
    except (TypeError, ValueError) as err:
        print("Config file validation error:", err)
        return {}
    
    return data


def render_template(template_name: str, context: dict) -> str:
    """Renders a given template under the relative template directory

    Args:
        template_name (str): Name of template
        context (dict): Dict with template conext

    Returns:
        str: Rendered template as str
    """
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)
    return template.render(context)


def generate_config():
    """Generate a example config file."""
    config_content = render_template("config.yaml.j2", {"db_type": "mysql"})
    with open(os.path.join("config.yaml"), "w", encoding="utf-8") as f:
        f.write(config_content)
