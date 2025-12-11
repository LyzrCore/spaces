"""
Mock orchestrator for blueprint agent simulation.

Simulates multi-agent orchestration without actual LLM calls.
Generates contextual responses based on input patterns.
"""

import random
import time
from dataclasses import dataclass, field
from typing import Generator


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    role: str
    triggers: list[str] = field(default_factory=list)  # Keywords that activate this agent


@dataclass
class BlueprintConfig:
    """Configuration for a blueprint."""
    id: str
    name: str
    domain: str
    manager: AgentConfig
    workers: list[AgentConfig] = field(default_factory=list)


class MockOrchestrator:
    """
    Mock orchestrator that simulates blueprint agent processing.

    Generates realistic responses based on input patterns without
    making actual LLM API calls.
    """

    def __init__(self, blueprint: BlueprintConfig | dict):
        if isinstance(blueprint, dict):
            # Convert nested configs
            manager = blueprint.get("manager", {})
            if isinstance(manager, dict):
                manager = AgentConfig(**manager)

            workers = blueprint.get("workers", [])
            workers = [
                AgentConfig(**w) if isinstance(w, dict) else w
                for w in workers
            ]

            self.blueprint = BlueprintConfig(
                id=blueprint.get("id", ""),
                name=blueprint.get("name", ""),
                domain=blueprint.get("domain", ""),
                manager=manager,
                workers=workers,
            )
        else:
            self.blueprint = blueprint

        # Response templates by domain
        self._response_generators = {
            "it_operations": self._generate_it_response,
            "customer_service": self._generate_support_response,
            "default": self._generate_default_response,
        }

    def process(self, input_data: dict) -> dict:
        """
        Process input through simulated agent orchestration.

        Args:
            input_data: User input from form

        Returns:
            Structured response based on blueprint domain
        """
        # Get appropriate response generator
        generator = self._response_generators.get(
            self.blueprint.domain,
            self._response_generators["default"]
        )

        return generator(input_data)

    def process_stream(self, input_data: dict) -> Generator[dict, None, None]:
        """
        Process with streaming progress updates.

        Yields:
            Progress updates and final result
        """
        # Manager analyzing
        yield {
            "stage": "analyzing",
            "agent": self.blueprint.manager.name,
            "message": "Analyzing your request...",
        }
        time.sleep(0.5)

        # Determine which workers to involve
        relevant_workers = self._get_relevant_workers(input_data)

        # Workers processing
        for worker in relevant_workers:
            yield {
                "stage": "processing",
                "agent": worker.name,
                "message": f"Processing: {worker.role}",
            }
            time.sleep(0.3)

        # Manager synthesizing
        yield {
            "stage": "synthesizing",
            "agent": self.blueprint.manager.name,
            "message": "Synthesizing results...",
        }
        time.sleep(0.3)

        # Final result
        result = self.process(input_data)
        yield {
            "stage": "complete",
            "result": result,
        }

    def _get_relevant_workers(self, input_data: dict) -> list[AgentConfig]:
        """Determine which workers should process this input."""
        text = " ".join(str(v).lower() for v in input_data.values())

        relevant = []
        for worker in self.blueprint.workers:
            # Check if any trigger keywords match
            if any(trigger.lower() in text for trigger in worker.triggers):
                relevant.append(worker)

        # If no specific matches, use all workers
        if not relevant:
            relevant = self.blueprint.workers[:3]  # Limit to 3

        return relevant

    def _generate_it_response(self, input_data: dict) -> dict:
        """Generate IT incident response."""
        title = input_data.get("title", "Incident")
        description = input_data.get("description", "").lower()
        system = input_data.get("affected_system", "Unknown System")

        # Determine severity based on keywords
        severity = self._determine_severity(description)

        # Generate incident ID
        incident_id = f"INC-{random.randint(1000, 9999)}"

        # Generate timeline
        timeline = self._generate_it_timeline(description)

        # Generate root cause
        root_cause = self._generate_root_cause(description)

        # Generate resolution
        resolution = self._generate_resolution(description)

        return {
            "incident_id": incident_id,
            "title": title,
            "status": "In Progress",
            "severity": severity,
            "affected_system": system,
            "assigned_to": "On-Call Team",
            "timeline": timeline,
            "root_cause": root_cause,
            "resolution": resolution,
            "recommendations": [
                "Monitor system metrics for the next 24 hours",
                "Schedule post-incident review",
                "Update runbook with findings",
            ],
        }

    def _determine_severity(self, description: str) -> str:
        """Determine incident severity from description."""
        critical_keywords = ["down", "outage", "critical", "production", "100%", "all users"]
        high_keywords = ["slow", "degraded", "high cpu", "high memory", "timeout"]
        medium_keywords = ["intermittent", "some users", "error rate"]

        if any(kw in description for kw in critical_keywords):
            return "P1 - Critical"
        elif any(kw in description for kw in high_keywords):
            return "P2 - High"
        elif any(kw in description for kw in medium_keywords):
            return "P3 - Medium"
        else:
            return "P4 - Low"

    def _generate_it_timeline(self, description: str) -> list[dict]:
        """Generate incident timeline."""
        events = [
            {"time": "00:00", "event": "Incident reported", "agent": "System Monitoring"},
            {"time": "00:02", "event": "Alert triaged and severity assigned", "agent": "Alert Triage"},
            {"time": "00:05", "event": "Investigation started", "agent": "Root Cause Analysis"},
        ]

        if "cpu" in description or "memory" in description:
            events.append({"time": "00:08", "event": "Resource exhaustion detected", "agent": "System Monitoring"})
            events.append({"time": "00:12", "event": "Scaling remediation initiated", "agent": "Root Cause Analysis"})

        if "deploy" in description or "release" in description:
            events.append({"time": "00:08", "event": "Recent deployment identified", "agent": "Root Cause Analysis"})
            events.append({"time": "00:10", "event": "Rollback initiated", "agent": "Escalation Coordinator"})

        events.append({"time": "00:15", "event": "Resolution in progress", "agent": "Incident Coordinator"})

        return events

    def _generate_root_cause(self, description: str) -> str:
        """Generate root cause analysis."""
        if "cpu" in description:
            return "Root cause identified as CPU exhaustion due to inefficient query processing in the database layer. The query optimizer failed to use the correct index, causing full table scans under high load."
        elif "memory" in description:
            return "Memory leak detected in the application service. The connection pool was not properly releasing connections, leading to gradual memory exhaustion over time."
        elif "deploy" in description or "release" in description:
            return "Issue traced to recent deployment (v2.3.1). A configuration change in the service mesh caused intermittent connection failures between microservices."
        elif "timeout" in description:
            return "Timeout caused by database connection pool exhaustion. The connection limit was reached due to long-running transactions not being properly closed."
        elif "error" in description:
            return "Error spike caused by upstream API rate limiting. The external service began rejecting requests after exceeding the quota limit."
        else:
            return "Investigation identified the root cause as a configuration drift between environments. The production configuration was missing critical environment variables added in the last release."

    def _generate_resolution(self, description: str) -> str:
        """Generate resolution steps."""
        if "cpu" in description:
            return "1. Added missing database index\n2. Optimized query patterns\n3. Increased connection pool size\n4. Deployed hotfix to production"
        elif "memory" in description:
            return "1. Identified leaking connections\n2. Applied connection pool fix\n3. Restarted affected services\n4. Verified memory stabilization"
        elif "deploy" in description:
            return "1. Initiated rollback to v2.3.0\n2. Verified service connectivity\n3. Confirmed user impact resolved\n4. Scheduled hotfix for configuration issue"
        else:
            return "1. Identified affected components\n2. Applied configuration fix\n3. Verified system stability\n4. Confirmed resolution with monitoring"

    def _generate_support_response(self, input_data: dict) -> dict:
        """Generate customer support response."""
        query = input_data.get("query", input_data.get("description", ""))

        return {
            "ticket_id": f"TKT-{random.randint(1000, 9999)}",
            "status": "Resolved",
            "response": "Thank you for reaching out. Based on your inquiry, here's what we found...",
            "category": "General Inquiry",
            "resolution_time": "15 minutes",
        }

    def _generate_default_response(self, input_data: dict) -> dict:
        """Generate default response for unknown domains."""
        return {
            "status": "Processed",
            "message": "Your request has been processed successfully.",
            "input_received": input_data,
        }
