"""Configuration for IT Service Desk demo app."""

# Support both local and HF Spaces imports
try:
    from apps.shared.orchestrator import MockOrchestrator
    from apps.it_service_desk.mock_data import SAMPLE_INCIDENTS, get_dashboard_stats
except ImportError:
    from shared.orchestrator import MockOrchestrator
    from mock_data import SAMPLE_INCIDENTS, get_dashboard_stats


# Blueprint configuration for IT Incident Response
IT_INCIDENT_BLUEPRINT = {
    "id": "it-incident-response",
    "name": "IT Incident Response",
    "domain": "it_operations",
    "manager": {
        "name": "Incident Coordinator",
        "role": "Orchestrates incident response workflow",
        "triggers": [],
    },
    "workers": [
        {
            "name": "System Monitoring",
            "role": "Monitors system health and detects anomalies",
            "triggers": ["cpu", "memory", "disk", "performance", "slow", "high"],
        },
        {
            "name": "Alert Triage",
            "role": "Triages alerts and assigns severity",
            "triggers": ["alert", "critical", "urgent", "priority"],
        },
        {
            "name": "Root Cause Analysis",
            "role": "Investigates and identifies root cause",
            "triggers": ["error", "failure", "bug", "issue", "cause"],
        },
        {
            "name": "Escalation Coordinator",
            "role": "Manages escalations and notifications",
            "triggers": ["escalate", "notify", "team", "urgent"],
        },
    ],
}

# Create orchestrator instance
orchestrator = MockOrchestrator(IT_INCIDENT_BLUEPRINT)

# App configuration
APP_CONFIG = {
    "id": "it_service_desk",
    "title": "IT Service Desk",
    "description": "Incident Management System powered by AI Agent Orchestration",

    # Header links
    "github_url": "https://github.com/LyzrCore/spaces",
    "studio_url": "https://studio.lyzr.ai/blueprints",
    "readme_url": "https://github.com/LyzrCore/spaces#readme",

    # Entity naming
    "entity_name": "incident",
    "entity_name_plural": "incidents",

    # Sidebar navigation
    "sidebar": [
        {"label": "Dashboard", "path": "/", "icon": "📊"},
        {"label": "Incidents", "path": "/incidents", "icon": "🎫"},
        {"label": "New Incident", "path": "/new", "icon": "➕"},
    ],

    # Pages configuration
    "pages": {
        "/": {
            "page": "dashboard",
            "variant": "metrics",
            "data_key": "dashboard",
            "config": {
                "title": "Overview",
                "stats": [
                    {"label": "Open", "value_key": "open_count", "icon": "🔴", "color": "red"},
                    {"label": "In Progress", "value_key": "in_progress_count", "icon": "🟡", "color": "yellow"},
                    {"label": "Resolved", "value_key": "resolved_count", "icon": "🟢", "color": "green"},
                    {"label": "Total", "value_key": "total_count", "icon": "📋", "color": "blue"},
                ],
                "recent_items_key": "recent_items",
                "recent_items_title": "Recent Incidents",
            },
        },
        "/incidents": {
            "page": "list",
            "variant": "table",
            "data_key": "incidents",
            "config": {
                "title": "All Incidents",
                "columns": [
                    {"key": "id", "label": "ID", "width": "100px"},
                    {"key": "title", "label": "Title"},
                    {"key": "severity", "label": "Severity", "type": "badge"},
                    {"key": "status", "label": "Status", "type": "badge"},
                    {"key": "assigned_to", "label": "Assigned To"},
                    {"key": "created_at", "label": "Created"},
                ],
                "empty_title": "No incidents",
                "empty_description": "All systems operational!",
            },
        },
        "/new": {
            "page": "form",
            "variant": "standard",
            "config": {
                "title": "Report New Incident",
                "description": "Describe the issue and our AI agents will analyze, triage, and provide resolution guidance.",
                "fields": [
                    {
                        "key": "title",
                        "label": "Incident Title",
                        "type": "text",
                        "placeholder": "Brief description of the issue",
                        "required": True,
                    },
                    {
                        "key": "description",
                        "label": "Description",
                        "type": "textarea",
                        "placeholder": "Detailed description of the incident. Include error messages, affected users, timeline, etc.",
                        "rows": 5,
                        "required": True,
                    },
                    {
                        "key": "affected_system",
                        "label": "Affected System",
                        "type": "select",
                        "options": [
                            "API Gateway",
                            "Auth Service",
                            "Database",
                            "Infrastructure",
                            "Analytics",
                            "Email Service",
                            "Other",
                        ],
                        "required": True,
                    },
                ],
                "submit_label": "Submit Incident",
                "processing_label": "Analyzing incident...",
            },
        },
    },

    # Data sources
    "data": {
        "incidents": SAMPLE_INCIDENTS,
        "dashboard": get_dashboard_stats(),
    },

    # Orchestrator
    "orchestrator": orchestrator,
}
