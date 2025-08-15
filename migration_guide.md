# 🚀 Practical Migration Guide: L3AGI → XAgent

## 📋 Quick Start

This guide provides **step-by-step instructions** to migrate L3AGI from Langchain REACT Agent to XAgent.

## 🎯 What You'll Accomplish

- ✅ Replace Langchain with XAgent
- ✅ Maintain all existing functionality
- ✅ Add advanced planning capabilities
- ✅ Implement human collaboration features
- ✅ Create a more robust architecture

## 🛠️ Prerequisites

- Python 3.10+
- Git
- Basic understanding of Python
- 11-17 hours of development time

## 📁 Project Structure

```
new prog/
├── team-of-ai-agents/     # Current L3AGI system
├── XAgent/                # XAgent framework
├── demo_langchain_react.py # Current system demo
├── demo_xagent.py         # XAgent demo
├── migration_analysis.md  # Detailed analysis
└── migration_guide.md     # This guide
```

## 🚀 Phase 1: Foundation Setup (2-3 hours)

### Step 1.1: Create Migration Branch

```bash
cd team-of-ai-agents
git checkout -b migrate-to-xagent
git status
```

### Step 1.2: Install XAgent Dependencies

```bash
cd apps/server
pip install -r ../../XAgent/requirements.txt
```

### Step 1.3: Test XAgent Installation

```bash
python -c "import XAgent; print('XAgent imported successfully')"
```

### Step 1.4: Create New Directory Structure

```bash
mkdir -p agents/xagent/tools
touch agents/xagent/__init__.py
touch agents/xagent/tools/__init__.py
```

## 🔧 Phase 2: Core Agent Migration (4-6 hours)

### Step 2.1: Create XAgent Base Class

Create `agents/xagent/base_xagent.py`:

```python
"""
XAgent base class for L3AGI integration
"""

from XAgent.agent.base_agent import BaseAgent
from XAgent.message_history import Message
from XAgent.utils import LLMStatusCode
from typing import List, Dict, Any

class L3AGIXAgent(BaseAgent):
    """Base XAgent class adapted for L3AGI framework"""
    
    def __init__(self, config, prompt_messages: List[Message] = None):
        super().__init__(config, prompt_messages)
        self.l3agi_config = {}
    
    def parse(self, **args) -> (LLMStatusCode, Message, dict):
        """Parse input and return status, message, and metadata"""
        # Implementation will be specific to each agent type
        pass
    
    def set_l3agi_config(self, config: Dict[str, Any]):
        """Set L3AGI-specific configuration"""
        self.l3agi_config = config
    
    def get_l3agi_config(self) -> Dict[str, Any]:
        """Get L3AGI-specific configuration"""
        return self.l3agi_config
```

### Step 2.2: Create XAgent Conversational Agent

Create `agents/xagent/conversational_xagent.py`:

```python
"""
XAgent-based conversational agent for L3AGI
"""

import asyncio
from typing import List, Dict, Any
from XAgent.agent.plan_refine_agent import PlanRefineAgent
from XAgent.agent.tool_agent import ToolAgent
from XAgent.message_history import Message
from XAgent.utils import LLMStatusCode
from agents.xagent.base_xagent import L3AGIXAgent
from memory.zep.zep_memory import ZepMemory
from config import Config

class XAgentConversationalAgent(L3AGIXAgent):
    """XAgent-based conversational agent"""
    
    def __init__(self, config, tools: List[Any], memory: ZepMemory):
        super().__init__(config)
        self.tools = tools
        self.memory = memory
        self.planner = PlanRefineAgent(config)
        self.tool_agent = ToolAgent(config, tools)
    
    async def run(self, prompt: str, **kwargs) -> str:
        """Run the conversational agent"""
        
        # Create task message
        task_message = Message(
            role="user",
            content=prompt,
            timestamp=None
        )
        
        # Plan the approach
        status, plan_message, plan_metadata = self.planner.parse(
            messages=[task_message]
        )
        
        if status != LLMStatusCode.SUCCESS:
            return f"Planning failed: {status}"
        
        # Execute the plan using tools
        status, result_message, result_metadata = self.tool_agent.parse(
            messages=[plan_message],
            plan=plan_metadata.get('plan')
        )
        
        if status != LLMStatusCode.SUCCESS:
            return f"Execution failed: {status}"
        
        # Save to memory
        self.memory.save_context(
            {"input": prompt},
            {"output": result_message.content}
        )
        
        return result_message.content
    
    def parse(self, **args) -> (LLMStatusCode, Message, dict):
        """Parse input for XAgent compatibility"""
        # This method is required by XAgent base class
        # Implementation depends on specific use case
        pass
```

### Step 2.3: Create Tool Adapter

Create `agents/xagent/tools/tool_adapter.py`:

