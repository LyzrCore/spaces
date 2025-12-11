"""
IT Service Desk - Incident Management Demo App.

This app demonstrates the IT Incident Response blueprint
with AI-powered incident analysis, triage, and resolution.
"""

import sys
from pathlib import Path

# Add project root to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Support both local and HF Spaces imports
try:
    from apps.shared.engine import DemoApp
    from apps.it_service_desk.config import APP_CONFIG
    from config.settings import LOCAL_PORTS, is_dev_mode
except ImportError:
    from shared.engine import DemoApp
    from config import APP_CONFIG
    # Default for HF Spaces
    def is_dev_mode():
        return False
    LOCAL_PORTS = {}


# Build the app from configuration
app = DemoApp(APP_CONFIG)

if __name__ == "__main__":
    demo = app.build()

    if is_dev_mode():
        demo.launch(server_port=LOCAL_PORTS.get("it_service_desk", 7862))
    else:
        demo.launch()
