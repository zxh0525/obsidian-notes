# OpenClaw 自动化能力全景

> 整理日期：2026-03-29
> 用途：帮助团队了解 OpenClaw 有哪些自动化能力，如何组合使用
> 基于：OpenClaw v2026.3.22 + 实际部署 Skills

---

## 一、自动化核心四大件

| 能力 | 触发方式 | 用途 |
|------|----------|------|
| **Skills** | 人工调用 / Agent 调用 | 封装好的工具，SOP化 |
| **Hooks** | Gateway 事件自动触发 | 事件驱动，如 session 创建、任务完成 |
| **Cron** | 定时（精确到分钟） | 每日简报、定时发布、数据监控 |
| **Agent Loop** | 人工 / 消息 / Cron 触发 | 子 Agent 并行任务 |

---

## 二、Skills 系统（已部署）

Skills 是封装好的工具，每个 Agent 可以配置自己的 Skills 列表。

### 2.1 已安装 Skills 总览

**🔧 通用工具**
| Skill | 功能 |
|-------|------|
| `browser` | 网页自动化（浏览、截图、表单填写） |
| `shell` | 执行系统命令 |
| `ffmpeg` | 音视频处理（格式转换、剪辑） |
| `github` | GitHub Issues/PR/CI 操作 |
| `automation-workflows` | Zapier/Make/n8n 工作流设计 |
| `rag` | 知识库检索增强生成 |

**📊 数据与监控**
| Skill | 功能 |
|-------|------|
| `system-resource-monitor` | 系统资源监控（CPU/内存/磁盘） |
| `daily-briefing` | 每日简报（天气+日历+提醒） |
| `daily-review` | 每日复盘（工作日志+经验教训） |

**📱 自媒体运营**
| Skill | 功能 |
|-------|------|
| `douyin-publish-v2` | 抖音文章发布（标题+摘要+正文+AI头图） |
| `xiaohongshu-publish` | 小红书发布 |
| `feishu-sync` | 飞书同步 |
| `Social Media Scheduler` | 社交媒体定时发布 |

**📁 知识管理**
| Skill | 功能 |
|-------|------|
| `memory_search` | 记忆检索（语义搜索 MEMORY.md） |
| `obsidian` | Obsidian 笔记操作 |
| `feishu-doc` | 飞书文档读写 |
| `feishu-wiki` | 飞书知识库 |
| `feishu-drive` | 飞书云盘 |

**🛠️ 开发与调试**
| Skill | 功能 |
|-------|------|
| `skill-creator` | 创建/编辑/审计 AgentSkill |
| `coding-agent` | 编程助手 |
| `clawhub` | OpenClaw 技能市场 |
| `hooks-auto-save` | Hooks 自动保存 |

**📄 文档与媒体**
| Skill | 功能 |
|-------|------|
| `pdf` | PDF 处理 |
| `ppt-generator` | PPT 生成 |
| `image_generate` | 图片生成（AI绘图） |
| `video-frames` | 视频抽帧 |

**📈 效率工具**
| Skill | 功能 |
|-------|------|
| `SEO` | SEO 优化分析 |
| `quality-checker` | 内容质量检查 |
| `content-workflow` | 内容生产工作流 |
| `content-publishing` | 内容发布工作流 |

### 2.2 如何使用 Skills

**方式一：Agent 自动调用**
```
main 派发给 tech → tech 自动识别需要用 browser skill → 执行
```

**方式二：人工触发**
```
对 main 说："帮我查一下今天股市" → main 调用 stock_news agent
```

**方式三：创建新 Skill**
```
向 main 说："帮我创建一个 xxx 的 Skill" → tech 执行 skill-creator
```

---

## 三、Hooks 系统（事件触发）

Hooks 让你在特定事件发生时自动执行动作。

### 3.1 可用 Hook 点

| Hook 点 | 触发时机 |
|---------|----------|
| `before_model_resolve` | 模型解析前 |
| `before_prompt_build` | Prompt 构建前 |
| `before_tool_call` | 工具调用前 |
| `after_agent_run` | Agent 执行完成后 |
| `on_cron` | Cron 定时触发 |
| `on_agent_start` | Agent 开始时 |
| `on_agent_end` | Agent 结束时 |
| `on_error` | 错误发生时 |

### 3.2 已配置的 Hooks

**hooks-auto-save**
- 路径：`~/.openclaw/extensions/hooks-auto-save/`
- 功能：自动保存 session 上下文到 memory/