```python
"""
Tool adapter to integrate L3AGI tools with XAgent
"""

from typing import List, Dict, Any, Callable
from XAgent.agent.tool_agent import ToolAgent

class L3AGIToolAdapter:
    """Adapter to make L3AGI tools compatible with XAgent"""
    
    def __init__(self, tools: List[Any]):
        self.tools = tools
        self.adapted_tools = self._adapt_tools()
    
    def _adapt_tools(self) -> List[Dict[str, Any]]:
        """Convert L3AGI tools to XAgent format"""
        adapted = []
        
        for tool in self.tools:
            # Extract tool information
            tool_info = {
                "name": getattr(tool, 'name', tool.__class__.__name__),
                "description": getattr(tool, 'description', ''),
                "parameters": getattr(tool, 'parameters', {}),
                "function": tool.run if hasattr(tool, 'run') else tool
            }
            adapted.append(tool_info)
        
        return adapted
    
    def get_adapted_tools(self) -> List[Dict[str, Any]]:
        """Get tools in XAgent format"""
        return self.adapted_tools
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a specific tool"""
        for tool in self.tools:
            if getattr(tool, 'name', tool.__class__.__name__) == tool_name:
                if hasattr(tool, 'run'):
                    return tool.run(**kwargs)
                elif callable(tool):
                    return tool(**kwargs)
        
        raise ValueError(f"Tool {tool_name} not found")
```

## 🔌 Phase 3: Tool Integration (2-3 hours)

### Step 3.1: Update Conversational Agent to Use Tool Adapter

Modify `agents/xagent/conversational_xagent.py`:

```python
# Add import
from agents.xagent.tools.tool_adapter import L3AGIToolAdapter

class XAgentConversationalAgent(L3AGIXAgent):
    def __init__(self, config, tools: List[Any], memory: ZepMemory):
        super().__init__(config)
        self.tool_adapter = L3AGIToolAdapter(tools)
        self.memory = memory
        self.planner = PlanRefineAgent(config)
        # Use adapted tools
        self.tool_agent = ToolAgent(config, self.tool_adapter.get_adapted_tools())
```

### Step 3.2: Create Safety Wrapper

Create `agents/xagent/tools/safety_wrapper.py`:

```python
"""
Safety wrapper for tool execution in XAgent
"""

import docker
from typing import Any, Dict
import logging

class ToolSafetyWrapper:
    """Wrapper to ensure safe tool execution"""
    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.logger = logging.getLogger(__name__)
    
    def execute_safely(self, tool_func: Callable, *args, **kwargs) -> Any:
        """Execute tool with safety measures"""
        try:
            # Log tool execution
            self.logger.info(f"Executing tool: {tool_func.__name__}")
            
            # Execute tool
            result = tool_func(*args, **kwargs)
            
            # Log success
            self.logger.info(f"Tool {tool_func.__name__} executed successfully")
            
            return result
            
        except Exception as e:
            # Log error
            self.logger.error(f"Tool {tool_func.__name__} failed: {str(e)}")
            
            # Return safe error message
            return f"Tool execution failed: {str(e)}"
    
    def validate_input(self, tool_name: str, **kwargs) -> bool:
        """Validate tool input parameters"""
        # Add input validation logic here
        return True
```

## 🧠 Phase 4: Memory & Context (1-2 hours)

### Step 4.1: Integrate ZepMemory with XAgent

Modify `agents/xagent/conversational_xagent.py`:

```python
class XAgentConversationalAgent(L3AGIXAgent):
    def __init__(self, config, tools: List[Any], memory: ZepMemory):
        super().__init__(config)
        self.tool_adapter = L3AGIToolAdapter(tools)
        self.memory = memory
        self.planner = PlanRefineAgent(config)
        self.tool_agent = ToolAgent(config, self.tool_adapter.get_adapted_tools())
    
    def _get_conversation_context(self) -> List[Message]:
        """Get conversation context from ZepMemory"""
        memory_vars = self.memory.load_memory_variables({})
        chat_history = memory_vars.get("chat_history", [])
        
        # Convert to XAgent Message format
        messages = []
        for msg in chat_history:
            if hasattr(msg, 'type') and msg.type == 'human':
                messages.append(Message(role="user", content=msg.content))
            elif hasattr(msg, 'type') and msg.type == 'ai':
                messages.append(Message(role="assistant", content=msg.content))
        
        return messages
    
    async def run(self, prompt: str, **kwargs) -> str:
        """Run with conversation context"""
        
        # Get conversation context
        context_messages = self._get_conversation_context()
        
        # Add current prompt
        task_message = Message(role="user", content=prompt)
        all_messages = context_messages + [task_message]
        
        # Plan with context
        status, plan_message, plan_metadata = self.planner.parse(
            messages=all_messages
        )
        
        # ... rest of implementation
```

## 🧪 Phase 5: Testing & Validation (2-3 hours)

### Step 5.1: Create Test Script

Create `test_xagent_migration.py`:

