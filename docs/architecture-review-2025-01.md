# 创作工作室架构审视报告

> 审视日期：2025-01-28
> 状态：**已确认，待实施**

---

## 执行摘要

**当前评分**：7.0/10 — 架构设计优秀，但存在关键协作缺口

**优化后预期**：8.5/10

本次审视覆盖：
- 四部门架构和目录结构
- Agent 职责定义
- Skill 功能设计
- 从策划→创作→发布的完整流程

---

## 一、发现的问题及解决方案

| 问题 | 解决方案 | 状态 |
|------|----------|------|
| 缺失修订职责定义 | chapter-writer 增加修订模式 | ✅ 已确认 |
| 蓝图变更无同步机制 | 利用 Git + 新增 blueprint-sync-checker | ✅ 已确认 |
| 缺失"策划完成"检查点 | 蓝图状态管理（drafting/ready） | ✅ 已确认 |
| entity-manager 职责模糊 | 删除，职责合并到其他 Agent | ✅ 已确认 |
| 跨章一致性检查不全面 | 扩展 chapter-auditor 职责 | ✅ 已确认 |
| Git 规范已定义但未实现 | 各 Agent 补全 Git 提交实现 | ✅ 已确认 |

---

## 二、确认的设计决策

### 2.1 蓝图状态管理

```
                    修改蓝图
                       │
                       ▼
┌─────────┐  审核通过  ┌─────────┐
│ drafting │ ────────► │  ready  │
│ (策划中) │           │(可创作) │
└─────────┘  ◄──────── └─────────┘
                修改蓝图
```

| 状态 | 设置权限 | 触发条件 |
|------|----------|----------|
| `drafting` | 蓝图规划智能体 | 任何蓝图文件被修改 |
| `ready` | **仅** blueprint-auditor | 审核通过 |

**存储位置**：`proposal.md` 的 YAML front matter

```yaml
---
project_id: xuanhuan_001
title: 《XXX》
blueprint_status: drafting  # drafting / ready
---
```

### 2.2 Git 版本管理

- **规范位置**：`specs/git-convention.md`（已存在）
- **决策**：利用 Git 进行版本控制和变更追踪
  - 蓝图变更通过 `git diff` 识别
  - 不需要单独的 changelog 或 history 文件
- **问题**：各 Agent 未实现规范
- **行动**：补全各 Agent 的 Git 提交实现

### 2.3 chapter-writer 双模式

| 模式 | 触发方式 | 输入 | 输出 |
|------|----------|------|------|
| 创作模式 | 默认 / 用户指定 | 大纲 + 上下文 | draft 章节 |
| 修订模式 | 用户指定 / 检测到 pending 状态 | pending 章节 + 审核报告 | revised 章节 |

**两种触发方式都支持**

### 2.4 删除 entity-manager

职责合并：

| 原功能 | 合并到 |
|--------|--------|
| 创作时更新实体库 | chapter-writer |
| 跨章一致性检查 | chapter-auditor |

### 2.5 blueprint-sync-checker

- **触发方式**：用户主动调用
- **实现方式**：利用 `git diff` 识别蓝图变更，分析影响范围
- **输出**：受影响章节清单 + 修订优先级

### 2.6 不需要交接单

- 用蓝图状态（`drafting`/`ready`）替代交接概念
- 蓝图随时可调整，通过 Git 追踪变更

---

## 三、优化后的团队架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        策划团队 (Blueprints)                      │
├─────────────────────────────────────────────────────────────────┤
│ worldview-architect → character-designer → outline-architect    │
│         │                    │                    │             │
│         └──────── 修改蓝图 → status: drafting ────┘             │
│                              ↓                                   │
│              blueprint-auditor (审核通过 → status: ready)        │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                        创作团队 (Productions)                     │
├─────────────────────────────────────────────────────────────────┤
│ production-initializer                                           │
│         ↓                                                        │
│ chapter-writer (创作/修订) ←─────────────┐                       │
│         ↓                                │                       │
│ chapter-auditor (单章审核 + 跨章一致性)   │                       │
│         ↓                                │                       │
│     [pending] ───────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                        发布团队 (Releases)                        │
├─────────────────────────────────────────────────────────────────┤
│ release-manager → format-exporter / audiobook-optimizer          │
│                 → video-director → video-assembler               │
└─────────────────────────────────────────────────────────────────┘
```

**Agent 数量变化**：
- 策划团队：4 个（不变）
- 创作团队：3 个（删除 entity-manager）
- 发布团队：4 个（不变）

---

## 四、实施清单

### 第一阶段：核心流程

| 序号 | 任务 | 类型 | 文件 |
|------|------|------|------|
| 1 | proposal 模板增加 `blueprint_status` 字段 | 修改 | `templates/proposal-template.md` |
| 2 | 蓝图规划智能体：修改后设置 status: drafting | 修改 | `agents/worldview-architect.md`<br>`agents/character-designer.md`<br>`agents/outline-architect.md` |
| 3 | blueprint-auditor：审核通过后设置 status: ready | 修改 | `skills/blueprint-auditor/SKILL.md` |
| 4 | chapter-writer：增加修订模式 + 蓝图状态检查 | 修改 | `agents/chapter-writer.md` |
| 5 | chapter-auditor：增加跨章一致性检查 | 修改 | `agents/chapter-auditor.md` |
| 6 | 删除 entity-manager | 删除 | `agents/entity-manager.md` |

### 第二阶段：版本管理

| 序号 | 任务 | 类型 | 文件 |
|------|------|------|------|
| 7 | 各 Agent 补全 Git 提交实现 | 修改 | 所有 Agent |
| 8 | 新增 blueprint-sync-checker Skill | 新增 | `skills/blueprint-sync-checker/SKILL.md` |

---

## 五、预期效果

| 维度 | 当前 | 优化后 |
|------|------|--------|
| Agent 职责清晰度 | 7.5/10 | 9/10 |
| 策划→创作衔接 | 5.5/10 | 8.5/10 |
| 蓝图变更同步 | 3/10 | 8/10 |
| **总体评分** | **7.0/10** | **8.5/10** |

---

## 修订记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2025-01-28 | 0.1 | 初版审视报告 |
| 2025-01-28 | 1.0 | 讨论后确认设计决策，更新实施清单 |
