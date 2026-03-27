# 接口文档

## CLI 命令行接口

### 主入口 (main.py)

```bash
python main.py [OPTIONS]
```

**全局选项**:
| 参数 | 说明 |
|------|------|
| `--debug` | 启用调试模式，输出详细日志 |
| `--dry-run` | 仅获取数据，不进行 AI 分析 |

**运行模式**:
| 参数 | 说明 |
|------|------|
| `--schedule` | 启用定时任务模式，每日定时执行 |
| `--serve` | 启动 FastAPI 后端服务（同时执行分析任务） |
| `--serve-only` | 仅启动 FastAPI 后端服务，不自动执行分析 |
| `--webui` | 启动 Web 管理界面 |
| `--webui-only` | 仅启动 Web 服务，不执行自动分析 |
| `--market-review` | 仅运行大盘复盘分析 |
| `--backtest` | 运行回测 |

**分析控制**:
| 参数 | 说明 |
|------|------|
| `--stocks <codes>` | 指定要分析的股票代码，逗号分隔 |
| `--no-notify` | 不发送推送通知 |
| `--single-notify` | 启用单股推送模式 |
| `--workers <n>` | 并发线程数 |
| `--force-run` | 跳过交易日检查，强制执行 |

**服务配置**:
| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--port <n>` | 8000 | FastAPI 服务端口 |
| `--host <addr>` | 0.0.0.0 | FastAPI 服务监听地址 |

## REST API 接口

基础路径: `/api/v1`

### 分析接口

#### POST /api/v1/analysis/analyze

触发股票分析

**请求体**:
```json
{
  "stock_codes": ["600519", "000001"],
  "async_mode": false,
  "notify": true
}
```

**响应 (同步模式)**:
```json
{
  "success": true,
  "results": [
    {
      "stock_code": "600519",
      "stock_name": "贵州茅台",
      "decision": "买入",
      "buy_price": 1650.00,
      "stop_loss": 1600.00,
      "target_price": 1750.00,
      "signals": ["MA5>MA10>MA20", "量比放大"]
    }
  ]
}
```

#### GET /api/v1/analysis/tasks

获取任务列表

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `status` | string | 过滤任务状态 |
| `limit` | int | 返回数量限制 |

#### GET /api/v1/analysis/tasks/stream

SSE 实时推送任务进度

#### GET /api/v1/analysis/status/{task_id}

查询任务状态

### 历史记录接口

#### GET /api/v1/history

查询历史分析记录

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| `stock_code` | string | 股票代码过滤 |
| `start_date` | string | 开始日期 |
| `end_date` | string | 结束日期 |
| `limit` | int | 返回数量 |

### 股票数据接口

#### GET /api/v1/stocks

获取股票数据

#### GET /api/v1/stocks/search

搜索股票（代码/名称/拼音）

### 组合管理接口

#### GET /api/v1/portfolio

获取持仓列表

#### POST /api/v1/portfolio

添加持仓记录

#### DELETE /api/v1/portfolio/{id}

删除持仓记录

### Agent 对话接口

#### POST /api/v1/agent/chat

Agent 策略对话

**请求体**:
```json
{
  "message": "帮我分析一下当前市场趋势",
  "stock_code": "600519",
  "skill_id": "bull_trend"
}
```

### 回测接口

#### GET /api/v1/backtest

获取回测结果

#### POST /api/v1/backtest

触发回测

**请求体**:
```json
{
  "stock_code": "600519",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

### 系统配置接口

#### GET /api/v1/system/config

获取系统配置

#### PUT /api/v1/system/config

更新系统配置

## Bot 命令接口

### 飞书/钉钉/Telegram/Discord 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/analyze <code>` | 分析指定股票 | `/analyze 600519` |
| `/batch` | 批量分析自选股 | `/batch` |
| `/chat <question>` | Agent 对话 | `/chat 当前适合买什么` |
| `/ask <question>` | 快速问答 | `/ask 茅台还能买吗` |
| `/market` | 大盘复盘 | `/market` |
| `/status` | 系统状态 | `/status` |
| `/help` | 帮助信息 | `/help` |

## WebSocket/SSE 接口

### 任务进度推送

```typescript
// 客户端订阅
const eventSource = new EventSource('/api/v1/analysis/tasks/stream?task_id=xxx');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.progress, data.message);
};
```

## 数据 Schema

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    stock_code: str              # 股票代码
    stock_name: str              # 股票名称
    decision: str                # 决策：买入/卖出/观望
    buy_price: Optional[float]   # 买入价
    stop_loss: Optional[float]   # 止损价
    target_price: Optional[float] # 目标价
    signals: List[str]           # 信号列表
    analysis: str                 # 分析内容
    timestamp: datetime           # 分析时间
```

### AgentContext

```python
@dataclass
class AgentContext:
    stock_code: str
    stock_name: str
    realtime_quote: dict
    chip_distribution: dict
    trend_analysis: dict
    news_intel: List[dict]
    history_context: List[dict]
```

### StageResult

```python
@dataclass
class StageResult:
    agent_name: str
    opinion: AgentOpinion
    timestamp: datetime
    success: bool
    error: Optional[str]
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| `STOCK_NOT_FOUND` | 股票代码不存在 |
| `ANALYSIS_IN_PROGRESS` | 分析正在进行 |
| `DATA_FETCH_FAILED` | 数据获取失败 |
| `AI_ANALYSIS_FAILED` | AI 分析失败 |
| `NOTIFICATION_FAILED` | 通知发送失败 |
| `UNAUTHORIZED` | 未授权访问 |
| `PORTFOLIO_BUSY` | 账本正忙（高并发冲突） |
