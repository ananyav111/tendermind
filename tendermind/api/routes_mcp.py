from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from tendermind.mcp_servers.registry import mcp_registry
from tendermind.models.mcp_types import MCPToolDefinition, MCPCallRequest, MCPCallResponse, AgentTraceEntry
from tendermind.data.db import db

router = APIRouter(prefix="/api/mcp", tags=["Model Context Protocol (MCP)"])

@router.get("/tools", response_model=List[MCPToolDefinition])
def list_mcp_tools():
    """Returns all registered MCP tools across the 7 independent servers."""
    return mcp_registry.list_all_tools()

@router.post("/invoke", response_model=MCPCallResponse)
def invoke_mcp_tool(req: MCPCallRequest = Body(...)):
    """Executes an MCP tool call through the registry and logs an auditable trace."""
    response = mcp_registry.execute_tool(
        server_name=req.server_name,
        tool_name=req.tool_name,
        arguments=req.arguments,
        agent_name="User Directed MCP Call"
    )
    return response

@router.get("/traces", response_model=List[AgentTraceEntry])
def get_agent_traces():
    """
    Returns live execution trace entries for Screen 7 (AI Agent Activity),
    showing which agent activated, MCP server called, tool used, results, and approval status.
    """
    return db.get_traces()
