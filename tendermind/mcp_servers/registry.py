import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from tendermind.models.mcp_types import (
    MCPToolDefinition, MCPCallRequest, MCPCallResponse, AgentTraceEntry
)
from tendermind.mcp_servers.tender_server import TenderMCPServer
from tendermind.mcp_servers.document_server import DocumentMCPServer
from tendermind.mcp_servers.business_server import BusinessMCPServer
from tendermind.mcp_servers.eligibility_server import EligibilityMCPServer
from tendermind.mcp_servers.bid_server import BidMCPServer
from tendermind.mcp_servers.monitoring_server import MonitoringMCPServer
from tendermind.mcp_servers.communication_server import CommunicationMCPServer
from tendermind.data.db import db

class MCPRegistry:
    """
    Central Registry for all TenderMind MCP Servers.
    Orchestrates cross-server discovery, invocation, parameter validation,
    and maintains auditable AI Agent Activity traces (Screen 7).
    """

    def __init__(self):
        self.servers = {
            "TenderMCPServer": TenderMCPServer(),
            "DocumentMCPServer": DocumentMCPServer(),
            "BusinessMCPServer": BusinessMCPServer(),
            "EligibilityMCPServer": EligibilityMCPServer(),
            "BidMCPServer": BidMCPServer(),
            "MonitoringMCPServer": MonitoringMCPServer(),
            "CommunicationMCPServer": CommunicationMCPServer()
        }

    def list_all_tools(self) -> List[MCPToolDefinition]:
        all_tools = []
        for s in self.servers.values():
            all_tools.extend(s.list_tools())
        return all_tools

    def find_server_for_tool(self, tool_name: str) -> Optional[str]:
        for s_name, s in self.servers.items():
            if tool_name in s.tools:
                return s_name
        return None

    def execute_tool(self, server_name: str, tool_name: str,
                     arguments: Dict[str, Any], agent_name: str = "TenderMind Orchestrator",
                     requires_approval: bool = False, approved: bool = True) -> MCPCallResponse:
        if server_name not in self.servers:
            # Fallback to finding by tool name
            alt_server = self.find_server_for_tool(tool_name)
            if alt_server:
                server_name = alt_server
            else:
                return MCPCallResponse(
                    success=False,
                    server_name=server_name,
                    tool_name=tool_name,
                    error=f"MCP Server '{server_name}' is not registered."
                )

        server = self.servers[server_name]
        response = server.invoke_tool(tool_name, arguments)

        # Log trace in database for Screen 7 inspection
        summary = ""
        if response.success:
            if isinstance(response.result, dict):
                keys = list(response.result.keys())[:3]
                summary = f"Success: retrieved {', '.join(keys)}..."
            elif isinstance(response.result, list):
                summary = f"Success: {len(response.result)} records retrieved."
            else:
                summary = f"Success: {str(response.result)[:100]}"
        else:
            summary = f"Failed: {response.error}"

        trace = AgentTraceEntry(
            trace_id=str(uuid.uuid4())[:8],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            agent_name=agent_name,
            mcp_server=server_name,
            tool_called=tool_name,
            parameters=arguments,
            summary_result=summary,
            status="SUCCESS" if response.success else "FAILED",
            requires_human_approval=requires_approval,
            approved=approved
        )
        db.add_trace(trace)

        return response

mcp_registry = MCPRegistry()
