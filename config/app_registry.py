"""
App Registry - Single source of truth for all apps in the ecosystem.

Each app entry contains:
- name: Display name
- hf_space: HuggingFace space identifier (lyzr-ai/<app_id>)
- url: Production URL (https://<app_id>.lyzr.space)
- description: Brief description of the app
"""

APPS_REGISTRY: dict[str, dict] = {
    "dashboard": {
        "name": "Dashboard",
        "hf_space": "lyzr-ai/dashboard",
        "url": "https://dashboard.lyzr.space",
        "description": "Main dashboard for the Lyzr ecosystem",
    },
    "analytics": {
        "name": "Analytics",
        "hf_space": "lyzr-ai/analytics",
        "url": "https://analytics.lyzr.space",
        "description": "View and analyze your data",
    },
    "it_service_desk": {
        "name": "IT Service Desk",
        "hf_space": "lyzr-ai/it-service-desk",
        "url": "https://it-service-desk.lyzr.space",
        "description": "AI-powered Incident Management System",
    },
}


def get_app_info(app_id: str) -> dict | None:
    """Get full info for an app by its ID."""
    return APPS_REGISTRY.get(app_id)


def get_all_apps() -> list[str]:
    """Get list of all app IDs."""
    return list(APPS_REGISTRY.keys())


def get_app_url(app_id: str) -> str | None:
    """Get the URL for an app."""
    app = APPS_REGISTRY.get(app_id)
    if app:
        return app.get("url")
    return None
