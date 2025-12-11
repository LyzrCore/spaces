"""Mock data for IT Service Desk demo."""

SAMPLE_INCIDENTS = [
    {
        "id": "INC-1001",
        "title": "Production API High Latency",
        "description": "API response times exceeding 5 seconds, affecting checkout flow",
        "status": "Resolved",
        "severity": "P1",
        "affected_system": "API Gateway",
        "assigned_to": "Platform Team",
        "created_at": "2024-01-15 10:15:00",
        "resolved_at": "2024-01-15 10:45:00",
        "root_cause": "Database connection pool exhausted due to connection leak in v2.3.1",
        "resolution": "Rolled back to v2.3.0 and applied hotfix for connection handling",
        "timeline": [
            {"time": "10:15", "event": "Alert triggered: API latency > 5s", "agent": "Monitoring"},
            {"time": "10:17", "event": "Triaged as P1 - Critical", "agent": "Triage"},
            {"time": "10:22", "event": "Identified DB connection exhaustion", "agent": "RCA"},
            {"time": "10:35", "event": "Rollback initiated", "agent": "Escalation"},
            {"time": "10:45", "event": "Service restored", "agent": "Coordinator"},
        ],
    },
    {
        "id": "INC-1002",
        "title": "Login Authentication Failures",
        "description": "Users unable to login, OAuth token validation failing",
        "status": "In Progress",
        "severity": "P2",
        "affected_system": "Auth Service",
        "assigned_to": "Security Team",
        "created_at": "2024-01-15 14:30:00",
        "timeline": [
            {"time": "14:30", "event": "Multiple login failure reports", "agent": "Monitoring"},
            {"time": "14:32", "event": "Triaged as P2 - High", "agent": "Triage"},
            {"time": "14:40", "event": "Investigating OAuth provider", "agent": "RCA"},
        ],
    },
    {
        "id": "INC-1003",
        "title": "Slow Dashboard Loading",
        "description": "Analytics dashboard taking 30+ seconds to load",
        "status": "Open",
        "severity": "P3",
        "affected_system": "Analytics",
        "assigned_to": "Data Team",
        "created_at": "2024-01-15 16:00:00",
        "timeline": [
            {"time": "16:00", "event": "Performance degradation detected", "agent": "Monitoring"},
            {"time": "16:05", "event": "Triaged as P3 - Medium", "agent": "Triage"},
        ],
    },
    {
        "id": "INC-1004",
        "title": "Email Notifications Delayed",
        "description": "Transactional emails being delayed by 15-20 minutes",
        "status": "Resolved",
        "severity": "P3",
        "affected_system": "Email Service",
        "assigned_to": "Platform Team",
        "created_at": "2024-01-14 09:00:00",
        "resolved_at": "2024-01-14 11:30:00",
        "root_cause": "Email queue backlog due to rate limiting from provider",
        "resolution": "Increased queue workers and implemented retry logic",
    },
    {
        "id": "INC-1005",
        "title": "Memory Usage Spike on Worker Nodes",
        "description": "Kubernetes worker nodes showing 95% memory usage",
        "status": "Resolved",
        "severity": "P2",
        "affected_system": "Infrastructure",
        "assigned_to": "SRE Team",
        "created_at": "2024-01-13 22:00:00",
        "resolved_at": "2024-01-13 23:15:00",
        "root_cause": "Memory leak in cache invalidation service",
        "resolution": "Patched service and scaled horizontally",
    },
]


def get_dashboard_stats() -> dict:
    """Calculate dashboard statistics from incidents."""
    open_count = sum(1 for i in SAMPLE_INCIDENTS if i["status"] == "Open")
    in_progress = sum(1 for i in SAMPLE_INCIDENTS if i["status"] == "In Progress")
    resolved_count = sum(1 for i in SAMPLE_INCIDENTS if i["status"] == "Resolved")

    return {
        "open_count": open_count,
        "in_progress_count": in_progress,
        "resolved_count": resolved_count,
        "total_count": len(SAMPLE_INCIDENTS),
        "recent_items": SAMPLE_INCIDENTS[:5],
    }
