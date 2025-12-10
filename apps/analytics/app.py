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
    from config.settings import LOCAL_PORTS, is_dev_mode
except ImportError:
    from shared.custom_components import AppBase
    from config.settings import LOCAL_PORTS, is_dev_mode


class AnalyticsApp(AppBase):
    """Analytics dashboard application with Home and Settings pages."""

    def register_pages(self) -> None:
        """Register all pages for the analytics app."""
        self.add_page("Home", "/", self.build_home)
        self.add_page("Settings", "/settings", self.build_settings)

    def build_home(self) -> None:
        """Build the home page content."""
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

    def build_settings(self) -> None:
        """Build the settings page content."""
        gr.Markdown("## Analytics Settings")
        gr.Markdown("Configure your analytics preferences here.")

        with gr.Group():
            gr.Markdown("### Data Collection")
            tracking_enabled = gr.Checkbox(
                label="Enable Tracking",
                value=True,
            )
            anonymize_ip = gr.Checkbox(
                label="Anonymize IP Addresses",
                value=True,
            )

        with gr.Group():
            gr.Markdown("### Report Settings")
            default_date_range = gr.Dropdown(
                label="Default Date Range",
                choices=["Today", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
                value="Last 7 Days",
            )
            email_reports = gr.Checkbox(
                label="Email Weekly Reports",
                value=False,
            )
            report_email = gr.Textbox(
                label="Report Email",
                placeholder="your@email.com",
                visible=True,
            )

        save_btn = gr.Button("Save Settings", variant="primary")
        status = gr.Textbox(label="Status", interactive=False)

        def save_settings(tracking, anonymize, date_range, email_reports, email):
            return f"Settings saved: Tracking={tracking}, Anonymize={anonymize}, Range={date_range}"

        save_btn.click(
            fn=save_settings,
            inputs=[tracking_enabled, anonymize_ip, default_date_range, email_reports, report_email],
            outputs=status,
        )


if __name__ == "__main__":
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
