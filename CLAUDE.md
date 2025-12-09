# CLAUDE.md

本文件为 Claude Code 在本 Plugin 中工作时的指导文档。

---

## 项目概述

**Novel Writing Studio Plugin** - 提供从素材分析到小说发布的全自动化创作流程，支持多种类型小说创作。

### 四部门架构

```
素材池(Pools) → 策划(Blueprints) → 制作(Productions) → 发布(Releases)
```

### 三层组件体系

| 层级 | 组件类型 | 说明 |
|------|----------|------|
| Skills | 自动激活 | 分析、检查、导出工具 |
| Agents | 显式调用 | 策划/设计/创作/审核专家 |
| Commands | 批量操作 | 用户快捷指令 |

---

## 核心规范

> **所有 Agent/Command/Skill 必须遵循以下规范文件：**

| 规范 | 文件 | 说明 |
|------|------|------|
| 目录结构 | `specs/directory-structure.md` | 四部门路径、输入输出位置、project_id 规则 |
| 书写风格 | `specs/writing-style.md` | 标点、数字、段落、对话、YAML格式 |
| 实体格式 | `templates/entities-template.md` | 实体库表格格式 |

---

## 知识包系统

### 目录结构

```
libraries/knowledge/
├── _base/                    # 通用知识（始终加载）
│   ├── story-structures.md   # 故事结构（三幕/英雄之旅等）
│   └── character-archetypes.md # 角色原型
│
├── chinese-webnovel/         # 中文网文知识包
│   ├── xuanhuan-patterns.md  # 玄幻套路
│   ├── power-systems.md      # 境界体系
│   └── goldfinger-types.md   # 金手指类型
│
└── {other-packs}/            # 其他知识包（自动发现）
```

### 知识加载规则

1. **`_base/`** 目录下的文件**始终加载**
2. **其他目录**根据用户需求关键词**自动匹配**：
   - "玄幻/网文/修仙/废柴流" → `chinese-webnovel/`
   - "异世界/轻小说/转生" → `japanese-lightnovel/`
   - "fantasy/epic" → `western-fantasy/`
3. 如果没有匹配的知识包，仅使用 `_base/` 中的通用知识

---

## Agent 工作模式

### 输入源
1. 用户工作区文件（`blueprints/`、`productions/`）
2. Plugin 知识库（`libraries/knowledge/`）
3. 用户的自然语言指令

### 输出目标
- 生成文件到用户工作区
- 更新实体库
- **不写入 Plugin 目录**

### 知识发现流程

```
1. 始终读取 libraries/knowledge/_base/*.md
2. Glob libraries/knowledge/*/ 获取所有知识包目录
3. 根据用户需求关键词匹配目录名
4. 读取匹配目录下的相关 .md 文件
```

### 协作流程

```
pool-analyzer → worldview-architect → character-designer → outline-architect
                                                               ↓
revision-writer ← chapter-auditor ← chapter-writer ← production-initializer
                                                               ↓
                                                        format-exporter
```

---

## Commands 快速参考

| 命令 | 部门 | 功能 |
|------|------|------|
| `/workspace-init` | 跨部门 | 初始化工作区目录结构 |
| `/write-chapters 1-10` | Productions | 批量创作章节 |
| `/review-batch 1-10` | Releases | 批量审核章节 |
| `/export-all` | Releases | 一键导出所有格式 |

---

## 调试指南

### 验证 Agent 输出
1. 检查文件是否生成到正确的用户工作区目录（参见 `specs/directory-structure.md`）
2. 确认实体库格式正确（参见 `templates/entities-template.md`）
3. 验证章节遵守书写规范（参见 `specs/writing-style.md`）

### 常见问题
- **路径错误**: 参考 `specs/directory-structure.md` 确认正确路径
- **格式不符**: 检查 `specs/writing-style.md` 规范
- **实体不一致**: 检查 `productions/{project_id}/data/entities.md` 更新
- **知识缺失**: 检查是否正确加载了 `_base/` 和匹配的知识包
