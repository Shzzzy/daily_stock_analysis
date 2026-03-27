# StockAnalysisPipeline

股票分析流水线是系统的核心编排模块，协调整个股票分析流程。

## 什么是 StockAnalysisPipeline？

StockAnalysisPipeline 负责管理从数据获取到通知推送的完整分析流程，支持传统 AI 分析模式和 Agent 模式两种分析方式。

**关键特征**:
- 线程池并发处理多只股票
- 支持断点续传（数据获取失败后可重试）
- 单股分析完成后立即推送（可选）
- 完整分析后汇总推送

## 代码位置

| 方面 | 位置 |
|------|------|
| 实现 | `src/core/pipeline.py` |
| 入口 | `main.py` |
| 测试 | `tests/` |

## 核心流程

```
run_full_analysis()
    │
    ├── 刷新股票列表 (_refresh_stock_list)
    │
    ├── 交易日过滤 (_compute_trading_day_filter)
    │
    └── pipeline.run(stock_codes)
            │
            ├── ThreadPoolExecutor (max_workers=3)
            │
            └── process_single_stock()
                    │
                    ├── fetch_and_save_data()
                    │       │
                    │       └── DataFetcherManager.get_daily_data()
                    │
                    ├── analyze_stock()
                    │       │
                    │       ├── 传统模式: GeminiAnalyzer.analyze()
                    │       │
                    │       └── Agent 模式: _analyze_with_agent()
                    │
                    ├── 保存分析历史 (DatabaseManager)
                    │
                    └── 单股推送 (可选, NotificationService)
```

## 关键方法

### run()

运行完整分析流程，使用线程池并发处理多只股票。

```python
def run(self, stock_codes: List[str]) -> List[AnalysisResult]:
```

### process_single_stock()

处理单只股票的完整流程。

```python
async def process_single_stock(
    self,
    stock_code: str,
    task_id: Optional[str] = None
) -> Tuple[Optional[str], Optional[AnalysisResult], Optional[str]]:
```

### _analyze_with_agent()

Agent 模式分析，调用 AgentExecutor/Orchestrator。

```python
async def _analyze_with_agent(
    self,
    stock_code: str,
    context: dict,
    agent_executor: AgentExecutor
) -> AgentResult:
```

## 依赖

**本模块依赖**:
- `DataFetcherManager` - 多数据源管理
- `GeminiAnalyzer` / `AgentExecutor` - AI 分析
- `NotificationService` - 通知服务
- `SearchService` - 搜索服务
- `DatabaseManager` - 数据持久化

**依赖本模块的**:
- `main.py` - CLI 入口
- `api/v1/endpoints/analysis.py` - API 端点
</