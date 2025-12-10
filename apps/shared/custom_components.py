"""
Base App Class for consistent app structure across the ecosystem.

Provides a base class that handles:
- Common header/footer creation
- Navigation integration
- Consistent layout structure
"""

from abc import ABC, abstractmethod
import gradio as gr

# Support both local and HF Spaces imports
try:
    from config.app_registry import get_app_info
    from apps.shared.ui_components import header, footer, navigation
except ImportError:
    from config.app_registry import get_app_info
    from shared.ui_components import header, footer, navigation


class AppBase(ABC):
    """
    Base class for all apps in the ecosystem.

    Subclasses must implement the `build()` method to define
    their specific UI and functionality.
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

        # Validate app exists in registry
        app_info = get_app_info(app_id)
        if not app_info:
            raise ValueError(f"App '{app_id}' not found in registry")

        self.app_info = app_info

    def create_header(self) -> None:
        """Create the standard header with title and navigation."""
        header(self.title, self.description)
        navigation(self.app_id)

    def create_footer(self) -> None:
        """Create the standard footer."""
        footer()

    @abstractmethod
    def build(self) -> gr.Blocks:
        """
        Build the Gradio interface.

        Subclasses must implement this method to define their UI.
        Should create a gr.Blocks context with:
        - self.create_header()
        - Custom UI components
        - self.create_footer()

        Returns:
            gr.Blocks instance
        """
        pass

    def launch(self, **kwargs) -> None:
        """
        Build and launch the app.

        Args:
            **kwargs: Arguments passed to gr.Blocks.launch()
        """
        demo = self.build()
        demo.launch(**kwargs)
