"""Detail page template with variants: standard, timeline."""

import gradio as gr
from typing import Callable
from dataclasses import dataclass, field


@dataclass
class SectionConfig:
    """Configuration for a detail section."""
    title: str
    type: str = "key_value"  # key_value, markdown, timeline
    fields: list[dict] | None = None  # For key_value: [{"key": "x", "label": "X"}]
    content_key: str | None = None  # For markdown
    events_key: str | None = None  # For timeline


@dataclass
class DetailPageConfig:
    """Configuration for DetailPage."""
    variant: str = "standard"  # standard, timeline
    title_key: str = "title"
    subtitle_key: str | None = None
    badges: list[dict] = field(default_factory=list)  # [{"key": "status", "type": "status"}]
    sections: list[SectionConfig] = field(default_factory=list)
    timeline_events_key: str = "timeline"


class DetailPage:
    """
    Detail page template for showing single entity.

    Variants:
        - standard: Header + key-value sections + markdown sections
        - timeline: Header + activity timeline
    """

    def __init__(self, config: DetailPageConfig | dict):
        if isinstance(config, dict):
            # Convert sections if present
            if "sections" in config and config["sections"]:
                config["sections"] = [
                    SectionConfig(**s) if isinstance(s, dict) else s
                    for s in config["sections"]
                ]
            self.config = DetailPageConfig(**config)
        else:
            self.config = config

    def render(self, data: dict) -> None:
        """
        Render the detail page.

        Args:
            data: Entity data to display
        """
        self._render_header(data)

        if self.config.variant == "timeline":
            self._render_timeline(data)
        else:
            self._render_sections(data)

    def _render_header(self, data: dict) -> None:
        """Render detail header with title and badges."""
        title = data.get(self.config.title_key, "Untitled")
        subtitle = data.get(self.config.subtitle_key, "") if self.config.subtitle_key else ""

        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown(f"## {title}")
                if subtitle:
                    gr.Markdown(f"*{subtitle}*")

            with gr.Column(scale=1):
                badges_html = '<div style="display: flex; gap: 8px; justify-content: flex-end;">'
                for badge_config in self.config.badges:
                    value = data.get(badge_config["key"], "")
                    if value:
                        color = self._get_badge_color(value, badge_config.get("type", "status"))
                        badges_html += f'''
                        <span style="
                            background-color: {color}20;
                            color: {color};
                            padding: 4px 12px;
                            border-radius: 9999px;
                            font-size: 12px;
                            font-weight: 600;
                            text-transform: uppercase;
                        ">{value}</span>
                        '''
                badges_html += '</div>'
                gr.HTML(badges_html)

    def _render_sections(self, data: dict) -> None:
        """Render detail sections."""
        for section in self.config.sections:
            gr.Markdown(f"### {section.title}")

            if section.type == "key_value":
                self._render_key_value_section(data, section)
            elif section.type == "markdown":
                self._render_markdown_section(data, section)
            elif section.type == "timeline":
                self._render_timeline_section(data, section)

    def _render_key_value_section(self, data: dict, section: SectionConfig) -> None:
        """Render key-value pairs section."""
        if not section.fields:
            return

        html = '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">'
        for field in section.fields:
            key = field.get("key", "")
            label = field.get("label", key.replace("_", " ").title())
            value = data.get(key, "N/A")

            html += f'''
            <div>
                <div style="font-size: 12px; color: #6b7280; margin-bottom: 2px;">{label}</div>
                <div style="font-size: 14px; color: #111827;">{value}</div>
            </div>
            '''
        html += '</div>'
        gr.HTML(html)

    def _render_markdown_section(self, data: dict, section: SectionConfig) -> None:
        """Render markdown content section."""
        if not section.content_key:
            return

        content = data.get(section.content_key, "")
        if content:
            gr.Markdown(content)
        else:
            gr.Markdown("*No content available*")

    def _render_timeline_section(self, data: dict, section: SectionConfig) -> None:
        """Render timeline section."""
        events_key = section.events_key or "timeline"
        events = data.get(events_key, [])
        self._render_timeline_events(events)

    def _render_timeline(self, data: dict) -> None:
        """Render full timeline variant."""
        events = data.get(self.config.timeline_events_key, [])
        gr.Markdown("### Activity Timeline")
        self._render_timeline_events(events)

    def _render_timeline_events(self, events: list[dict]) -> None:
        """Render timeline events."""
        if not events:
            gr.HTML('<div style="color: #6b7280; padding: 16px;">No activity yet</div>')
            return

        html = '<div style="position: relative; padding-left: 24px;">'
        html += '<div style="position: absolute; left: 7px; top: 8px; bottom: 8px; width: 2px; background: #e5e7eb;"></div>'

        for event in events:
            time = event.get("time", event.get("timestamp", ""))
            title = event.get("event", event.get("title", ""))
            details = event.get("details", event.get("description", ""))
            agent = event.get("agent", "")

            html += f'''
            <div style="position: relative; padding-bottom: 16px;">
                <div style="
                    position: absolute;
                    left: -20px;
                    width: 12px;
                    height: 12px;
                    background: #3b82f6;
                    border-radius: 50%;
                    border: 2px solid white;
                "></div>
                <div style="display: flex; gap: 8px; align-items: baseline;">
                    <span style="font-size: 12px; color: #6b7280; min-width: 50px;">{time}</span>
                    <span style="font-weight: 500; color: #111827;">{title}</span>
                    {f'<span style="font-size: 11px; color: #9ca3af;">({agent})</span>' if agent else ''}
                </div>
                {f'<div style="margin-left: 58px; font-size: 13px; color: #6b7280;">{details}</div>' if details else ''}
            </div>
            '''

        html += '</div>'
        gr.HTML(html)

    def _get_badge_color(self, value: str, badge_type: str) -> str:
        """Get color for badge based on value and type."""
        if badge_type == "severity":
            severity_colors = {
                "p1": "#dc2626",
                "p2": "#ea580c",
                "p3": "#ca8a04",
                "p4": "#6b7280",
                "critical": "#dc2626",
                "high": "#ea580c",
                "medium": "#ca8a04",
                "low": "#6b7280",
            }
            return severity_colors.get(value.lower(), "#6b7280")
        else:  # status
            status_colors = {
                "open": "#ef4444",
                "in_progress": "#f59e0b",
                "in progress": "#f59e0b",
                "resolved": "#22c55e",
                "closed": "#6b7280",
            }
            return status_colors.get(value.lower(), "#6b7280")
