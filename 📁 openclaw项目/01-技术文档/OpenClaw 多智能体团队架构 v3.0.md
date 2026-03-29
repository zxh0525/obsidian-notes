# OpenClaw 多智能体团队架构

> 整理日期：2026-03-29
> 基于：`~/.openclaw/openclaw.json` 实际配置
> 版本：v3.0（现行）

---

## 一、整体架构

OpenClaw 运行一个 Gateway 进程，托管 **15+ 个独立 Agent**，分为三大团队：

| 团队 | Agent数量 | 入口 |
|------|-----------|------|
| **通用团队** | 7 | main |
| **自媒体团队** | 3 | mediayy |
| **股票团队** | 10 | stock_decider |
| **加密货币团队** | 6 | crypto_decider |

每个 Agent 有独立的：
- **Workspace**：文件、AGENTS.md、SOUL.md
- **AgentDir**：认证配置、模型注册
- **Session Store**：聊天历史

---

## 二、通用团队（7人）

### 2.1 成员一览

| Agent ID | 名称 | 核心职责 | 上游 | 下游 |
|----------|------|----------|------|------|
| `main` | 调度员 | 任务拆解、进度督导、结果交付 | 你（海兄） | 全员 |
| `memory` | 记忆管理员 | 维护 MEMORY.md、知识库、记忆检索 | 全员 | 全员（数据中台） |
| `tech` | 技术工程师 | 工具开发、浏览器自动化、API调度 | main | 执行层 |
| `business` | 商业分析师 | 战略定调、商业逻辑、变现路径 | main | invest、writing |
| `growth` | 成长导师 | 学习规划、进度追踪、数据反馈 | main | invest |
| `invest` | 复利研究员 | 投资分析、复利计算、风险评估 | business、growth | quality |
| `life` | 生活体验官 | 生活项目管理、酒吧运营 | main | business |

### 2.2 main（调度员）职责

**核心职能**：任务拆解与进度督导，不直接产出内容。

**调度规则**：
```
用户需求 → main解析意图 → DAG任务拆分 → 按依赖顺序派发
  → 监控执行 → quality审核 → 汇总交付 → 询问满意度
```

**强制汇报规则**（⚠️ 严格遵守）：
- 耗时任务（>5分钟）必须事先告知预计时间
- 每5分钟回报进度
- 有问题立即说，不能"以为没事"
- 没进度更新 = 立即检查并回报

**禁止行为**：
- ❌ 绕 quality 直接交付复杂研究成果
- ❌ main 抢做具体执行任务
- ❌ 让用户"一直等到"

### 2.3 协作链路

```
📱 自媒体链路：
main → memory(查偏好) → writing(撰稿) → quality(审核) → tech(发布) → main(交付)

💰 投资链路：
main → invest(分析) → business(评估) → quality(风控) → main(交付)

🎯 自动化链路：
main → tech(开发) → business(方案) → quality(审核) → main(交付)
```

---

## 三、自媒体团队（3人）

### 3.1 成员一览

| Agent ID | 名称 | 核心职责 |
|----------|------|----------|
| `mediayy` | 负责人 | 热点抓取、账号分析、发布协调 |
| `writing` | 自媒体写手 | 文案撰写、标题优化 |
| `quality` | 质量检查员 | 审核把关、合规扫描 |

**平台**：抖音（61132228487）、小红书、今日头条

### 3.2 工作流程

```
Step 1：mediayy 抓取热点（每天10:00、16:00）
Step 2：writing 根据热点撰写文案（200+字/篇）
Step 3：quality 审核（合规、错别字、爆款元素）
Step 4：mediayy 执行发布（或交海兄手动发布）
Step 5：growth 追踪数据，每周五复盘
```

**内容规范**：
- 抖音：标题≤30字，正文≥1000字，1-5话题
- 小红书：标题≤20字+emoji，正文≥800字
- **敏感词禁则**：赚钱、变现、兼职、副业

---

## 四、股票团队（10人）

### 4.1 决策层

| Agent ID | 名称 | 职责 |
|----------|------|------|
| `stock_decider` | 决策官 | 调度研究员、汇总研判、决策买入/卖出 |

### 4.2 研究员（4人）

