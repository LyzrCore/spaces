"""Configuration module for the Gradio Spaces ecosystem."""

from config.app_registry import APPS_REGISTRY, get_app_info, get_all_apps, get_app_url
from config.settings import ENVIRONMENT, LOCAL_PORTS, is_dev_mode, is_prod_mode

__all__ = [
    "APPS_REGISTRY",
    "get_app_info",
    "get_all_apps",
    "get_app_url",
    "ENVIRONMENT",
    "LOCAL_PORTS",
    "is_dev_mode",
    "is_prod_mode",
]
