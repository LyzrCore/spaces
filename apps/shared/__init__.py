"""Shared components for the Gradio Spaces ecosystem."""

# Support both local and HF Spaces imports
try:
    from apps.shared.ui_components import header, footer, navigation
    from apps.shared.custom_components import AppBase
except ImportError:
    from shared.ui_components import header, footer, navigation
    from shared.custom_components import AppBase

__all__ = [
    "header",
    "footer",
    "navigation",
    "AppBase",
]
