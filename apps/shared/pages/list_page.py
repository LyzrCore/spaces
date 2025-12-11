"""List page template with variants: table, cards, compact."""

import gradio as gr
from typing import Callable
from dataclasses import dataclass


@dataclass
class ColumnConfig:
    """Configuration for a table column."""
    key: str
    label: str
    width: str | None = None
    type: str = "text"  # text, badge, datetime


@dataclass
class ListPageConfig:
    """Configuration for ListPage."""
    variant: str = "table"  # table, cards, compact
    title: str = "Items"
    columns: list[ColumnConfig] | None = None
    card_title_key: str = "title"
    card_subtitle_key: str | None = None
    card_badge_key: str | None = None
    empty_title: str = "No items yet"
    empty_description: str | None = None
    on_item_click: Callable | None = None


class ListPage:
    """
    List page template with multiple variants.

    Variants:
        - table: Dense tabular view with columns
        - cards: Grid of cards with more visual info
        - compact: Simple single-line items
    """

    def __init__(self, config: ListPageConfig | dict):
        if isinstance(config, dict):
            # Convert columns if present
            if "columns" in config and config["columns"]:
                config["columns"] = [
                    ColumnConfig(**c) if isinstance(c, dict) else c
                    for c in config["columns"]
                ]
            self.config = ListPageConfig(**config)
        else:
            self.config = config

    def render(self, data: list[dict], on_select: Callable | None = None) -> gr.Dataframe | gr.HTML:
        """
        Render the list page.

        Args:
            data: List of items to display
            on_select: Callback when item is selected

        Returns:
            Gradio component
        """
        if not data:
            return self._render_empty()

        if self.config.variant == "table":
            return self._render_table(data, on_select)
        elif self.config.variant == "cards":
            return self._render_cards(data, on_select)
        elif self.config.variant == "compact":
            return self._render_compact(data, on_select)
        else:
            return self._render_table(data, on_select)

    def _render_empty(self) -> gr.HTML:
        """Render empty state."""
        return gr.HTML(f'''
        <div style="
            text-align: center;
            padding: 48px 24px;
            color: #6b7280;
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
            <div style="font-size: 18px; font-weight: 600; color: #374151; margin-bottom: 8px;">
                {self.config.empty_title}
            </div>
            {f'<div style="font-size: 14px;">{self.config.empty_description}</div>' if self.config.empty_description else ''}
        </div>
        ''')

    def _render_table(self, data: list[dict], on_select: Callable | None = None) -> gr.Dataframe:
        """Render table variant."""
        if not self.config.columns:
            # Auto-generate columns from first item
            if data:
                columns = [ColumnConfig(key=k, label=k.replace("_", " ").title()) for k in data[0].keys()]
            else:
                columns = []
        else:
            columns = self.config.columns

        headers = [col.label for col in columns]
        rows = []
        for item in data:
            row = []
            for col in columns:
                value = item.get(col.key, "")
                if col.type == "badge":
                    # For badges, just show the text (styling handled separately)
                    row.append(str(value))
                else:
                    row.append(str(value) if value else "")
            rows.append(row)

        df = gr.Dataframe(
            headers=headers,
            value=rows,
            interactive=False,
            wrap=True,
        )

        return df

    def _render_cards(self, data: list[dict], on_select: Callable | None = None) -> gr.HTML:
        """Render cards variant."""
        cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px;">'

        for item in data:
            title = item.get(self.config.card_title_key, "Untitled")
            subtitle = item.get(self.config.card_subtitle_key, "") if self.config.card_subtitle_key else ""
            badge = item.get(self.config.card_badge_key, "") if self.config.card_badge_key else ""

            badge_html = ""
            if badge:
                badge_color = self._get_status_color(badge)
                badge_html = f'''
                <span style="
                    background-color: {badge_color}20;
                    color: {badge_color};
                    padding: 2px 8px;
                    border-radius: 9999px;
                    font-size: 11px;
                    font-weight: 600;
                    text-transform: uppercase;
                ">{badge}</span>
                '''

            cards_html += f'''
            <div style="
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 16px;
                cursor: pointer;
                transition: box-shadow 0.2s;
            " onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.1)'"
               onmouseout="this.style.boxShadow='none'">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                    <div style="font-weight: 600; color: #111827;">{title}</div>
                    {badge_html}
                </div>
                {f'<div style="font-size: 14px; color: #6b7280;">{subtitle}</div>' if subtitle else ''}
            </div>
            '''

        cards_html += '</div>'
        return gr.HTML(cards_html)

    def _render_compact(self, data: list[dict], on_select: Callable | None = None) -> gr.HTML:
        """Render compact variant."""
        items_html = '<div style="border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden;">'

        for i, item in enumerate(data):
            title = item.get(self.config.card_title_key, "Untitled")
            badge = item.get(self.config.card_badge_key, "") if self.config.card_badge_key else ""

            border_top = "border-top: 1px solid #e5e7eb;" if i > 0 else ""
            badge_html = ""
            if badge:
                badge_color = self._get_status_color(badge)
                badge_html = f'<span style="color: {badge_color}; font-size: 12px; font-weight: 600;">{badge}</span>'

            items_html += f'''
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 16px;
                {border_top}
                cursor: pointer;
            " onmouseover="this.style.backgroundColor='#f9fafb'"
               onmouseout="this.style.backgroundColor='white'">
                <span style="color: #111827;">{title}</span>
                {badge_html}
            </div>
            '''

        items_html += '</div>'
        return gr.HTML(items_html)

    def _get_status_color(self, status: str) -> str:
        """Get color for status badge."""
        status_colors = {
            "open": "#ef4444",
            "in_progress": "#f59e0b",
            "in progress": "#f59e0b",
            "resolved": "#22c55e",
            "closed": "#6b7280",
            "p1": "#dc2626",
            "p2": "#ea580c",
            "p3": "#ca8a04",
            "p4": "#6b7280",
        }
        return status_colors.get(status.lower(), "#6b7280")
