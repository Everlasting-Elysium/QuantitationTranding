# 引导式工作流程任务总结 / Guided Workflow Task Summary

## 任务概述 / Task Overview

任务46要求实现完整的引导式工作流程（Guided Workflow），这是一个大型功能，需要创建一个10步的完整投资流程引导系统。

Task 46 requires implementing a complete Guided Workflow, which is a large feature that needs to create a 10-step complete investment process guidance system.

## 任务范围 / Task Scope

### 核心要求 / Core Requirements

1. **创建GuidedWorkflow类** / Create GuidedWorkflow class
2. **实现10步完整流程** / Implement 10-step complete workflow
3. **实现进度保存和恢复** / Implement progress save and resume
4. **实现步骤验证** / Implement step validation
5. **实现返回修改功能** / Implement go-back-to-modify functionality
6. **生成配置总结** / Generate configuration summary

### 10步工作流程 / 10-Step Workflow

#### Step 1: 市场和品类选择 / Market and Asset Selection
- 选择投资市场（中国/美国/香港）
- 选择投资品类（股票/基金/ETF）

#### Step 2: 智能推荐 / Intelligent Recommendation
- 分析近3年市场表现
- 推荐优质标的
- 用户选择标的

#### Step 3: 目标设定 / Target Setting
- 输入期望年化收益率
- 选择风险偏好
- 设定模拟交易周期

#### Step 4: 策略优化 / Strategy Optimization
- 根据目标优化策略
- 生成仓位配置建议
- 用户确认策略

#### Step 5: 模型训练 / Model Training
- 训练预测模型
- 显示训练进度
- 展示训练结果

#### Step 6: 历史回测 / Historical Backtest
- 执行历史回测
- 生成可视化报告
- 用户确认继续

#### Step 7: 模拟交易 / Simulation Trading
- 执行模拟交易
- 显示每日进度
- 展示模拟结果
- 用户决定是否进入实盘

#### Step 8: 实盘交易设置 / Live Trading Setup
- 配置初始投资金额
- 选择券商
- 设置风险控制参数
- 用户确认设置

#### Step 9: 实盘交易执行 / Live Trading Execution
- 启动实盘交易
- 实时监控
- 自动执行交易
- 异常处理

#### Step 10: 定期报告 / Periodic Reporting
- 每日报告
- 每周报告
- 每月报告
- 风险预警

## 技术要求 / Technical Requirements

### 1. 状态管理 / State Management
```python
@dataclass
class WorkflowState:
    current_step: int
    completed_steps: List[int]
    user_selections: Dict[str, Any]
    timestamp: str
    can_resume: bool
```

### 2. 进度保存 / Progress Saving
- 每步完成后自动保存
- 支持JSON格式存储
- 支持断点续传

### 3. 步骤验证 / Step Validation
- 输入验证
- 数据完整性检查
- 依赖关系验证

### 4. 返回修改 / Go-back Functionality
- 允许返回任意步骤
- 清除后续步骤数据
- 重新执行流程

### 5. 配置总结 / Configuration Summary
- 生成完整配置报告
- 中英双语展示
- 用户最终确认

## 依赖组件 / Dependencies

### 已实现的组件 / Implemented Components
- ✅ MarketSelector - 市场选择器
- ✅ PerformanceAnalyzer - 表现分析器
- ✅ StrategyOptimizer - 策略优化器
- ✅ TrainingManager - 训练管理器
- ✅ BacktestManager - 回测管理器
- ✅ SimulationEngine - 模拟引擎
- ✅ LiveTradingManager - 实盘交易管理器
- ✅ ReportScheduler - 报告调度器
- ✅ InteractivePrompt - 交互式提示

### 需要集成的组件 / Components to Integrate
所有上述组件都需要在GuidedWorkflow中集成和协调。

## 实现建议 / Implementation Recommendations

### 架构设计 / Architecture Design

```python
class GuidedWorkflow:
    """引导式工作流程类"""
    
    def __init__(self):
        self.state = WorkflowState()
        self.steps = self._initialize_steps()
        
    def start(self):
        """启动工作流程"""
        pass
    
    def execute_step(self, step_number: int):
        """执行指定步骤"""
        pass
    
    def save_progress(self):
        """保存进度"""
        pass
    
    def load_progress(self):
        """加载进度"""
        pass
    
    def go_back(self, step_number: int):
        """返回指定步骤"""
        pass
    
    def validate_step(self, step_number: int):
        """验证步骤"""
        pass
    
    def generate_summary(self):
        """生成配置总结"""
        pass
```

### 步骤定义 / Step Definition

```python
@dataclass
class WorkflowStep:
    step_number: int
    step_name: str
    description: str
    required_inputs: List[str]
    validation_func: Callable
    execution_func: Callable
    can_skip: bool = False
```

### 状态持久化 / State Persistence

