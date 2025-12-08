"""
Test: Guided Workflow / 测试：引导式工作流程

This script tests the guided workflow system.
本脚本测试引导式工作流程系统。
"""

import sys
from pathlib import Path

# Add src to path / 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cli.guided_workflow import GuidedWorkflow, WorkflowState
from cli.interactive_prompt import InteractivePrompt


def test_workflow_state():
    """Test WorkflowState creation / 测试WorkflowState创建"""
    print("测试 WorkflowState 创建 / Testing WorkflowState creation...")
    
    state = WorkflowState()
    assert state.current_step == 0
    assert state.completed_steps == []
    assert state.workflow_id is not None
    assert state.created_at is not None
    
    print("✓ WorkflowState 创建成功 / WorkflowState created successfully")
    return True


def test_workflow_initialization():
    """Test GuidedWorkflow initialization / 测试GuidedWorkflow初始化"""
    print("\n测试 GuidedWorkflow 初始化 / Testing GuidedWorkflow initialization...")
    
    workflow = GuidedWorkflow(state_dir="./test_workflow_states")
    assert workflow.prompt is not None
    assert workflow.state_dir.exists()
    assert len(workflow.steps) == 10
    
    print("✓ GuidedWorkflow 初始化成功 / GuidedWorkflow initialized successfully")
    print(f"  工作流步骤数 / Number of workflow steps: {len(workflow.steps)}")
    
    return True


def test_state_save_load():
    """Test state save and load / 测试状态保存和加载"""
    print("\n测试状态保存和加载 / Testing state save and load...")
    
    workflow = GuidedWorkflow(state_dir="./test_workflow_states")
    
    # Create a test state / 创建测试状态
    workflow.state = WorkflowState()
    workflow.state.market = "CN"
    workflow.state.market_name = "中国市场"
    workflow.state.asset_type = "stock"
    workflow.state.target_return = 20.0
    workflow.state.current_step = 2
    workflow.state.completed_steps = [0, 1]
    
    # Save state / 保存状态
    workflow._save_state()
    print("✓ 状态已保存 / State saved")
    
    # Load state / 加载状态
    loaded_state = workflow._load_latest_state()
    assert loaded_state is not None
    assert loaded_state.market == "CN"
    assert loaded_state.target_return == 20.0
    assert loaded_state.current_step == 2
    assert len(loaded_state.completed_steps) == 2
    
    print("✓ 状态加载成功 / State loaded successfully")
    print(f"  市场 / Market: {loaded_state.market}")
    print(f"  目标收益率 / Target Return: {loaded_state.target_return}%")
    print(f"  当前步骤 / Current Step: {loaded_state.current_step}")
    
    return True


def test_step_definitions():
    """Test that all steps are properly defined / 测试所有步骤是否正确定义"""
    print("\n测试步骤定义 / Testing step definitions...")
    
    workflow = GuidedWorkflow(state_dir="./test_workflow_states")
    
    expected_steps = [
        "市场和资产选择",
        "智能推荐",
        "目标设定",
        "策略优化",
        "模型训练",
        "历史回测",
        "模拟交易",
        "实盘交易设置",
        "实盘交易执行",
        "报告配置"
    ]
    
    for i, (step_name, step_func) in enumerate(workflow.steps):
        assert expected_steps[i] in step_name, f"Step {i+1} name mismatch"
        assert callable(step_func), f"Step {i+1} function is not callable"
        print(f"  ✓ 步骤 {i+1}: {step_name}")
    
    print("✓ 所有步骤定义正确 / All steps properly defined")
    return True


def test_interactive_prompt():
    """Test InteractivePrompt functionality / 测试InteractivePrompt功能"""
    print("\n测试 InteractivePrompt 功能 / Testing InteractivePrompt functionality...")
    
    prompt = InteractivePrompt()
    
    # Test display_message / 测试display_message
    prompt.display_message("这是一条测试消息 / This is a test message", "info")
    prompt.display_message("这是一条成功消息 / This is a success message", "success")
    prompt.display_message("这是一条警告消息 / This is a warning message", "warning")
    
    # Test display_progress / 测试display_progress
    print("\n测试进度显示 / Testing progress display:")
    for i in range(1, 6):
        prompt.display_progress(i, 5, "测试中... / Testing...")
        import time
        time.sleep(0.1)
    
    print("\n✓ InteractivePrompt 功能正常 / InteractivePrompt working correctly")
    return True


def main():
    """Run all tests / 运行所有测试"""
    print("="*80)
    print("引导式工作流程测试 / Guided Workflow Tests")
    print("="*80)
    
    tests = [
        test_workflow_state,
        test_workflow_initialization,
        test_state_save_load,
        test_step_definitions,
        test_interactive_prompt
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试失败 / Test failed: {test.__name__}")
            print(f"  错误 / Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*80)
    print(f"测试结果 / Test Results: {passed} 通过 / passed, {failed} 失败 / failed")
    print("="*80)
    
    # Cleanup test files / 清理测试文件
    import shutil
    test_dir = Path("./test_workflow_states")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("\n✓ 测试文件已清理 / Test files cleaned up")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
