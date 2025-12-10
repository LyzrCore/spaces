"""
Shared UI components for consistent styling across all apps.

Provides reusable header, footer, and navigation components.
"""

import gradio as gr
from config.app_registry import APPS_REGISTRY, get_app_info, get_all_apps
from config.settings import get_app_url


def header(title: str, subtitle: str | None = None) -> gr.Markdown:
    """
    Create a header component with title and optional subtitle.

    Args:
        title: Main title text
        subtitle: Optional subtitle/description

    Returns:
        gr.Markdown component
    """
    content = f"# {title}"
    if subtitle:
        content += f"\n\n*{subtitle}*"

    return gr.Markdown(content)


def footer() -> gr.Markdown:
    """
    Create a standard footer component.

    Returns:
        gr.Markdown component
    """
    content = """
---

**Powered by Lyzr** | [lyzr.space](https://lyzr.space)
"""
    return gr.Markdown(content)


def navigation(current_app_id: str) -> gr.Markdown:
    """
    Create navigation links to all other apps.

    Args:
        current_app_id: Current app's ID (will be highlighted, not linked)

    Returns:
        gr.Markdown component with navigation links
    """
    lines: list[str] = ["---", "### All Apps", ""]

    app_links = []
    for app_id in get_all_apps():
        app_info = get_app_info(app_id)
        if app_info:
            if app_id == current_app_id:
                # Current app - bold, no link
                app_links.append(f"**{app_info['name']}**")
            else:
                url = get_app_url(app_id)
                app_links.append(f"[{app_info['name']}]({url})")

    lines.append(" | ".join(app_links))
    lines.append("")
    lines.append("---")

    return gr.Markdown("\n".join(lines))