| Agent ID | 名称 | 职责 |
|----------|------|------|
| `stock_fundamental` | 基本面研究员 | 财务分析、估值、盈利能力 |
| `stock_industry` | 行业研究员 | 行业趋势、产业链、竞争格局 |
| `stock_news` | 消息面研究员 | 政策、公告、舆情、突发事件 |
| `stock_technical` | 技术面研究员 | 趋势、均线、成交量、形态 |

### 4.3 执行层（5人）

| Agent ID | 名称 | 职责 |
|----------|------|------|
| `stock_sentiment` | 情绪分析师 | 市场情绪、资金流向、情绪指标 |
| `stock_trader` | 交易员 | 交易执行、仓位管理 |
| `stock_risk` | 风控官 | 风险敞口、止损管理 |
| `stock_pm` | 组合经理 | 资产配置、组合优化 |
| `stock_bull` | 多头研究员 | 做多逻辑、上涨催化剂 |
| `stock_bear` | 空头研究员 | 做空逻辑、下跌风险 |

### 4.4 工作模式

**项目一：人工交易（当前模式）**
```
main → stock_decider派发任务 → 4研究员分析 → decider汇总 → 海兄手动操作
```

**项目二：自动化交易（未来模式）**
```
stock_trade.py simulate → 模拟验证 → 对接券商API
```
⚠️ 当前资金1000元，只能模拟。等资金3000+后对接真实API。

---

## 五、加密货币团队（6人）

| Agent ID | 名称 | 职责 |
|----------|------|------|
| `crypto_decider` | 决策官 | 调度研究员、决策交易 |
| `crypto_fundamental` | 基本面研究员 | 链上数据、代币经济、协议分析 |
| `crypto_technical` | 技术面研究员 | K线、均线、形态分析 |
| `crypto_news` | 消息面研究员 | 政策、公告、社交舆情 |
| `crypto_trader` | 交易员 | 交易执行 |
| `crypto_risk` | 风控官 | 风险控制 |

---

## 六、Skills 配置

### 6.1 全局共享 Skills

| Skill | 用途 |
|-------|------|
| `browser` | 网页浏览、数据抓取 |
| `shell` | 命令执行 |
| `memory_search` | 记忆检索 |
| `ffmpeg` | 音视频处理 |
| `github` | GitHub 操作 |
| `automation-workflows` | 自动化工作流 |
| `rag` | 知识库检索 |
| `daily-briefing` | 每日简报 |
| `system-resource-monitor` | 系统监控 |

### 6.2 各 Agent 专用 Skills

| Agent | 特色 Skills |
|-------|-------------|
| `tech` | `coding-agent`, `skill-creator`, `clawhub`, `hooks-auto-save` |
| `growth` | `notion`, `feishu-doc`, `feishu-wiki` |
| `mediayy` | `douyin-publish-v2`, `feishu-sync`, `daily-review` |
| `writing` | `xhs-note-creator`, `SEO`, `Social Media Scheduler` |
| `quality` | `quality-checker` |

---

## 七、调度机制

### 7.1 main 是唯一入口

所有用户需求 → `main` → 拆解 → 派发给对应 Agent

### 7.2 subagent 权限控制

每个 Agent 的 `subagents.allowAgents` 定义了它可以调用的其他 Agent：

```
main.allowAgents: [writing, quality, tech, life, growth, invest, business, memory, stock_decider, mediayy]
stock_decider.allowAgents: [stock_industry, stock_fundamental, stock_technical, stock_news, stock_sentiment, ...]
```

### 7.3 强制审核流程

```
writing产出 → quality审核 → Pass信号 → tech执行 → main交付
invest分析 → quality风控审核 → main交付
```

---

## 八、记忆管理

- **Obsidian 仓库**：`/home/xxh/文档/xxhnote/`
- **项目文档**：`/home/xxh/文档/xxhnote/📁 openclaw项目/`
- **每日记忆**：`memory/YYYY-MM-DD.md`
- **长期记忆**：`MEMORY.md`
- **索引文档**：`📁 openclaw项目/📋 文档索引.md`

---

## 九、消息路由

```
飞书私聊（ou_09f1152d4e0fe27de6cc1580eb2e06da）→ main
股票团队群（oc_xxx）→ stock_decider
加密货币群（oc_xxx）→ crypto_decider
```

---

> 下一步：随着团队升级，持续更新本文档
