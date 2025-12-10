"""
Dashboard - Main dashboard application.
"""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import gradio as gr
from apps.shared.custom_components import AppBase
from config.settings import LOCAL_PORTS


class DashboardApp(AppBase):
    """Main dashboard application."""

    def build(self) -> gr.Blocks:
        with gr.Blocks(title=self.title) as demo:
            self.create_header()

            gr.Markdown("## Welcome to the Dashboard")
            gr.Markdown("This is the main dashboard. Use the navigation above to access other apps.")

            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Quick Stats")
                    status_text = gr.Textbox(
                        label="System Status",
                        value="All systems operational",
                        interactive=False,
                    )

                with gr.Column():
                    gr.Markdown("### Actions")
                    refresh_btn = gr.Button("Refresh Status", variant="primary")
                    message_input = gr.Textbox(
                        label="Message",
                        placeholder="Enter a message...",
                    )
                    message_output = gr.Textbox(label="Response", interactive=False)

            def get_status() -> str:
                return "Dashboard is running - Status: OK"

            def echo_message(message: str) -> str:
                return f"You said: {message}"

            refresh_btn.click(fn=get_status, outputs=status_text)
            message_input.submit(fn=echo_message, inputs=message_input, outputs=message_output)

            self.create_footer()

        return demo


if __name__ == "__main__":
    app = DashboardApp(
        app_id="dashboard",
        title="Dashboard",
        description="Main dashboard for the Lyzr ecosystem",
    )
    demo = app.build()
    demo.launch(server_port=LOCAL_PORTS.get("dashboard", 7860))
