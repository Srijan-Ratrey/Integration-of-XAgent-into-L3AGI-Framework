"""
Tool adapter to integrate L3AGI tools with XAgent
"""

from typing import List, Dict, Any, Callable, Optional
import logging

class L3AGIToolAdapter:
    """Adapter to make L3AGI tools compatible with XAgent"""
    
    def __init__(self, tools: List[Any]):
        self.tools = tools
        self.adapted_tools = self._adapt_tools()
        self.logger = logging.getLogger(__name__)
    
    def _adapt_tools(self) -> List[Dict[str, Any]]:
        """Convert L3AGI tools to XAgent format"""
        adapted = []
        
        for tool in self.tools:
            try:
                # Extract tool information
                tool_info = {
                    "name": getattr(tool, 'name', tool.__class__.__name__),
                    "description": getattr(tool, 'description', ''),
                    "parameters": getattr(tool, 'parameters', {}),
                    "function": tool.run if hasattr(tool, 'run') else tool,
                    "tool_type": "l3agi_tool",
                    "original_tool": tool
                }
                adapted.append(tool_info)
                self.logger.info(f"Adapted tool: {tool_info['name']}")
                
            except Exception as e:
                self.logger.warning(f"Failed to adapt tool {tool}: {e}")
                # Create a basic tool info as fallback
                tool_info = {
                    "name": str(tool),
                    "description": "L3AGI tool (fallback)",
                    "parameters": {},
                    "function": tool,
                    "tool_type": "l3agi_tool_fallback",
                    "original_tool": tool
                }
                adapted.append(tool_info)
        
        return adapted
    
    def get_adapted_tools(self) -> List[Dict[str, Any]]:
        """Get tools in XAgent format"""
        return self.adapted_tools
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool"""
        for tool_info in self.adapted_tools:
            if tool_info["name"] == tool_name:
                try:
                    tool_func = tool_info["function"]
                    if hasattr(tool_func, 'run'):
                        result = tool_func.run(**kwargs)
                    elif callable(tool_func):
                        result = tool_func(**kwargs)
                    else:
                        result = f"Tool {tool_name} is not callable"
                    
                    self.logger.info(f"Executed tool {tool_name} successfully")
                    return result
                    
                except Exception as e:
                    error_msg = f"Tool {tool_name} execution failed: {str(e)}"
                    self.logger.error(error_msg)
                    return error_msg
        
        raise ValueError(f"Tool {tool_name} not found")
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        for tool_info in self.adapted_tools:
            if tool_info["name"] == tool_name:
                return tool_info
        return None
    
    def list_tools(self) -> List[str]:
        """List all available tool names"""
        return [tool["name"] for tool in self.adapted_tools]
    
    def validate_tool_input(self, tool_name: str, **kwargs) -> bool:
        """Validate input parameters for a tool"""
        tool_info = self.get_tool_info(tool_name)
        if not tool_info:
            return False
        
        # Basic validation - can be enhanced
        required_params = tool_info.get("parameters", {}).get("required", [])
        for param in required_params:
            if param not in kwargs:
                return False
        
        return True
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get the schema for a specific tool"""
        tool_info = self.get_tool_info(tool_name)
        if not tool_info:
            return None
        
        return {
            "name": tool_info["name"],
            "description": tool_info["description"],
            "parameters": tool_info["parameters"],
            "type": tool_info["tool_type"]
        }
