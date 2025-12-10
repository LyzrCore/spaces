"""
Shared UI components for consistent styling across all apps.

Provides reusable layout components: navbar links and footer.
"""

import gradio as gr

# Support both local and HF Spaces imports
try:
    from config.app_registry import APPS_REGISTRY, get_app_info, get_all_apps
    from config.settings import get_app_url
except ImportError:
    import sys
    sys.path.insert(0, "/app")
    from config.app_registry import APPS_REGISTRY, get_app_info, get_all_apps
    from config.settings import get_app_url


def get_navbar_links(current_app_id: str) -> list[tuple[str, str]]:
    """
    Generate navbar links for cross-app navigation.

    Args:
        current_app_id: Current app's ID (excluded from links)

    Returns:
        List of (name, url) tuples for other apps
    """
    links = []
    for app_id in get_all_apps():
        if app_id != current_app_id:
            app_info = get_app_info(app_id)
            if app_info:
                url = get_app_url(app_id)
                if url:
                    links.append((app_info["name"], url))
    return links


def create_footer() -> gr.Markdown:
    """
    Create a standard footer component.

    Returns:
        gr.Markdown component
    """
    return gr.Markdown(
        """
---
**Powered by Lyzr** | [lyzr.ai](https://lyzr.ai)
""",
        elem_classes=["footer"]
    )
