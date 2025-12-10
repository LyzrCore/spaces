# Lyzr Spaces

A monorepo for Gradio applications deployed to HuggingFace Spaces.

## Apps

| App | Local Port | Production URL |
|-----|------------|----------------|
| dashboard | 7860 | https://dashboard.lyzr.space |
| analytics | 7861 | https://analytics.lyzr.space |

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
APP_ENV=dev python apps/dashboard/app.py
```

## Project Structure

```
spaces/
├── apps/
│   ├── shared/          # Shared UI components
│   ├── dashboard/       # Dashboard app
│   └── analytics/       # Analytics app
├── config/
│   ├── app_registry.py  # App definitions
│   ├── settings.py      # Environment config
│   └── validator.py     # Registry validation
└── .github/workflows/   # CI/CD
```

## Deployment

Push to `main` → GitHub Actions deploys changed apps to HuggingFace Spaces.

Required secret: `HF_TOKEN`
