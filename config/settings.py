"""
Environment configuration and URL resolution.

Supports local development with localhost URLs and production with lyzr.space URLs.
"""

import os

# Environment: "dev" for local development, "prod" for production
ENVIRONMENT = os.getenv("APP_ENV", "prod")

# Local development port mappings
LOCAL_PORTS: dict[str, int] = {
    "dashboard": 7860,
    "analytics": 7861,
    "it_service_desk": 7862,
}


def get_app_url(app_id: str) -> str | None:
    """
    Get the URL for an app based on current environment.

    In dev mode: returns localhost URL with assigned port
    In prod mode: returns lyzr.space URL from registry
    """
    from config.app_registry import APPS_REGISTRY

    if ENVIRONMENT == "dev":
        port = LOCAL_PORTS.get(app_id)
        if port:
            return f"http://localhost:{port}"
        return None

    # Production mode - use registry URL
    app_info = APPS_REGISTRY.get(app_id)
    if app_info:
        return app_info.get("url")
    return None


def is_dev_mode() -> bool:
    """Check if running in development mode."""
    return ENVIRONMENT == "dev"


def is_prod_mode() -> bool:
    """Check if running in production mode."""
    return ENVIRONMENT == "prod"
