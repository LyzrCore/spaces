"""
App builder engine - builds Gradio apps from configuration.

This module provides a configuration-driven approach to building
demo applications powered by blueprint agent orchestration.
"""

import gradio as gr
from typing import Callable, Any
from dataclasses import dataclass, field

# Support both local and HF Spaces imports
try:
    from apps.shared.pages import ListPage, DetailPage, FormPage, DashboardPage
    from apps.shared.pages.form_page import create_processing_html
    from apps.shared.ui_components import create_footer
except ImportError:
    from shared.pages import ListPage, DetailPage, FormPage, DashboardPage
    from shared.pages.form_page import create_processing_html
    from shared.ui_components import create_footer


@dataclass
class AppConfig:
    """Configuration for a demo application."""
    id: str
    title: str
    description: str | None = None

    # Header links
    github_url: str | None = None
    studio_url: str | None = None
    readme_url: str | None = None

    # Entity naming
    entity_name: str = "item"
    entity_name_plural: str = "items"

    # Sidebar navigation
    sidebar: list[dict] = field(default_factory=list)

    # Pages configuration
    pages: dict[str, dict] = field(default_factory=dict)

    # Data sources
    data: dict[str, Any] = field(default_factory=dict)

    # Orchestrator for processing
    orchestrator: Any = None


class DemoApp:
    """
    Demo application builder.

    Builds a complete Gradio app from configuration with:
    - Sidebar navigation
    - Header with links
    - Page templates
    - Data binding
    - Orchestrator integration
    """

    PAGE_TEMPLATES = {
        "list": ListPage,
        "detail": DetailPage,
        "form": FormPage,
        "dashboard": DashboardPage,
    }

    def __init__(self, config: AppConfig | dict):
        if isinstance(config, dict):
            self.config = AppConfig(**config)
        else:
            self.config = config

        self._current_page = "/"

    def build(self) -> gr.Blocks:
        """Build the complete Gradio application."""
        with gr.Blocks(title=self.config.title) as demo:
            # State for current item (for detail views)
            current_item = gr.State(None)

            # Header
            self._build_header()

            # Main layout: Sidebar + Content
            with gr.Row():
                # Sidebar
                with gr.Column(scale=1, min_width=200):
                    self._build_sidebar()

                # Content area
                with gr.Column(scale=4):
                    # Build all pages as separate containers
                    page_containers = {}
                    for path, page_config in self.config.pages.items():
                        is_home = path == "/"
                        with gr.Column(visible=is_home, elem_id=f"page-{path.replace('/', '-')}") as container:
                            self._build_page(path, page_config)
                        page_containers[path] = container

            # Footer
            create_footer()

        return demo


    def _build_header(self) -> None:
        """Build app header with title and links."""
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown(f"# {self.config.title}")
                if self.config.description:
                    gr.Markdown(f"*{self.config.description}*")

            with gr.Column(scale=1, min_width=300):
                links_html = '<div style="display: flex; gap: 16px; justify-content: flex-end; align-items: center; padding-top: 8px;">'
                if self.config.github_url:
                    links_html += f'<a href="{self.config.github_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">⭐ GitHub</a>'
                if self.config.studio_url:
                    links_html += f'<a href="{self.config.studio_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">🚀 Lyzr Studio</a>'
                if self.config.readme_url:
                    links_html += f'<a href="{self.config.readme_url}" target="_blank" style="text-decoration: none; color: #374151; font-size: 14px;">📖 Readme</a>'
                links_html += '</div>'
                gr.HTML(links_html)

    def _build_sidebar(self) -> None:
        """Build sidebar navigation."""
        for item in self.config.sidebar:
            icon = item.get("icon", "")
            label = item.get("label", "")

            gr.Button(
                f"{icon} {label}".strip(),
                variant="secondary",
                size="sm",
            )

    def _build_page(self, path: str, page_config: dict) -> None:
        """Build a single page from configuration."""
        page_type = page_config.get("page", "list")
        variant = page_config.get("variant", "standard")
        config = page_config.get("config", {})
        config["variant"] = variant

        # Get data for this page
        data = self._get_page_data(path, page_config)

        if page_type == "list":
            template = ListPage(config)
            template.render(data)

        elif page_type == "detail":
            template = DetailPage(config)
            if data:
                template.render(data)
            else:
                gr.Markdown("*Select an item to view details*")

        elif page_type == "form":
            template = FormPage(config)
            submit_btn, fields, result_container, processing_html, result_output = template.render()

            # Connect form submission to orchestrator
            if self.config.orchestrator:
                self._connect_form_to_orchestrator(
                    submit_btn, fields, template,
                    result_container, processing_html, result_output
                )

        elif page_type == "dashboard":
            template = DashboardPage(config)
            template.render(data)

    def _get_page_data(self, path: str, page_config: dict) -> Any:
        """Get data for a page from configured data sources."""
        data_key = page_config.get("data_key")
        if data_key and data_key in self.config.data:
            return self.config.data[data_key]

        # Fallback: check if there's mock_data in page config
        if "mock_data" in page_config:
            return page_config["mock_data"]

        return []

    def _connect_form_to_orchestrator(
        self,
        submit_btn: gr.Button,
        fields: dict,
        template: FormPage,
        result_container: gr.Column,
        processing_html: gr.HTML,
        result_output: gr.Markdown,
    ) -> None:
        """Connect form submission to orchestrator processing."""

        def process_form(*field_values):
            # Build input dict from field values
            field_keys = template.get_field_keys()
            input_data = dict(zip(field_keys, field_values))

            # Process through orchestrator
            if self.config.orchestrator:
                result = self.config.orchestrator.process(input_data)
                return (
                    gr.update(visible=True),  # Show result container
                    "",  # Clear processing (done)
                    f"### Result\n\n{self._format_result(result)}"
                )
            else:
                return (
                    gr.update(visible=True),
                    "",
                    "### Result\n\n*Processing complete (no orchestrator configured)*"
                )

        submit_btn.click(
            fn=process_form,
            inputs=list(fields.values()),
            outputs=[result_container, processing_html, result_output],
        )

    def _format_result(self, result: dict) -> str:
        """Format orchestrator result as markdown."""
        if not result:
            return "*No result*"

        md = ""
        for key, value in result.items():
            label = key.replace("_", " ").title()
            if isinstance(value, list):
                md += f"**{label}:**\n"
                for item in value:
                    if isinstance(item, dict):
                        md += f"- {item.get('event', item.get('title', str(item)))}\n"
                    else:
                        md += f"- {item}\n"
            else:
                md += f"**{label}:** {value}\n\n"

        return md

    def launch(self, **kwargs) -> None:
        """Build and launch the app."""
        demo = self.build()
        # Use Glass theme with light mode
        if "theme" not in kwargs:
            kwargs["theme"] = gr.themes.Glass()
        demo.launch(**kwargs)


def build_app(config: dict | AppConfig) -> gr.Blocks:
    """
    Build a Gradio app from configuration.

    Args:
        config: App configuration dict or AppConfig instance

    Returns:
        gr.Blocks instance ready to launch
    """
    app = DemoApp(config)
    return app.build()
