"""Form page template with variants: standard, wizard."""

import gradio as gr
from typing import Callable, Generator
from dataclasses import dataclass, field


@dataclass
class FieldConfig:
    """Configuration for a form field."""
    key: str
    label: str
    type: str = "text"  # text, textarea, select, number
    placeholder: str = ""
    required: bool = False
    options: list[str] | None = None  # For select
    rows: int = 3  # For textarea


@dataclass
class FormPageConfig:
    """Configuration for FormPage."""
    variant: str = "standard"  # standard, wizard
    title: str = "Submit"
    description: str | None = None
    fields: list[FieldConfig] = field(default_factory=list)
    submit_label: str = "Submit"
    processing_label: str = "Processing..."


class FormPage:
    """
    Form page template for user input.

    Variants:
        - standard: Single-column form
        - wizard: Multi-step form (future)
    """

    def __init__(self, config: FormPageConfig | dict):
        if isinstance(config, dict):
            # Convert fields if present
            if "fields" in config and config["fields"]:
                config["fields"] = [
                    FieldConfig(**f) if isinstance(f, dict) else f
                    for f in config["fields"]
                ]
            self.config = FormPageConfig(**config)
        else:
            self.config = config

        self._field_components: dict[str, gr.Component] = {}

    def render(
        self,
        on_submit: Callable[[dict], Generator | dict] | None = None,
    ) -> tuple[gr.Button, dict[str, gr.Component], gr.Column]:
        """
        Render the form page.

        Args:
            on_submit: Callback when form is submitted

        Returns:
            Tuple of (submit_button, field_components, result_container)
        """
        if self.config.title:
            gr.Markdown(f"## {self.config.title}")

        if self.config.description:
            gr.Markdown(self.config.description)

        # Render fields
        self._field_components = {}
        for field_config in self.config.fields:
            self._field_components[field_config.key] = self._render_field(field_config)

        # Submit button
        submit_btn = gr.Button(
            self.config.submit_label,
            variant="primary",
            size="lg",
        )

        # Result container (for showing processing + results)
        with gr.Column(visible=False) as result_container:
            processing_indicator = gr.HTML("")
            result_output = gr.Markdown("")

        return submit_btn, self._field_components, result_container, processing_indicator, result_output

    def _render_field(self, field_config: FieldConfig) -> gr.Component:
        """Render a single form field."""
        label = field_config.label
        if field_config.required:
            label += " *"

        if field_config.type == "text":
            return gr.Textbox(
                label=label,
                placeholder=field_config.placeholder,
                lines=1,
            )
        elif field_config.type == "textarea":
            return gr.Textbox(
                label=label,
                placeholder=field_config.placeholder,
                lines=field_config.rows,
            )
        elif field_config.type == "select":
            return gr.Dropdown(
                label=label,
                choices=field_config.options or [],
                value=None,
            )
        elif field_config.type == "number":
            return gr.Number(
                label=label,
            )
        else:
            return gr.Textbox(
                label=label,
                placeholder=field_config.placeholder,
            )

    def get_field_values(self) -> list[gr.Component]:
        """Get list of field components for inputs."""
        return list(self._field_components.values())

    def get_field_keys(self) -> list[str]:
        """Get list of field keys."""
        return list(self._field_components.keys())


def create_processing_html(steps: list[dict]) -> str:
    """
    Create HTML for processing indicator.

    Args:
        steps: List of {"label": str, "status": "pending"|"active"|"complete"}
    """
    html = '<div style="padding: 16px; background: #f9fafb; border-radius: 8px; margin-top: 16px;">'
    html += '<div style="font-weight: 600; margin-bottom: 12px;">Processing your request...</div>'

    for step in steps:
        status = step.get("status", "pending")
        label = step.get("label", "")

        if status == "complete":
            icon = "✓"
            color = "#22c55e"
            text_color = "#111827"
        elif status == "active":
            icon = "●"
            color = "#3b82f6"
            text_color = "#111827"
        else:
            icon = "○"
            color = "#9ca3af"
            text_color = "#9ca3af"

        html += f'''
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <span style="color: {color}; margin-right: 8px; font-size: 14px;">{icon}</span>
            <span style="color: {text_color}; font-size: 14px;">{label}</span>
        </div>
        '''

    html += '</div>'
    return html
