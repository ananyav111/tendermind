import time
import inspect
from typing import Dict, Any, Callable, List, Optional
from tendermind.models.mcp_types import MCPToolDefinition, MCPCallResponse

class BaseMCPServer:
    """
    Base MCP (Model Context Protocol) Server implementation.
    Adheres to the official MCP tool schema and standard JSON-RPC execution interface.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.tools: Dict[str, Callable] = {}
        self.tool_definitions: Dict[str, MCPToolDefinition] = {}

    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], handler: Callable):
        self.tools[name] = handler
        self.tool_definitions[name] = MCPToolDefinition(
            name=name,
            description=description,
            server_name=self.name,
            parameters=parameters
        )

    def list_tools(self) -> List[MCPToolDefinition]:
        return list(self.tool_definitions.values())

    def invoke_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPCallResponse:
        if tool_name not in self.tools:
            return MCPCallResponse(
                success=False,
                server_name=self.name,
                tool_name=tool_name,
                error=f"Tool '{tool_name}' not found on server '{self.name}'"
            )

        handler = self.tools[tool_name]
        start_time = time.perf_counter()
        try:
            # Check parameter signatures
            sig = inspect.signature(handler)
            if len(sig.parameters) == 0:
                result = handler()
            else:
                result = handler(**arguments)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return MCPCallResponse(
                success=True,
                server_name=self.name,
                tool_name=tool_name,
                result=result,
                execution_time_ms=round(elapsed_ms, 2)
            )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return MCPCallResponse(
                success=False,
                server_name=self.name,
                tool_name=tool_name,
                error=str(e),
                execution_time_ms=round(elapsed_ms, 2)
            )
