# DataFetcherManager

多数据源管理器，实现股票数据的故障自动切换，确保数据获取的可靠性。

## 什么是 DataFetcherManager？

DataFetcherManager 采用策略模式和故障切换机制，管理多个股票数据源，按优先级尝试获取数据，单一数据源失败时自动切换到下一个。

**关键特征**:
- 多数据源优先级管理
- 故障自动切换
- 熔断保护机制
- 字段标准化

## 代码位置

| 方面 | 位置 |
|------|------|
| 实现 | `data_provider/base.py` |
| 数据源 | `data_provider/` |

## 数据源优先级

| 优先级 | 数据源 | 说明 |
|--------|--------|------|
| 0 | EfinanceFetcher | efinance 库 |
| 1 | AkShareFetcher | AkShare 库 |
| 2 | TushareFetcher | Tushare Pro |
| 2 | PytdxFetcher | Pytdx 通达信 |
| 3 | BaostockFetcher | Baostock 库 |
| 4 | YFinanceFetcher | YFinance（美股） |

## 核心接口

### get_daily_data()

获取日线数据。

```python
async def get_daily_data(
    stock_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
```

**流程**:
1. 按优先级遍历数据源
2. 尝试获取数据
3. 成功则标准化字段名并返回
4. 失败则切换到下一个数据源
5. 所有数据源失败则抛出异常

### get_realtime_quote()

获取实时行情。

```python
async def get_realtime_quote(stock_code: str) -> dict:
```

### get_chip_distribution()

获取筹码分布。

```python
async def get_chip_distribution(stock_code: str) -> dict:
```

## 熔断保护

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 60):
        ...

    async def call(self, func, *args, **kwargs):
        ...
```

## 依赖

**本模块依赖**:
- 各数据源 Fetcher（efinance、akshare、tushare、yfinance 等）
- 外部数据 API

**依赖本模块的**:
- `src/core/pipeline.py` - 核心分析流水线
- `src/agent/tools/market_tools.py` - Agent 市场工具
</