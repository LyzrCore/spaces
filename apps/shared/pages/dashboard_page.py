"""Dashboard page template with variants: metrics, activity."""

import gradio as gr
from dataclasses import dataclass, field


@dataclass
class StatConfig:
    """Configuration for a stat card."""
    label: str
    value_key: str
    icon: str = ""
    color: str = "blue"


@dataclass
class DashboardPageConfig:
    """Configuration for DashboardPage."""
    variant: str = "metrics"  # metrics, activity
    title: str = "Dashboard"
    stats: list[StatConfig] = field(default_factory=list)
    recent_items_key: str = "recent_items"
    recent_items_title: str = "Recent Items"
    recent_items_limit: int = 5


class DashboardPage:
    """
    Dashboard page template for overview.

    Variants:
        - metrics: Stats cards + recent items
        - activity: Stats + activity feed
    """

    def __init__(self, config: DashboardPageConfig | dict):
        if isinstance(config, dict):
            # Convert stats if present
            if "stats" in config and config["stats"]:
                config["stats"] = [
                    StatConfig(**s) if isinstance(s, dict) else s
                    for s in config["stats"]
                ]
            self.config = DashboardPageConfig(**config)
        else:
            self.config = config

    def render(self, data: dict) -> None:
        """
        Render the dashboard page.

        Args:
            data: Dashboard data including stats and recent items
        """
        gr.Markdown(f"## {self.config.title}")

        # Render stats cards
        if self.config.stats:
            self._render_stats(data)

        # Render recent items
        if self.config.recent_items_key in data:
            self._render_recent_items(data)

    def _render_stats(self, data: dict) -> None:
        """Render stats cards."""
        color_map = {
            "blue": "#3b82f6",
            "green": "#22c55e",
            "yellow": "#f59e0b",
            "red": "#ef4444",
            "purple": "#8b5cf6",
            "gray": "#6b7280",
        }

        with gr.Row():
            for stat in self.config.stats:
                value = data.get(stat.value_key, 0)
                color = color_map.get(stat.color, "#3b82f6")

                with gr.Column(scale=1, min_width=150):
                    gr.HTML(f'''
                    <div style="
                        background: white;
                        border: 1px solid #e5e7eb;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                    ">
                        <div style="font-size: 32px; margin-bottom: 8px;">{stat.icon}</div>
                        <div style="font-size: 28px; font-weight: 700; color: {color};">{value}</div>
                        <div style="font-size: 14px; color: #6b7280;">{stat.label}</div>
                    </div>
                    ''')

    def _render_recent_items(self, data: dict) -> None:
        """Render recent items list."""
        items = data.get(self.config.recent_items_key, [])
        items = items[:self.config.recent_items_limit]

        gr.Markdown(f"### {self.config.recent_items_title}")

        if not items:
            gr.HTML('<div style="color: #6b7280; padding: 16px;">No recent items</div>')
            return

        html = '<div style="border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">'

        for i, item in enumerate(items):
            title = item.get("title", item.get("id", "Untitled"))
            status = item.get("status", "")
            created = item.get("created_at", item.get("created", ""))

            border_top = "border-top: 1px solid #e5e7eb;" if i > 0 else ""

            status_color = self._get_status_color(status)
            status_html = ""
            if status:
                status_html = f'''
                <span style="
                    background-color: {status_color}20;
                    color: {status_color};
                    padding: 2px 8px;
                    border-radius: 9999px;
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                ">{status}</span>
                '''

            html += f'''
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 16px;
                {border_top}
            ">
                <div>
                    <div style="font-weight: 500; color: #111827;">{title}</div>
                    <div style="font-size: 12px; color: #6b7280;">{created}</div>
                </div>
                {status_html}
            </div>
            '''

        html += '</div>'
        gr.HTML(html)

    def _get_status_color(self, status: str) -> str:
        """Get color for status."""
        status_colors = {
            "open": "#ef4444",
            "in_progress": "#f59e0b",
            "in progress": "#f59e0b",
            "resolved": "#22c55e",
            "closed": "#6b7280",
        }
        return status_colors.get(status.lower(), "#6b7280")