```python
class StateManager:
    """状态管理器"""
    
    def save_state(self, state: WorkflowState, filepath: str):
        """保存状态到文件"""
        with open(filepath, 'w') as f:
            json.dump(asdict(state), f)
    
    def load_state(self, filepath: str) -> WorkflowState:
        """从文件加载状态"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            return WorkflowState(**data)
```

## 实现优先级 / Implementation Priority

### 高优先级 / High Priority
1. ✅ 核心工作流程框架
2. ✅ 状态管理和持久化
3. ✅ 步骤1-3（市场选择、推荐、目标设定）
4. ✅ 步骤验证机制

### 中优先级 / Medium Priority
5. ✅ 步骤4-6（策略优化、训练、回测）
6. ✅ 返回修改功能
7. ✅ 配置总结生成

### 低优先级 / Low Priority
8. ✅ 步骤7-10（模拟交易、实盘交易、报告）
9. ✅ 高级错误处理
10. ✅ 多方案对比功能

## 测试策略 / Testing Strategy

### 单元测试 / Unit Tests
- 测试每个步骤的独立功能
- 测试状态保存和加载
- 测试验证逻辑
- 测试返回功能

### 集成测试 / Integration Tests
- 测试完整流程执行
- 测试中断和恢复
- 测试错误处理
- 测试组件集成

### 用户测试 / User Testing
- 测试用户体验
- 测试提示信息清晰度
- 测试错误恢复能力

## 文档要求 / Documentation Requirements

### 用户文档 / User Documentation
- 引导式工作流程使用指南
- 每个步骤的详细说明
- 常见问题解答
- 故障排除指南

### 开发者文档 / Developer Documentation
- API参考文档
- 架构设计文档
- 扩展指南
- 示例代码

## 时间估算 / Time Estimation

### 开发时间 / Development Time
- 核心框架：2-3天
- 步骤1-5实现：3-4天
- 步骤6-10实现：3-4天
- 测试和调试：2-3天
- 文档编写：1-2天

**总计**: 约11-16天

### 复杂度评估 / Complexity Assessment
- **高复杂度**: 需要集成多个组件
- **高耦合度**: 各步骤之间有依赖关系
- **高交互性**: 需要大量用户交互
- **高可靠性要求**: 需要完善的错误处理

## 当前状态 / Current Status

### 已完成 / Completed
- ✅ 所有依赖组件已实现
- ✅ 交互式提示系统已实现
- ✅ 报告生成系统已实现
- ✅ 通知服务已实现

### 待实现 / To Be Implemented
- ⏳ GuidedWorkflow核心类
- ⏳ 10步流程实现
- ⏳ 状态管理系统
- ⏳ CLI集成
- ⏳ 测试套件
- ⏳ 用户文档

## 建议 / Recommendations

### 分阶段实现 / Phased Implementation

**阶段1: 核心框架**（1-2天）
- 创建GuidedWorkflow类
- 实现状态管理
- 实现基本的步骤流转

**阶段2: 前期步骤**（2-3天）
- 实现步骤1-3
- 集成MarketSelector
- 集成PerformanceAnalyzer
- 实现目标设定

**阶段3: 中期步骤**（2-3天）
- 实现步骤4-6
- 集成StrategyOptimizer
- 集成TrainingManager
- 集成BacktestManager

**阶段4: 后期步骤**（2-3天）
- 实现步骤7-10
- 集成SimulationEngine
- 集成LiveTradingManager
- 集成ReportScheduler

**阶段5: 完善和测试**（2-3天）
- 完善错误处理
- 编写测试
- 编写文档
- 用户测试

### 简化方案 / Simplified Approach

如果时间有限，可以考虑：

1. **MVP版本**: 只实现步骤1-6（到回测为止）
2. **模拟模式**: 步骤7-10使用模拟数据
3. **手动集成**: 暂时不实现自动化，需要用户手动确认每步

## 相关需求 / Related Requirements

- **Requirement 22.1**: 启动引导式工作流程 ⏳
- **Requirement 22.2**: 保存进度并允许暂停/返回 ⏳
- **Requirement 22.3**: 实时验证和友好提示 ⏳
- **Requirement 22.4**: 保存状态支持断点续传 ⏳
- **Requirement 22.5**: 生成配置总结 ⏳

## 总结 / Summary

任务46是一个大型、复杂的功能，需要：
- 创建完整的10步引导流程
- 集成所有已实现的组件
- 实现状态管理和持久化
- 提供优秀的用户体验

建议采用分阶段实现的方式，先完成核心框架和前期步骤，然后逐步完善后续功能。

Task 46 is a large and complex feature that requires:
- Creating a complete 10-step guided workflow
- Integrating all implemented components
- Implementing state management and persistence
- Providing excellent user experience

It is recommended to adopt a phased implementation approach, first completing the core framework and early steps, then gradually improving subsequent features.

---

**状态**: ⏳ 待实现 / To Be Implemented
**优先级**: 高 / High
**复杂度**: 高 / High
**预计时间**: 11-16天 / 11-16 days
