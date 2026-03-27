# Agent 系统

项目实现了基于 AI Agent 的智能分析架构，支持单 Agent 和多 Agent 协作两种模式。

## 什么是 Agent 系统？

Agent 系统通过 AI 大模型实现智能股票分析，采用 ReAct（Reasoning + Acting）模式，支持调用工具获取实时数据和执行分析。

**关键特征**:
- 单 Agent 模式：简单高效的 ReAct 循环
- 多 Agent 模式：专业化 Agent 协作链
- 策略技能系统：可配置的交易策略
- 工具注册表：标准化的工具调用接口

## 代码位置

| 方面 | 位置 |
|------|------|
| 单 Agent 执行器 | `src/agent/executor.py` |
| 多 Agent 编排器 | `src/agent/orchestrator.py` |
| Agent 工厂 | `src/agent/factory.py` |
| LLM 适配器 | `src/agent/llm_adapter.py` |
| 工具注册表 | `src/agent/tools/registry.py` |
| 专业化 Agent | `src/agent/agents/` |

## 架构模式

### 单 Agent 模式 (agent_arch=single)

```
User Request
    │
    └── AgentExecutor.run()
            │
            └── run_agent_loop()
                    │
                    ├── LLM.generate()
                    │       │
                    │       └── Thought → Action → Observation
                    │
                    └── ToolRegistry.execute_tool()
```

### 多 Agent 模式 (agent_arch=multi)

```
User Request
    │
    └── AgentOrchestrator.run()
            │
            ├── _build_context() - 种子上下文
            │
            ├── AgentChain (根据模式构建)
            │       │
            │       ├── TechnicalAgent → 技术分析
            │       ├── IntelAgent → 情报搜索
            │       ├── RiskAgent → 风险评估 (full/specialist)
            │       └── DecisionAgent → 决策生成
            │
            ├── _apply_risk_override() - 风险否决
            │
            └── _parse_dashboard() - 解析结果
```

## Agent 链模式

| 模式 | Agent 链 | 说明 |
|------|----------|------|
| `quick` | TechnicalAgent → DecisionAgent | 快速分析 |
| `standard` | TechnicalAgent → IntelAgent → DecisionAgent | 标准分析 |
| `full` | TechnicalAgent → IntelAgent → RiskAgent → DecisionAgent | 完整分析 |
| `specialist` | TechnicalAgent → IntelAgent → RiskAgent → SkillAgent → DecisionAgent | 专业模式 |

## 关键组件

### AgentExecutor

单 Agent 执行器，包含 ReAct 执行循环。

```python
class AgentExecutor:
    async def run(
        self,
        stock_code: str,
        context: AgentContext,
        system prompt: str
    ) -> AgentResult:
```

### AgentOrchestrator

多 Agent 编排器，管理 Agent 链执行和结果聚合。

```python
class AgentOrchestrator:
    async def run(
        self,
        stock_code: str,
        context: AgentContext,
        mode: str = "standard"
    ) -> AgentResult:
```

### ToolRegistry

工具注册表，提供 OpenAI 格式的工具声明。

```python
class ToolRegistry:
    def get_tools(self) -> List[dict]:  # OpenAI tools format
    async def execute_tool(self, tool_name: str, arguments: dict) -> Any:
```

## 工具类型

| 工具 | 说明 |
|------|------|
| MarketTools | 行情数据工具 |
| DataTools | 数据获取工具 |
| SearchTools | 搜索工具 |
| AnalysisTools | 分析工具 |
| BacktestTools | 回测工具 |

## 依赖

**本模块依赖**:
- LiteLLM - 统一 LLM 接口
- 外部搜索 API - Tavily、SerpAPI 等
- 股票数据 API - DataFetcherManager

**依赖本模块的**:
- `src/core/pipeline.py` - 核心分析流水线
</