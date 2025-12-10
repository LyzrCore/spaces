"""Shared components for the Gradio Spaces ecosystem."""

# Support both local and HF Spaces imports
try:
    from apps.shared.ui_components import (
        get_navbar_links,
        create_sidebar_content,
        create_footer,
    )
    from apps.shared.custom_components import AppBase
except ImportError:
    from shared.ui_components import (
        get_navbar_links,
        create_sidebar_content,
        create_footer,
    )
    from shared.custom_components import AppBase

__all__ = [
    "get_navbar_links",
    "create_sidebar_content",
    "create_footer",
    "AppBase",
]
