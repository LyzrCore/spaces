"""
Analytics - Analytics dashboard application.
"""

import sys
from pathlib import Path

# Add project root to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import gradio as gr

# Support both local (apps.shared) and HF Spaces (shared) imports
try:
    from apps.shared.custom_components import AppBase
    from config.settings import LOCAL_PORTS
except ImportError:
    from shared.custom_components import AppBase
    from config.settings import LOCAL_PORTS


class AnalyticsApp(AppBase):
    """Analytics dashboard application."""

    def build(self) -> gr.Blocks:
        with gr.Blocks(title=self.title) as demo:
            self.create_header()

            gr.Markdown("## Analytics Dashboard")
            gr.Markdown("View your analytics data here.")

            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Overview")
                    with gr.Row():
                        total_users = gr.Number(label="Total Users", value=1234, interactive=False)
                        active_sessions = gr.Number(label="Active Sessions", value=56, interactive=False)
                        conversion_rate = gr.Number(label="Conversion Rate (%)", value=3.2, interactive=False)

                with gr.Column(scale=1):
                    gr.Markdown("### Actions")
                    refresh_btn = gr.Button("Refresh Data", variant="primary")
                    export_btn = gr.Button("Export Report", variant="secondary")

            with gr.Row():
                date_range = gr.Dropdown(
                    label="Date Range",
                    choices=["Today", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                    value="Last 7 Days",
                )
                metric_type = gr.Dropdown(
                    label="Metric Type",
                    choices=["Users", "Sessions", "Pageviews", "Events"],
                    value="Users",
                )

            status_output = gr.Textbox(label="Status", interactive=False)

            def refresh_data():
                import random
                return (
                    random.randint(1000, 2000),
                    random.randint(40, 80),
                    round(random.uniform(2.0, 5.0), 1),
                    "Data refreshed",
                )

            def export_report(date: str, metric: str) -> str:
                return f"Exporting {metric} report for {date}..."

            refresh_btn.click(
                fn=refresh_data,
                outputs=[total_users, active_sessions, conversion_rate, status_output],
            )

            export_btn.click(
                fn=export_report,
                inputs=[date_range, metric_type],
                outputs=status_output,
            )

            self.create_footer()

        return demo


if __name__ == "__main__":
    from config.settings import is_dev_mode

    app = AnalyticsApp(
        app_id="analytics",
        title="Analytics",
        description="View and analyze your data",
    )
    demo = app.build()

    # Only specify port in dev mode; HF Spaces manages ports automatically
    if is_dev_mode():
        demo.launch(server_port=LOCAL_PORTS.get("analytics", 7861))
    else:
        demo.launch()
