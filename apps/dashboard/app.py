"""
Dashboard - Main dashboard application.
"""

import sys
from pathlib import Path

# Add project root to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import gradio as gr

# Support both local (apps.shared) and HF Spaces (shared) imports
try:
    from apps.shared.custom_components import AppBase
    from config.settings import LOCAL_PORTS, is_dev_mode
except ImportError:
    from shared.custom_components import AppBase
    from config.settings import LOCAL_PORTS, is_dev_mode


class DashboardApp(AppBase):
    """Main dashboard application with Home and Settings pages."""

    def register_pages(self) -> None:
        """Register all pages for the dashboard."""
        self.add_page("Home", "/", self.build_home)
        self.add_page("Settings", "/settings", self.build_settings)

    def build_home(self) -> None:
        """Build the home page content."""
        gr.Markdown("## Welcome to the Dashboard")
        gr.Markdown("This is the main dashboard. Use the sidebar to navigate between pages.")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Quick Stats")
                status_text = gr.Textbox(
                    label="System Status",
                    value="All systems operational",
                    interactive=False,
                )
                refresh_btn = gr.Button("Refresh Status", variant="primary")

                def get_status() -> str:
                    return "Dashboard is running - Status: OK"

                refresh_btn.click(fn=get_status, outputs=status_text)

            with gr.Column():
                gr.Markdown("### Quick Actions")
                message_input = gr.Textbox(
                    label="Message",
                    placeholder="Enter a message...",
                )
                message_output = gr.Textbox(label="Response", interactive=False)

                def echo_message(message: str) -> str:
                    return f"You said: {message}"

                message_input.submit(fn=echo_message, inputs=message_input, outputs=message_output)

    def build_settings(self) -> None:
        """Build the settings page content."""
        gr.Markdown("## Settings")
        gr.Markdown("Configure your dashboard preferences here.")

        with gr.Group():
            gr.Markdown("### Display Settings")
            theme = gr.Dropdown(
                label="Theme",
                choices=["Light", "Dark", "System"],
                value="System",
            )
            notifications = gr.Checkbox(
                label="Enable Notifications",
                value=True,
            )

        with gr.Group():
            gr.Markdown("### Data Settings")
            refresh_interval = gr.Slider(
                label="Auto-refresh Interval (seconds)",
                minimum=5,
                maximum=300,
                value=30,
                step=5,
            )

        save_btn = gr.Button("Save Settings", variant="primary")
        status = gr.Textbox(label="Status", interactive=False)

        def save_settings(theme_val, notif_val, interval_val):
            return f"Settings saved: Theme={theme_val}, Notifications={notif_val}, Refresh={interval_val}s"

        save_btn.click(
            fn=save_settings,
            inputs=[theme, notifications, refresh_interval],
            outputs=status,
        )


if __name__ == "__main__":
    app = DashboardApp(
        app_id="dashboard",
        title="Dashboard",
        description="Main dashboard for the Lyzr ecosystem",
    )
    demo = app.build()

    # Only specify port in dev mode; HF Spaces manages ports automatically
    if is_dev_mode():
        demo.launch(server_port=LOCAL_PORTS.get("dashboard", 7860))
    else:
        demo.launch()
