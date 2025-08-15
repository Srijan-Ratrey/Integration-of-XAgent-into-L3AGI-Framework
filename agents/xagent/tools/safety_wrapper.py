"""
Safety wrapper for tool execution in XAgent
"""

import logging
from typing import Any, Dict, Callable, Optional, List
import time
import traceback

class ToolSafetyWrapper:
    """Wrapper to ensure safe tool execution"""
    
    def __init__(self, enable_logging: bool = True):
        self.logger = logging.getLogger(__name__) if enable_logging else None
        self.execution_history = []
        self.max_execution_time = 30  # seconds
        self.max_memory_usage = 100 * 1024 * 1024  # 100MB
    
    def execute_safely(self, tool_func: Callable, tool_name: str, *args, **kwargs) -> Any:
        """Execute tool with safety measures"""
        start_time = time.time()
        execution_id = f"{tool_name}_{int(start_time)}"
        
        # Log execution start
        self._log_execution_start(execution_id, tool_name, args, kwargs)
        
        try:
            # Input validation
            if not self._validate_input(tool_name, args, kwargs):
                error_msg = f"Input validation failed for tool {tool_name}"
                self._log_execution_error(execution_id, tool_name, error_msg)
                return error_msg
            
            # Execute tool with timeout protection
            result = self._execute_with_timeout(tool_func, *args, **kwargs)
            
            # Log successful execution
            execution_time = time.time() - start_time
            self._log_execution_success(execution_id, tool_name, execution_time, result)
            
            # Record execution
            self._record_execution(execution_id, tool_name, True, execution_time, result)
            
            return result
            
        except Exception as e:
            # Log error
            execution_time = time.time() - start_time
            error_msg = f"Tool {tool_name} execution failed: {str(e)}"
            self._log_execution_error(execution_id, tool_name, error_msg)
            
            # Record failed execution
            self._record_execution(execution_id, tool_name, False, execution_time, error_msg)
            
            # Return safe error message
            return error_msg
    
    def _validate_input(self, tool_name: str, args: tuple, kwargs: dict) -> bool:
        """Validate tool input parameters"""
        try:
            # Basic validation - can be enhanced
            if len(args) > 10:  # Limit number of positional arguments
                return False
            
            if len(kwargs) > 20:  # Limit number of keyword arguments
                return False
            
            # Check for potentially dangerous inputs
            dangerous_patterns = [
                "eval(", "exec(", "import ", "os.system", "subprocess",
                "file://", "http://", "https://", "ftp://"
            ]
            
            input_str = str(args) + str(kwargs)
            for pattern in dangerous_patterns:
                if pattern in input_str:
                    self._log_security_warning(tool_name, f"Potentially dangerous input: {pattern}")
                    return False
            
            return True
            
        except Exception as e:
            self._log_security_warning(tool_name, f"Input validation error: {e}")
            return False
    
    def _execute_with_timeout(self, tool_func: Callable, *args, **kwargs) -> Any:
        """Execute tool with timeout protection"""
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Tool execution timed out after {self.max_execution_time} seconds")
        
        # Set timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.max_execution_time)
        
        try:
            result = tool_func(*args, **kwargs)
            signal.alarm(0)  # Cancel timeout
            return result
        except TimeoutError:
            signal.alarm(0)  # Cancel timeout
            raise
        except Exception:
            signal.alarm(0)  # Cancel timeout
            raise
    
    def _log_execution_start(self, execution_id: str, tool_name: str, args: tuple, kwargs: dict):
        """Log the start of tool execution"""
        if self.logger:
            self.logger.info(f"Starting tool execution: {execution_id} - {tool_name}")
            self.logger.debug(f"Args: {args}, Kwargs: {kwargs}")
    
    def _log_execution_success(self, execution_id: str, tool_name: str, execution_time: float, result: Any):
        """Log successful tool execution"""
        if self.logger:
            self.logger.info(f"Tool execution successful: {execution_id} - {tool_name} in {execution_time:.2f}s")
            self.logger.debug(f"Result: {result}")
    
    def _log_execution_error(self, execution_id: str, tool_name: str, error_msg: str):
        """Log tool execution error"""
        if self.logger:
            self.logger.error(f"Tool execution failed: {execution_id} - {tool_name}: {error_msg}")
    
    def _log_security_warning(self, tool_name: str, warning_msg: str):
        """Log security warning"""
        if self.logger:
            self.logger.warning(f"Security warning for {tool_name}: {warning_msg}")
    
    def _record_execution(self, execution_id: str, tool_name: str, success: bool, 
                         execution_time: float, result: Any):
        """Record tool execution for monitoring"""
        execution_record = {
            "id": execution_id,
            "tool_name": tool_name,
            "success": success,
            "execution_time": execution_time,
            "timestamp": time.time(),
            "result": str(result)[:1000]  # Limit result length
        }
        
        self.execution_history.append(execution_record)
        
        # Keep only last 1000 executions
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        successful = [e for e in self.execution_history if e["success"]]
        failed = [e for e in self.execution_history if not e["success"]]
        
        total_time = sum(e["execution_time"] for e in self.execution_history)
        avg_time = total_time / len(self.execution_history) if self.execution_history else 0
        
        return {
            "total_executions": len(self.execution_history),
            "successful_executions": len(successful),
            "failed_executions": len(failed),
            "success_rate": len(successful) / len(self.execution_history) if self.execution_history else 0,
            "average_execution_time": avg_time,
            "total_execution_time": total_time
        }
    
    def get_recent_executions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent tool executions"""
        return self.execution_history[-limit:] if self.execution_history else []
    
    def clear_execution_history(self):
        """Clear execution history"""
        self.execution_history.clear()
    
    def set_max_execution_time(self, seconds: int):
        """Set maximum execution time for tools"""
        self.max_execution_time = max(1, seconds)  # Minimum 1 second
    
    def set_max_memory_usage(self, bytes_limit: int):
        """Set maximum memory usage for tools"""
        self.max_memory_usage = max(1024, bytes_limit)  # Minimum 1KB
