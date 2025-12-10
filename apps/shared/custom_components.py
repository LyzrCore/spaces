"""
Base App Class for consistent app structure across the ecosystem.

Provides a base class that handles:
- Multi-page routing with gr.Blocks.route()
- Consistent layout with navbar and footer
- Cross-app navigation
- HuggingFace OAuth login with protected content
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
    navbar (cross-app navigation) and footer. Content is protected
    behind HuggingFace OAuth authentication.
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

    def _get_landing_css(self) -> str:
        """Get CSS for the centered modal landing page."""
        return """
        #landing-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
        }
        #login-modal {
            background: var(--background-fill-primary);
            border: 1px solid var(--border-color-primary);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
        }
        #login-modal h2 {
            margin-bottom: 0.5rem;
        }
        #login-modal p {
            color: var(--body-text-color-subdued);
            margin-bottom: 1.5rem;
        }
        .login-features {
            text-align: left;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color-primary);
        }
        .login-features ul {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
            color: var(--body-text-color-subdued);
        }
        """

    def _build_landing_page(self) -> None:
        """Build the landing page as a centered modal."""
        # Centered modal: 30% spacer | 40% modal | 30% spacer
        with gr.Row():
            with gr.Column(scale=3, min_width=0):
                pass  # Left spacer
            with gr.Column(scale=4, min_width=300, elem_id="login-modal"):
                gr.Markdown(f"## Welcome to {self.title}")
                if self.description:
                    gr.Markdown(f"{self.description}")
                gr.Markdown("Sign in with your HuggingFace account to continue.")
                gr.LoginButton(size="lg")
                gr.Markdown(
                    """
<div class="login-features">

**Why sign in?**
- Access all features of the application
- Your settings and preferences are saved
- Seamless integration with HuggingFace ecosystem

</div>
                    """
                )
            with gr.Column(scale=3, min_width=0):
                pass  # Right spacer

    def _build_page_with_layout(self, build_fn: Callable, navbar_links: list) -> None:
        """
        Build a page wrapped in the standard layout with auth check.

        Args:
            build_fn: Function that builds the page content
            navbar_links: Links for the navbar
        """
        # Inject CSS for landing modal
        gr.HTML(f"<style>{self._get_landing_css()}</style>", visible=False)

        # Top navbar with cross-app navigation
        gr.Navbar(
            value=navbar_links,
            main_page_name=self.title,
        )

        # Container for landing page (shown when not logged in)
        landing_container = gr.Column(visible=True, elem_id="landing-container")

        # Container for app content (shown when logged in)
        app_container = gr.Column(visible=False, elem_id="app-container")

        with landing_container:
            self._build_landing_page()

        with app_container:
            # Header with user info
            with gr.Row():
                with gr.Column(scale=4):
                    if self.description:
                        gr.Markdown(f"*{self.description}*")
                    user_info = gr.Markdown("", elem_id="user-info")

            # Main content area
            build_fn()

            # Footer
            create_footer()

        # Check auth status on load
        def check_auth(profile: gr.OAuthProfile | None):
            if profile is None:
                return (
                    gr.update(visible=True),   # Show landing
                    gr.update(visible=False),  # Hide app
                    ""
                )
            else:
                return (
                    gr.update(visible=False),  # Hide landing
                    gr.update(visible=True),   # Show app
                    f"Welcome, **{profile.name}**!"
                )

        # Use demo.load to check auth on page load
        # This will be connected in the build() method
        self._auth_check_fn = check_auth
        self._auth_outputs = [landing_container, app_container, user_info]

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
            # Connect auth check to page load
            demo.load(
                fn=self._auth_check_fn,
                inputs=None,
                outputs=self._auth_outputs
            )

        # Build additional pages with routes (outside the Blocks context)
        for name, path, build_fn in self._pages[1:]:
            with demo.route(name, path):
                self._build_page_with_layout(build_fn, navbar_links)
                # Note: demo.load in routes is handled by Gradio automatically

        return demo

    def launch(self, **kwargs) -> None:
        """
        Build and launch the app.

        Args:
            **kwargs: Arguments passed to gr.Blocks.launch()
        """
        demo = self.build()
        demo.launch(**kwargs)
