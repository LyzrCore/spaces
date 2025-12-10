"""
Registry Validator - Ensures app registry integrity.

Validates:
- Required keys exist for each app
- URLs are unique
- HF space names are unique
"""

REQUIRED_KEYS = ["name", "hf_space", "url", "description"]


class RegistryValidationError(Exception):
    """Raised when registry validation fails."""
    pass


def validate_required_keys(registry: dict[str, dict]) -> list[str]:
    """Check that all apps have required keys."""
    errors = []
    for app_id, app_info in registry.items():
        for key in REQUIRED_KEYS:
            if key not in app_info:
                errors.append(f"App '{app_id}' missing required key: '{key}'")
    return errors


def validate_unique_urls(registry: dict[str, dict]) -> list[str]:
    """Check that URLs are unique."""
    errors = []
    urls_seen: dict[str, str] = {}

    for app_id, app_info in registry.items():
        url = app_info.get("url")
        if url in urls_seen:
            errors.append(f"Duplicate URL '{url}' for apps: '{urls_seen[url]}' and '{app_id}'")
        else:
            urls_seen[url] = app_id

    return errors


def validate_unique_hf_spaces(registry: dict[str, dict]) -> list[str]:
    """Check that HF space names are unique."""
    errors = []
    spaces_seen: dict[str, str] = {}

    for app_id, app_info in registry.items():
        hf_space = app_info.get("hf_space")
        if hf_space in spaces_seen:
            errors.append(f"Duplicate HF space '{hf_space}' for apps: '{spaces_seen[hf_space]}' and '{app_id}'")
        else:
            spaces_seen[hf_space] = app_id

    return errors


def validate_registry(registry: dict[str, dict] | None = None) -> None:
    """
    Run all validation checks on the registry.

    Raises RegistryValidationError if any validation fails.
    """
    if registry is None:
        from config.app_registry import APPS_REGISTRY
        registry = APPS_REGISTRY

    all_errors: list[str] = []

    all_errors.extend(validate_required_keys(registry))
    all_errors.extend(validate_unique_urls(registry))
    all_errors.extend(validate_unique_hf_spaces(registry))

    if all_errors:
        error_msg = "Registry validation failed:\n" + "\n".join(f"  - {e}" for e in all_errors)
        raise RegistryValidationError(error_msg)


if __name__ == "__main__":
    try:
        validate_registry()
        print("Registry validation passed!")
    except RegistryValidationError as e:
        print(e)
        exit(1)
