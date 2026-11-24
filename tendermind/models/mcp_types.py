from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MCPToolDefinition(BaseModel):
    name: str
    description: str
    server_name: str
    parameters: Dict[str, Any]

class MCPCallRequest(BaseModel):
    server_name: str
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)

class MCPCallResponse(BaseModel):
    success: bool
    server_name: str
    tool_name: str
    result: Any = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0

class AgentTraceEntry(BaseModel):
    trace_id: str
    timestamp: str
    agent_name: str
    mcp_server: str
    tool_called: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    summary_result: str
    status: str = "SUCCESS"  # "SUCCESS", "WAITING_APPROVAL", "FAILED"
    requires_human_approval: bool = False
    approved: bool = True
