
```markdown
# MiniMax Coding Plan 基础版 + OpenClaw Agent 团队优化指南

## 问题诊断

**核心矛盾**：MiniMax Coding Plan 基础版提供 **40 prompts/5小时** 的配额，但 OpenClaw Agent 团队的默认配置会在 **10-20 分钟内耗尽** 该额度。

**消耗黑洞**：
- Agent 心跳轮询：每 3-5 秒 1 次请求 → 3600+ prompts/5h
- 子 Agent 独立调用：每个子任务单独计数
- 工具输出累积：超大上下文触发重试/超时

---

## 立即生效：5 大保命优化

### 1. 禁用轮询，改用 Hooks 回调（效果最显著）

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "teams": {
      "heartbeat": {
        "enabled": false,
        "interval": 300000
      },
      "mode": "hook",
      "hooks": {
        "on_complete": "http://localhost:18789/api/cron/wake",
        "on_error": "http://localhost:18789/api/cron/wake"
      }
    }
  }
}
```

**效果**：从 3600 次/5h 降至 1-5 次/5h（**720 倍提升**）

---

### 2. 强制批量处理模式

```json
{
  "agents": {
    "defaults": {
      "batchMode": true,
      "maxSubTasks": 10,
      "consolidateOutput": true
    }
  }
}
```

**使用方式**：
```bash
# 错误：3 次调用，消耗 3 prompts
openclaw agent --message "检查状态"
openclaw agent --message "读取日志"  
openclaw agent --message "发送邮件"

# 正确：1 次调用，消耗 1 prompt
openclaw agent --message "批量执行：1)检查状态 2)读取日志 3)发送邮件，汇总返回"
```

**效果**：10 倍提升

---

### 3. 启用本地缓存（零成本复用）

```bash
# 安装优化 Skill
openclaw skills install token-optimizer
```

```json
{
  "agents": {
    "defaults": {
      "cache": {
        "enabled": true,
        "ttl": 7200,
        "maxSize": 500,
        "strategy": "semantic"
      }
    }
  },
  "skills": {
    "token-optimizer": {
      "enabled": true,
      "dynamicToolLoading": true,
      "cachePrompt": true,
      "cacheTtl": "2h"
    }
  }
}
```

**效果**：缓存命中时不消耗 prompts，整体降低 70%+

---

### 4. 分层模型策略（M2.5 + M2 Free）

```json
{
  "agents": {
    "orchestrator": {
      "model": {
        "provider": "minimax",
        "model_id": "minimax/minimax-m2.5"
      }
    },
    "workers": {
      "model": {
        "provider": "minimax",
        "model_id": "minimax/minimax-m2",
        "fallback": "minimax/minimax-m2.1"
      },
      "rateLimit": {
        "requestsPerMinute": 10
      }
    }
  }
}
```

**说明**：
- 主 Agent（Orchestrator）：使用 Coding Plan 额度，负责决策
- 子 Agent（Workers）：使用 **MiniMax M2 Free**（零成本），限流 10-20 RPM

---

### 5. 激进上下文压缩

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "targetTokens": 20000,
        "strategy": "aggressive",
        "keepEssentials": ["system", "last_3_turns"]
      },
      "tools": {
        "outputMaxChars": 2000
      }
    }
  }
}
```

**效果**：避免超时重试，减少无效调用

---

## 配额管理与监控

### 实时监控
```bash
# 查看 MiniMax 额度
openclaw /status minimax

# 设置告警（剩余 5 prompts）
openclaw config set alerts.minimax.threshold=5
```

### 错峰使用策略
- **高强度任务**：安排在额度刷新后 30 分钟内
- **避免高峰**：14:00-18:00（UTC+8）期间限流更严格


---

## 关键配置速查

```bash
# 1. 立即禁用轮询
openclaw config set agents.teams.heartbeat.enabled=false

# 2. 启用批量模式
openclaw config set agents.defaults.batchMode=true

# 3. 安装缓存 Skill
openclaw skills install token-optimizer

# 4. 查看当前额度
openclaw /status minimax
```

---

> **核心原则**：MiniMax Coding Plan 基础版的 40 prompts/5h 不是限制，而是强制你优化架构设计。通过 Hooks 回调、批量处理和分层模型，完全可以在零额外成本下支撑生产级 Agent 团队。
