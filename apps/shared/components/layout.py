"""Layout components for page structure."""

import gradio as gr
from typing import Callable


def PageHeader(
    title: str,
    description: str | None = None,
    github_url: str | None = None,
    studio_url: str | None = None,
    readme_url: str | None = None,
) -> None:
    """
    Render page header with title and action links.

    Args:
        title: App title
        description: Optional description
        github_url: GitHub repo URL
        studio_url: Lyzr Studio blueprint URL
        readme_url: Readme/docs URL
    """
    with gr.Row(elem_classes=["page-header"]):
        with gr.Column(scale=3):
            gr.Markdown(f"# {title}")
            if description:
                gr.Markdown(f"*{description}*")
        with gr.Column(scale=1, min_width=300):
            links_html = '<div style="display: flex; gap: 16px; justify-content: flex-end; align-items: center;">'
            if github_url:
                links_html += f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">⭐ Star on GitHub</a>'
            if studio_url:
                links_html += f'<a href="{studio_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">🚀 Lyzr Studio</a>'
            if readme_url:
                links_html += f'<a href="{readme_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">📖 Readme</a>'
            links_html += '</div>'
            gr.HTML(links_html)


def Section(title: str, build_fn: Callable[[], None]) -> None:
    """
    Render a titled section.

    Args:
        title: Section title
        build_fn: Function that builds section content
    """
    gr.Markdown(f"### {title}")
    build_fn()


def Sidebar(
    items: list[dict],
    on_navigate: Callable[[str], None] | None = None,
) -> gr.Column:
    """
    Render sidebar navigation.

    Args:
        items: List of {"label": str, "path": str, "icon": str}
        on_navigate: Callback when item is clicked

    Returns:
        gr.Column containing sidebar
    """
    with gr.Column(scale=1, min_width=200, elem_classes=["sidebar"]) as sidebar:
        for item in items:
            icon = item.get("icon", "")
            label = item.get("label", "")
            path = item.get("path", "/")

            btn = gr.Button(
                f"{icon} {label}".strip(),
                variant="secondary",
                size="sm",
                elem_classes=["sidebar-item"],
            )
            if on_navigate:
                btn.click(fn=lambda p=path: on_navigate(p), inputs=[], outputs=[])

    return sidebar
