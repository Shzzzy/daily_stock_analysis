# 股票智能分析系统文档

股票智能分析系统是一个基于 AI 大模型的 A股/港股/美股自选股智能分析系统，每日自动分析并推送「决策仪表盘」。

**快速链接**: [架构](./ARCHITECTURE.md) | [接口](./INTERFACES.md) | [开发者指南](./DEVELOPER_GUIDE.md)

---

## 核心文档

### [架构](./ARCHITECTURE.md)
系统设计、技术栈、组件结构和数据流程。从这里开始了解系统如何运作。

### [接口](./INTERFACES.md)
REST API、CLI 命令、Bot 命令和数据 Schema。集成或使用此系统的参考。

### [开发者指南](./DEVELOPER_GUIDE.md)
环境搭建、开发工作流、编码规范和常见任务。贡献者必读。

---

## 模块

| 模块 | 描述 | README |
|------|------|--------|
| `src/core/` | 核心流程编排（股票分析流水线） | [pipeline.py](../src/core/pipeline.py) |
| `src/agent/` | AI Agent 模块（执行、编排、工具） | [executor.py](../src/agent/executor.py) |
| `data_provider/` | 多数据源适配与故障切换 | [base.py](../data_provider/base.py) |
| `src/notification_sender/` | 多渠道通知发送器 | [notification.py](../src/notification.py) |
| `src/services/` | 业务服务层 | [services/](../src/services/) |
| `src/repositories/` | 数据访问层 | [repositories/](../src/repositories/) |
| `api/` | FastAPI REST 接口 | [app.py](../api/app.py) |
| `bot/` | 机器人接入（飞书/钉钉/Telegram） | [handler.py](../bot/handler.py) |

---

## 核心概念

理解这些领域概念有助于导航代码库：

| 概念 | 描述 |
|------|------|
| [StockAnalysisPipeline](./专有概念/StockAnalysisPipeline.md) | 核心分析流水线，协调数据获取、AI 分析和通知 |
| [Agent 系统](./专有概念/Agent系统.md) | 多 Agent 协作架构，支持单/多 Agent 模式 |
| [DataFetcherManager](./专有概念/DataFetcherManager.md) | 多数据源管理器，实现故障自动切换 |
| [决策仪表盘](./专有概念/决策仪表盘.md) | AI 分析输出的结构化决策建议 |

---

## 入门指南

### 项目新人？

按此路径学习：
1. **[架构](./ARCHITECTURE.md)** - 了解全局
2. **[核心概念](#核心概念)** - 学习领域术语
3. **[开发者指南](./DEVELOPER_GUIDE.md)** - 搭建环境
4. **[接口](./INTERFACES.md)** - 探索公开 API

### 需要集成？

1. **[接口](./INTERFACES.md)** - API 契约和认证
2. **[架构](./ARCHITECTURE.md)** - 系统边界和数据流

### 首次贡献？

1. **[开发者指南](./DEVELOPER_GUIDE.md)** - 搭建和工作流
2. **[常见任务](./DEVELOPER_GUIDE.md#常见任务)** - 分步指南

---

## 快速参考

### 命令

```bash
python main.py              # 单次分析
python main.py --debug      # 调试模式
python main.py --schedule   # 定时任务
python main.py --serve      # API 服务
python main.py --backtest   # 回测
```

### 重要文件

| 文件 | 目的 |
|------|------|
| `main.py` | CLI 主入口 |
| `server.py` | FastAPI 服务入口 |
| `src/core/pipeline.py` | 核心分析流水线 |
| `src/agent/executor.py` | Agent 执行器 |
| `.env.example` | 环境变量模板 |
