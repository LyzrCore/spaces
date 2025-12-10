"""
Base App Class for consistent app structure across the ecosystem.

Provides a base class that handles:
- Multi-page routing with gr.Blocks.route()
- Consistent layout with navbar and footer
- Cross-app navigation
- HuggingFace OAuth login support
"""

from abc import ABC, abstractmethod
from typing import Callable
import gradio as gr

# Support both local and HF Spaces imports
try:
    from config.app_registry import get_app_info
    from apps.shared.ui_components import get_navbar_links, create_footer
except ImportError:
    from config.app_registry import get_app_info
    from shared.ui_components import get_navbar_links, create_footer


class AppBase(ABC):
    """
    Base class for all apps in the ecosystem.

    Provides multi-page routing with consistent layout including
    navbar (cross-app navigation) and footer.
    """

    def __init__(self, app_id: str, title: str, description: str | None = None):
        """
        Initialize the app.

        Args:
            app_id: Unique identifier matching registry key
            title: Display title for the app
            description: Optional description shown in header
        """
        self.app_id = app_id
        self.title = title
        self.description = description
        self._pages: list[tuple[str, str, Callable]] = []

        # Validate app exists in registry
        app_info = get_app_info(app_id)
        if not app_info:
            raise ValueError(f"App '{app_id}' not found in registry")

        self.app_info = app_info

    def add_page(self, name: str, path: str, build_fn: Callable[[], None]) -> None:
        """
        Register a page for this app.

        Args:
            name: Display name for the page (shown in navbar)
            path: URL path for the page (e.g., "/", "/settings")
            build_fn: Function that builds the page content
        """
        self._pages.append((name, path, build_fn))

    def get_page_list(self) -> list[tuple[str, str]]:
        """Get list of (name, path) for all pages."""
        return [(name, path) for name, path, _ in self._pages]

    def _build_page_with_layout(self, build_fn: Callable, navbar_links: list) -> None:
        """
        Build a page wrapped in the standard layout.

        Args:
            build_fn: Function that builds the page content
            navbar_links: Links for the navbar
        """
        # Top navbar with cross-app navigation
        gr.Navbar(
            value=navbar_links,
            main_page_name=self.title,
        )

        # Login button for HuggingFace OAuth
        with gr.Row():
            with gr.Column(scale=4):
                if self.description:
                    gr.Markdown(f"*{self.description}*")
            with gr.Column(scale=1, min_width=150):
                gr.LoginButton()

        # Main content area
        build_fn()

        # Footer
        create_footer()

    @abstractmethod
    def register_pages(self) -> None:
        """
        Register all pages for this app.

        Subclasses must implement this method to call add_page()
        for each page they want to include.

        Example:
            def register_pages(self):
                self.add_page("Home", "/", self.build_home)
                self.add_page("Settings", "/settings", self.build_settings)
        """
        pass

    def build(self) -> gr.Blocks:
        """
        Build the complete Gradio interface with all pages.

        Returns:
            gr.Blocks instance with multi-page routing
        """
        # Register pages first
        self.register_pages()

        if not self._pages:
            raise ValueError("No pages registered. Call add_page() in register_pages().")

        # Get navbar links to other apps
        navbar_links = get_navbar_links(self.app_id)

        # Build main page (first registered page, typically "/")
        main_name, main_path, main_build_fn = self._pages[0]

        with gr.Blocks(title=self.title) as demo:
            self._build_page_with_layout(main_build_fn, navbar_links)

        # Build additional pages with routes (outside the Blocks context)
        for name, path, build_fn in self._pages[1:]:
            with demo.route(name, path):
                self._build_page_with_layout(build_fn, navbar_links)

        return demo

    def launch(self, **kwargs) -> None:
        """
        Build and launch the app.

        Args:
            **kwargs: Arguments passed to gr.Blocks.launch()
        """
        demo = self.build()
        demo.launch(**kwargs)
