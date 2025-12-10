# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monorepo for Gradio apps deployed to HuggingFace Spaces under the `lyzr-ai` org. Each app runs at `https://<app-id>.lyzr.space`.

## Commands

```bash
# Run an app locally
APP_ENV=dev python apps/<app-id>/app.py

# Validate the app registry
PYTHONPATH=. python config/validator.py

# Create a new HF Space
huggingface-cli repo create --repo-type=space --space-sdk=gradio <app-id>
```

## Architecture

### App Structure
Apps extend `AppBase` from `apps/shared/custom_components.py`, which provides:
- Automatic header/footer via `create_header()` and `create_footer()`
- Navigation links to other apps via registry lookup
- Registry validation on instantiation

Each app must implement `build() -> gr.Blocks` and call the parent layout methods.

### Configuration System
- `config/app_registry.py`: Central `APPS_REGISTRY` dict with app metadata (name, hf_space, url, description)
- `config/settings.py`: Environment detection (`APP_ENV=dev|prod`) and `LOCAL_PORTS` mapping
- `config/validator.py`: Validates registry has required keys and no duplicate URLs/spaces

### URL Resolution
`settings.get_app_url(app_id)` returns localhost URLs in dev mode, production URLs in prod mode. This enables cross-app navigation to work both locally and in production.

## Adding a New App

1. Add entry to `APPS_REGISTRY` in `config/app_registry.py`
2. Add port to `LOCAL_PORTS` in `config/settings.py`
3. Create `apps/<app-id>/app.py` extending `AppBase`
4. Create `apps/<app-id>/requirements.txt` with `-r ../../requirements.txt`
5. Add deploy job to `.github/workflows/deploy.yml` (copy existing job pattern)
6. Add output to `detect-changes` job in workflow

## CI/CD

- Push to `main` triggers deployment of changed apps only
- Changes to `apps/shared/`, `config/`, or `requirements.txt` trigger deployment of all apps
- Files over 10MB will fail (HF Spaces limit)
- Required secret: `HF_TOKEN`

## Roadmap

- [ ] Custom domains (`<app-id>.lyzr.space`) - configure after validating end-to-end deployment