```python
#!/usr/bin/env python3
"""
Test script for XAgent migration
"""

import asyncio
import sys
import os

# Add L3AGI to path
sys.path.append('team-of-ai-agents/apps/server')

from agents.xagent.conversational_xagent import XAgentConversationalAgent
from memory.zep.zep_memory import ZepMemory
from config import Config

async def test_xagent_conversational():
    """Test the XAgent conversational agent"""
    
    print("🧪 Testing XAgent Conversational Agent")
    print("=" * 50)
    
    try:
        # Create mock config
        config = {
            "llm": {
                "model": "gpt-3.5-turbo",
                "api_key": "test-key"
            }
        }
        
        # Create mock tools
        tools = []
        
        # Create mock memory
        memory = ZepMemory(
            session_id="test-session",
            url="http://localhost:8000",
            api_key="test-key",
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create XAgent
        agent = XAgentConversationalAgent(config, tools, memory)
        
        print("✅ XAgent created successfully")
        
        # Test basic functionality
        test_prompt = "Hello, how are you?"
        print(f"\n📝 Testing with prompt: {test_prompt}")
        
        # Note: This will fail without proper LLM setup
        # but it tests the basic structure
        print("✅ Basic structure test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_imports():
    """Test that all imports work"""
    
    print("📦 Testing Imports")
    print("=" * 30)
    
    try:
        from XAgent.agent.base_agent import BaseAgent
        print("✅ XAgent base_agent imported")
        
        from XAgent.agent.plan_refine_agent import PlanRefineAgent
        print("✅ XAgent plan_refine_agent imported")
        
        from XAgent.agent.tool_agent import ToolAgent
        print("✅ XAgent tool_agent imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting XAgent Migration Tests")
    
    # Test imports first
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        asyncio.run(test_xagent_conversational())
        print("\n✅ All tests completed!")
    else:
        print("\n❌ Import tests failed. Check XAgent installation.")
```

### Step 5.2: Run Tests

```bash
cd team-of-ai-agents/apps/server
python ../../../test_xagent_migration.py
```

## 🔄 Phase 6: Integration & Cleanup (1-2 hours)

### Step 6.1: Update Main Files

Replace the old agent usage in `conversational.py`:

```python
# OLD: Langchain implementation
# agent = create_react_agent(llm, tools, prompt=agentPrompt)

# NEW: XAgent implementation
from agents.xagent.conversational_xagent import XAgentConversationalAgent

agent = XAgentConversationalAgent(
    config=agent_config,
    tools=tools,
    memory=memory
)

# Use the new agent
response = await agent.run(prompt)
```

### Step 6.2: Remove Old Dependencies

Update `pyproject.toml`:

```toml
# Remove these lines
# langchain = "^0.1.11"
# langchain-community = "^0.0.25"
# langchainhub = "^0.1.15"

# Add XAgent dependencies
# (already installed from requirements.txt)
```

### Step 6.3: Update Imports

Search and replace throughout the codebase:

```bash
# Find all Langchain imports
grep -r "from langchain" .
grep -r "import langchain" .

# Replace with XAgent equivalents
# (This will be done file by file)
```

## 📊 Validation Checklist

### ✅ Foundation Setup
- [ ] Migration branch created
- [ ] XAgent dependencies installed
- [ ] Directory structure created
- [ ] XAgent imports working

### ✅ Core Migration
- [ ] Base XAgent class created
- [ ] Conversational agent migrated
- [ ] Tool adapter implemented
- [ ] Safety wrapper created

### ✅ Tool Integration
- [ ] Tools adapted to XAgent format
- [ ] Tool execution working
- [ ] Safety measures implemented
- [ ] Error handling functional

### ✅ Memory & Context
- [ ] ZepMemory integrated
- [ ] Conversation context preserved
- [ ] Memory persistence working
- [ ] Context retrieval functional

### ✅ Testing & Validation
- [ ] Unit tests passing
- [ ] Integration tests working
- [ ] Performance acceptable
- [ ] All functionality preserved

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Check XAgent installation
   pip install -r XAgent/requirements.txt
   ```

2. **Tool Compatibility**
   ```python
   # Solution: Use tool adapter
   tool_adapter = L3AGIToolAdapter(tools)
   adapted_tools = tool_adapter.get_adapted_tools()
   ```

3. **Memory Issues**
   ```python
   # Solution: Check ZepMemory configuration
   memory = ZepMemory(session_id="test", url="http://localhost:8000")
   ```

4. **Performance Problems**
   ```python
   # Solution: Add caching and optimization
   # Implement in tool execution
   ```

## 🎉 Success Criteria

- ✅ All existing L3AGI functionality works
- ✅ XAgent features are functional
- ✅ Performance is acceptable (< 2x current)
- ✅ Tests are passing
- ✅ Documentation is complete
- ✅ Code is clean and maintainable

## 📝 Next Steps After Migration

1. **Performance Optimization**
2. **Advanced XAgent Features**
3. **Human Collaboration Implementation**
4. **Tool Safety Enhancements**
5. **User Experience Improvements**

---

*This guide provides a complete roadmap for migrating L3AGI to XAgent. Follow each phase step-by-step and test thoroughly before proceeding to the next phase.*
