"""
XAgent base class for L3AGI integration
"""

import sys
import os
from typing import List, Dict, Any, Optional

# Add XAgent to path for imports
xagent_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'XAgent')
sys.path.insert(0, xagent_path)

try:
    from XAgent.agent.base_agent import BaseAgent
    from XAgent.message_history import Message
    from XAgent.utils import LLMStatusCode
    XAGENT_AVAILABLE = True
except ImportError:
    XAGENT_AVAILABLE = False
    # Fallback classes for when XAgent is not available
    class BaseAgent:
        pass
    
    class Message:
        def __init__(self, role: str, content: str, timestamp=None):
            self.role = role
            self.content = content
            self.timestamp = timestamp
    
    class LLMStatusCode:
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ERROR = "ERROR"

class L3AGIXAgent(BaseAgent):
    """Base XAgent class adapted for L3AGI framework"""
    
    def __init__(self, config: Dict[str, Any], prompt_messages: Optional[List[Message]] = None):
        if XAGENT_AVAILABLE:
            super().__init__(config, prompt_messages)
        else:
            self.config = config
            self.prompt_messages = prompt_messages or []
        
        self.l3agi_config = {}
        self.agent_name = "L3AGI_XAgent"
        self.session_id = None
        self.sender_name = None
    
    def parse(self, **args) -> tuple:
        """Parse input and return status, message, and metadata"""
        # This method is required by XAgent base class
        # Implementation will be specific to each agent type
        raise NotImplementedError("Subclasses must implement parse method")
    
    def set_l3agi_config(self, config: Dict[str, Any]):
        """Set L3AGI-specific configuration"""
        self.l3agi_config = config
    
    def get_l3agi_config(self) -> Dict[str, Any]:
        """Get L3AGI-specific configuration"""
        return self.l3agi_config
    
    def set_session_info(self, session_id: str, sender_name: str):
        """Set session information for L3AGI"""
        self.session_id = session_id
        self.sender_name = sender_name
    
    def get_session_info(self) -> tuple:
        """Get session information"""
        return self.session_id, self.sender_name
    
    def is_xagent_available(self) -> bool:
        """Check if XAgent framework is available"""
        return XAGENT_AVAILABLE
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.agent_name,
            "type": "XAgent",
            "xagent_available": XAGENT_AVAILABLE,
            "l3agi_config": self.l3agi_config,
            "session_id": self.session_id,
            "sender_name": self.sender_name
        }
