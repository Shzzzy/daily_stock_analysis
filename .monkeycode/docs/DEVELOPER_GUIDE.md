# 开发者指南

## 项目目的

股票智能分析系统是一个基于 AI 大模型的 A股/港股/美股自选股智能分析系统，用于自动化股票分析和报告推送。

**核心职责**:
- 多数据源股票行情获取
- AI 驱动的技术分析和决策生成
- 多渠道自动化报告推送
- Agent 策略对话和回测验证

**相关系统**:
- 外部 AI 模型服务商（AIHubMix、Gemini、OpenAI）
- 股票数据提供商（Tushare、AkShare、YFinance）
- 消息通知平台（企业微信、飞书、Telegram）

## 环境搭建

### 前置条件

- Python 3.10+
- Git
- pip 或 conda

### 安装

```bash
# 克隆仓库
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的值
```

### 环境变量

| 变量 | 必需 | 描述 | 示例 |
|------|------|------|------|
| `STOCK_LIST` | 是 | 自选股代码 | `600519,hk00700,AAPL` |
| `GEMINI_API_KEY` | 推荐 | Gemini API Key | `AIza...` |
| `TAVILY_API_KEY` | 推荐 | Tavily 搜索 API | `tvly...` |
| `WECHAT_WEBHOOK_URL` | 可选 | 企业微信 Webhook | `https://...` |
| `FEISHU_WEBHOOK_URL` | 可选 | 飞书 Webhook | `https://...` |
| `TELEGRAM_BOT_TOKEN` | 可选 | Telegram Bot Token | `123:ABC` |
| `TELEGRAM_CHAT_ID` | 可选 | Telegram Chat ID | `-100123456` |

### 运行

```bash
# 单次分析
python main.py

# 调试模式
python main.py --debug

# 定时任务模式
python main.py --schedule

# API 服务模式
python main.py --serve

# Web 管理界面
python main.py --webui

# 大盘复盘
python main.py --market-review

# 回测
python main.py --backtest
```

### API 服务

```bash
# 启动 API 服务
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## 开发工作流

### 代码质量工具

| 工具 | 命令 | 目的 |
|------|------|------|
| pytest | `python -m pytest` | 单元测试 |
| flake8 | `flake8` | 代码检查 |
| py_compile | `python -m py_compile <file>` | 语法检查 |

### 提交前检查

```bash
# 运行 CI gate 检查
./scripts/ci_gate.sh

# 语法检查
python -m py_compile <changed_python_files>

# 运行测试
python -m pytest -m "not network"
```

### 分支策略

- `main` - 生产就绪代码
- `feature/*` - 新功能
- `fix/*` - Bug 修复

## 常见任务

### 添加新的数据源

**需修改的文件**:
1. `data_provider/` - 添加新的 Fetcher 类
2. `data_provider/base.py` - 注册新数据源

**步骤**:
1. 在 `data_provider/` 下创建新的 fetcher 文件
2. 继承 `BaseFetcher` 并实现必要方法
3. 在 `DataFetcherManager` 中注册新数据源

### 添加新的通知渠道

**需修改的文件**:
1. `src/notification_sender/` - 添加新的 Sender 类
2. `src/notification.py` - 注册新渠道

**步骤**:
1. 在 `src/notification_sender/` 创建新的 sender 文件
2. 继承 `BaseSender` 并实现 `send()` 方法
3. 在 `NotificationService` 中注册新渠道

### 添加新的 Agent 工具

**需修改的文件**:
1. `src/agent/tools/` - 添加新的工具类
2. `src/agent/tools/registry.py` - 注册新工具

**步骤**:
1. 实现新的工具类，继承相应基类
2. 在 `ToolRegistry` 中注册工具
3. 添加工具的 OpenAI 格式声明

### 添加新的交易策略

**需修改的文件**:
1. `src/agent/strategies/` - 添加策略实现
2. `src/agent/skills/` - 添加技能配置

### 修复 Bug

**流程**:
1. 编写复现 bug 的失败测试
2. 在代码中定位根因
3. 用最小改动修复
4. 验证测试通过

## 编码规范

### 文件组织
- 每个文件包含一个主要类或函数
- 相关文件放在同一目录
- 测试文件与源码同目录

### 命名

| 类型 | 约定 | 示例 |
|------|------|------|
| 文件 | snake_case | `stock_analyzer.py` |
| 类 | PascalCase | `StockAnalysisPipeline` |
| 函数 | snake_case | `get_daily_data` |
| 常量 | SCREAMING_SNAKE | `MAX_WORKERS` |

### 错误处理

```python
# 推荐：特定错误类型 + 明确消息
raise ValueError(f"Stock code {code} not found in database")

# 避免：通用错误
raise Exception("Something went wrong")
```

### 日志

```python
# 包含上下文
logger.info(f"Analyzing stock {stock_code}", extra={"trend": trend})

# 使用适当级别
logger.debug()  # 开发详情
logger.info()   # 正常操作
logger.warning()  # 可恢复问题
logger.error()  # 需要关注的故障
```

### 测试
- 测试文件: `[name].test.py` 与源码同目录
- 使用 `@pytest.mark` 标记测试类型
- 使用 `pytest -m "not network"` 跳过网络测试

## 核心模块

### src/core/pipeline.py

股票分析流水线，协调整个分析流程。

### src/agent/

AI Agent 模块，包含：
- `executor.py` - 单 Agent 执行器
- `orchestrator.py` - 多 Agent 编排器
- `agents/` - 专业化 Agent 实现

### data_provider/

多数据源适配层，实现故障自动切换。

### src/notification_sender/

通知渠道发送器，支持多平台推送。
