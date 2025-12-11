"""Badge components for status and severity display."""

import gradio as gr


def StatusBadge(status: str, status_colors: dict | None = None) -> gr.HTML:
    """
    Render a colored status badge.

    Args:
        status: Status text (e.g., "open", "in_progress", "resolved")
        status_colors: Optional dict mapping status to colors
    """
    default_colors = {
        "open": "#ef4444",
        "in_progress": "#f59e0b",
        "in progress": "#f59e0b",
        "resolved": "#22c55e",
        "closed": "#6b7280",
    }
    colors = status_colors or default_colors
    color = colors.get(status.lower(), "#6b7280")

    html = f'''
    <span style="
        background-color: {color}20;
        color: {color};
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    ">{status}</span>
    '''
    return gr.HTML(html)


def SeverityBadge(severity: str) -> gr.HTML:
    """
    Render a severity badge (P1-P4).

    Args:
        severity: Severity level (e.g., "P1", "P2", "P3", "P4")
    """
    severity_colors = {
        "p1": "#dc2626",
        "p1 - critical": "#dc2626",
        "critical": "#dc2626",
        "p2": "#ea580c",
        "p2 - high": "#ea580c",
        "high": "#ea580c",
        "p3": "#ca8a04",
        "p3 - medium": "#ca8a04",
        "medium": "#ca8a04",
        "p4": "#6b7280",
        "p4 - low": "#6b7280",
        "low": "#6b7280",
    }
    color = severity_colors.get(severity.lower(), "#6b7280")

    html = f'''
    <span style="
        background-color: {color};
        color: white;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 700;
    ">{severity.upper()}</span>
    '''
    return gr.HTML(html)