**session-memory hook**
- 触发：每个 `/new` 时自动保存会话上下文

### 3.3 配置示例

```json
{
  "agents": {
    "teams": {
      "heartbeat": { "enabled": false },
      "hooks": {
        "on_complete": "http://localhost:18789/api/cron/wake",
        "on_error": "http://localhost:18789/api/cron/wake"
      }
    }
  }
}
```

---

## 四、Cron 定时任务

### 4.1 已配置的定时任务

| 任务 | 时间 | 执行 Agent | 功能 |
|------|------|-----------|------|
| 每日读书提醒 | 08:00 | growth | 发送《时间的秩序》阅读提醒 |
| 每周六抖音复盘 | 10:00 | growth | 自动复盘本周数据 |
| 每日简报 | 每天 | daily-briefing | 天气+日历+提醒 |

### 4.2 Cron 配置命令

```bash
# 查看所有定时任务
openclaw cron list

# 编辑任务
openclaw cron edit <id> --to "chat:oc_xxx"

# 添加新任务
openclaw cron add "*/30 * * * *" --agent main --prompt "检查股票价格"
```

### 4.3 delivery 配置要点

⚠️ **必须指定 `--to chat:xxx`**，不能只靠 `--channel feishu`
```
openclaw cron add "0 10 * * 6" \
  --agent growth \
  --to "chat:oc_d9ad2f81f0b84cd9b2b5afce20bd2966" \
  --prompt "执行每周复盘"
```

---

## 五、Browser 自动化

### 5.1 两种模式

| 模式 | 说明 |
|------|------|
| `openclaw`（独立浏览器） | OpenClaw 管理的隔离浏览器，安全不影响日常 |
| `chrome`（扩展 relay） | 通过浏览器扩展控制已打开的 Chrome |

### 5.2 支持操作

- 快照、截图、点击、输入
- PDF 生成
- 表单自动填写
- 数据抓取

### 5.3 Skill

通过 `browser` skill 使用：
```bash
# 截图
openclaw browser screenshot https://example.com

# 点击元素
openclaw browser click "登录按钮"
```

---

## 六、Agent 协作模式

### 6.1 subagent 并行

main 可以同时派发多个 subagent，并行执行：
```
main → stock_fundamental（并行）→
       stock_industry（并行）→ stock_decider 汇总
       stock_technical（并行）→
       stock_news（并行）→
```

### 6.2 sessions_spawn（隔离子会话）

```python
sessions_spawn(
  task="分析这只股票",
  runtime="subagent",
  agentId="stock_fundamental"
)
```

### 6.3 sessions_yield（让出主会话）

当需要等待 subagent 结果时：
```
sessions_yield() → 等待 subagent 完成 → 接收结果继续
```

---

## 七、Memory 系统

### 7.1 三层架构

| 层级 | 文件 | 用途 |
|------|------|------|
| 实时上下文 | 对话 session | 当前任务上下文 |
| 每日记忆 | `memory/YYYY-MM-DD.md` | 当天工作记录 |
| 长期记忆 | `MEMORY.md` | 重要决策、偏好、规划 |

### 7.2 检索方式

```python
memory_search(query="海兄的股票偏好")  # 语义搜索
memory_get(path="memory/2026-03-29.md", from=1, lines=50)  # 精确读取
```

### 7.3 自动 flush

OpenClaw 在 compaction 前会自动提醒写记忆。

---

## 八、实战组合示例

### 8.1 抖音定时发布

```
Cron(12:00) → mediayy → douyin-publish-v2 Skill → 飞书通知海兄
```

### 8.2 每日股票监控

```
Cron(09:20) → main → stock_news → tech抓取数据 → 飞书推送
```

### 8.3 内容自动生产

```
热点发现 → writing撰稿 → quality审核 → tech生成配图 → mediayy发布
```

---

## 九、扩展方式

### 9.1 安装新 Skill

1. 去 [clawhub.com](https://clawhub.com) 找 Skill
2. 或用 `skill-creator` 自己创建
3. 在 `openclaw.json` 的 agents.list 中添加 skills

### 9.2 添加新 Agent

```bash
openclaw agents add stock_analyst \
  --workspace /path/to/workspace \
  --skills browser,memory_search,shell
```

### 9.3 MCP 工具扩展

OpenClaw 支持 MCP (Model Context Protocol)，可接入更多外部工具。

---

> 持续更新中，有新能力随时补充
