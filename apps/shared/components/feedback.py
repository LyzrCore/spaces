"""Feedback components for user interaction."""

import gradio as gr


def ProcessingIndicator(steps: list[dict], current_step: int = 0) -> gr.HTML:
    """
    Render a processing indicator with steps.

    Args:
        steps: List of {"label": str, "status": "pending"|"active"|"complete"}
        current_step: Index of current step
    """
    html = '<div style="padding: 16px;">'
    for i, step in enumerate(steps):
        if i < current_step:
            icon = "✓"
            color = "#22c55e"
        elif i == current_step:
            icon = "●"
            color = "#3b82f6"
        else:
            icon = "○"
            color = "#9ca3af"

        html += f'''
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="color: {color}; margin-right: 8px; font-size: 16px;">{icon}</span>
            <span style="color: {'#111827' if i <= current_step else '#9ca3af'};">{step["label"]}</span>
        </div>
        '''
    html += '</div>'
    return gr.HTML(html)


def EmptyState(
    title: str,
    description: str | None = None,
    icon: str = "📭",
) -> None:
    """
    Render an empty state message.

    Args:
        title: Empty state title
        description: Optional description
        icon: Emoji icon
    """
    gr.HTML(f'''
    <div style="
        text-align: center;
        padding: 48px 24px;
        color: #6b7280;
    ">
        <div style="font-size: 48px; margin-bottom: 16px;">{icon}</div>
        <div style="font-size: 18px; font-weight: 600; color: #374151; margin-bottom: 8px;">{title}</div>
        {f'<div style="font-size: 14px;">{description}</div>' if description else ''}
    </div>
    ''')
