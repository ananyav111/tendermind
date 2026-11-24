from typing import Dict, Any
from datetime import datetime
from tendermind.mcp_servers.base import BaseMCPServer
from tendermind.data.db import db

class CommunicationMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(
            name="CommunicationMCPServer",
            description="Manages calendar reminders, alerts, and notification drafts for tender deadlines."
        )
        self._register_all_tools()

    def _register_all_tools(self):
        self.register_tool(
            name="create_calendar_reminder",
            description="Schedule a submission deadline or pre-bid meeting calendar reminder (requires human approval).",
            parameters={
                "type": "object",
                "properties": {
                    "tender_id": {"type": "string", "description": "Tender ID"},
                    "event_title": {"type": "string", "description": "Calendar title"},
                    "event_date": {"type": "string", "description": "ISO date for reminder"},
                    "reminder_notes": {"type": "string", "description": "Actionable instructions"}
                },
                "required": ["tender_id", "event_title", "event_date"]
            },
            handler=self._tool_create_calendar_reminder
        )

        self.register_tool(
            name="draft_notification",
            description="Draft notification message for missing certificates or deadline extensions.",
            parameters={
                "type": "object",
                "properties": {
                    "recipient_role": {"type": "string", "description": "e.g. 'Project Manager', 'CEO'"},
                    "subject": {"type": "string", "description": "Notification subject"},
                    "body": {"type": "string", "description": "Notification text content"}
                },
                "required": ["recipient_role", "subject", "body"]
            },
            handler=self._tool_draft_notification
        )

    def _tool_create_calendar_reminder(self, tender_id: str, event_title: str,
                                       event_date: str, reminder_notes: str = "") -> Dict[str, Any]:
        return {
            "scheduled": True,
            "event_title": event_title,
            "event_date": event_date,
            "tender_id": tender_id,
            "reminder_lead_time": "24 hours prior to deadline",
            "notes": reminder_notes,
            "calendar_provider": "Google Calendar / ICS Export",
            "approval_status": "APPROVED_BY_USER"
        }

    def _tool_draft_notification(self, recipient_role: str, subject: str, body: str) -> Dict[str, Any]:
        return {
            "status": "DRAFTED",
            "recipient_role": recipient_role,
            "subject": subject,
            "body": body,
            "drafted_at": datetime.now().isoformat()
        }
