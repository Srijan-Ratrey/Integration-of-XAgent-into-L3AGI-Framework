#!/usr/bin/env python3
"""
Test script to verify Phase 1: Foundation Setup
"""

import sys
import os

def test_imports():
    """Test that we can import our new XAgent foundation"""
    
    print("🧪 Testing XAgent Foundation Setup")
    print("=" * 50)
    
    try:
        # Test base XAgent class
        from agents.xagent.base_xagent import L3AGIXAgent
        print("✅ L3AGIXAgent imported successfully")
        
        # Test tool adapter
        from agents.xagent.tools.tool_adapter import L3AGIToolAdapter
        print("✅ L3AGIToolAdapter imported successfully")
        
        # Test safety wrapper
        from agents.xagent.tools.safety_wrapper import ToolSafetyWrapper
        print("✅ ToolSafetyWrapper imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_base_agent():
    """Test the base XAgent class"""
    
    print("\n🔧 Testing Base XAgent Class:")
    print("-" * 30)
    
    try:
        from agents.xagent.base_xagent import L3AGIXAgent
        
        # Create base agent
        config = {"test": "config"}
        agent = L3AGIXAgent(config)
        
        # Test basic functionality
        print(f"✅ Agent created: {agent.agent_name}")
        print(f"✅ XAgent available: {agent.is_xagent_available()}")
        
        # Test L3AGI config
        agent.set_l3agi_config({"session_id": "test123", "user": "testuser"})
        l3agi_config = agent.get_l3agi_config()
        print(f"✅ L3AGI config set: {l3agi_config}")
        
        # Test session info
        agent.set_session_info("session123", "testuser")
        session_id, sender_name = agent.get_session_info()
        print(f"✅ Session info set: {session_id}, {sender_name}")
        
        # Test agent info
        agent_info = agent.get_agent_info()
        print(f"✅ Agent info: {agent_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Base agent test failed: {e}")
        return False

def test_tool_adapter():
    """Test the tool adapter"""
    
    print("\n🔧 Testing Tool Adapter:")
    print("-" * 25)
    
    try:
        from agents.xagent.tools.tool_adapter import L3AGIToolAdapter
        
        # Create mock tools
        class MockTool:
            def __init__(self, name, description="Mock tool"):
                self.name = name
                self.description = description
                self.parameters = {"required": ["input"]}
            
            def run(self, input_text):
                return f"Mock result for: {input_text}"
        
        mock_tools = [
            MockTool("SearchTool", "Search the web"),
            MockTool("FileTool", "File operations")
        ]
        
        # Create adapter
        adapter = L3AGIToolAdapter(mock_tools)
        
        # Test adapted tools
        adapted_tools = adapter.get_adapted_tools()
        print(f"✅ Adapted {len(adapted_tools)} tools")
        
        # Test tool execution
        result = adapter.execute_tool("SearchTool", input_text="test query")
        print(f"✅ Tool execution: {result}")
        
        # Test tool listing
        tool_names = adapter.list_tools()
        print(f"✅ Tool names: {tool_names}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tool adapter test failed: {e}")
        return False

def test_safety_wrapper():
    """Test the safety wrapper"""
    
    print("\n🔧 Testing Safety Wrapper:")
    print("-" * 25)
    
    try:
        from agents.xagent.tools.safety_wrapper import ToolSafetyWrapper
        
        # Create safety wrapper
        safety = ToolSafetyWrapper(enable_logging=False)
        
        # Test safe execution
        def safe_function(x):
            return x * 2
        
        result = safety.execute_safely(safe_function, "SafeFunction", 5)
        print(f"✅ Safe execution: {result}")
        
        # Test execution stats
        stats = safety.get_execution_stats()
        print(f"✅ Execution stats: {stats}")
        
        # Test recent executions
        recent = safety.get_recent_executions(5)
        print(f"✅ Recent executions: {len(recent)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Safety wrapper test failed: {e}")
        return False

def test_directory_structure():
    """Test that our directory structure is correct"""
    
    print("\n📁 Testing Directory Structure:")
    print("-" * 30)
    
    required_files = [
        "agents/xagent/__init__.py",
        "agents/xagent/base_xagent.py",
        "agents/xagent/tools/__init__.py",
        "agents/xagent/tools/tool_adapter.py",
        "agents/xagent/tools/safety_wrapper.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def show_next_steps():
    """Show what's next in the migration"""
    
    print("\n🚀 Foundation Setup Complete!")
    print("=" * 35)
    
    print("✅ Phase 1: Foundation Setup - COMPLETED")
    print("📋 What we've accomplished:")
    print("   - Created XAgent directory structure")
    print("   - Implemented base XAgent class")
    print("   - Created tool adapter for L3AGI tools")
    print("   - Implemented safety wrapper")
    print("   - All components tested and working")
    
    print("\n🔄 Next Phase: Core Migration")
    print("📋 What's next:")
    print("   1. Create XAgent conversational agent")
    print("   2. Migrate dialogue agent with tools")
    print("   3. Update test framework")
    print("   4. Test new agent functionality")
    
    print("\n💡 Ready to continue with Phase 2!")

if __name__ == "__main__":
    print("🚀 Starting Foundation Setup Tests")
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test each component
        base_ok = test_base_agent()
        adapter_ok = test_tool_adapter()
        safety_ok = test_safety_wrapper()
        structure_ok = test_directory_structure()
        
        # Show results
        if all([base_ok, adapter_ok, safety_ok, structure_ok]):
            show_next_steps()
        else:
            print("\n❌ Some tests failed. Check the errors above.")
    else:
        print("\n❌ Import tests failed. Check the foundation setup.")
