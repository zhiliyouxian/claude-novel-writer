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

## 用户工作区结构

用户在**任意目录**执行 `/workspace-init` 后，会创建以下结构：

```
{当前目录}/
├── pools/                      # 素材池部门
│   ├── {pool_name}/           # 素材池（用户放入参考小说）
│   └── analysis/              # 分析报告（自动生成）
│
├── blueprints/                 # 策划部门
│   └── {project_id}/          # 蓝图（企划书）
│       ├── proposal.md        # 选题方案
│       ├── worldview.md       # 世界观
│       ├── characters.md      # 角色档案
│       └── outline.md         # 章节大纲
│
├── productions/                # 制作部门
│   └── {project_id}/          # 制作项目
│       ├── blueprint.link     # 链接到蓝图
│       ├── chapters/          # 章节文件
│       └── data/
│           └── entities.md    # 实体库
│
└── releases/                   # 发布部门
    └── {project_id}/
        ├── reviews/           # 审核报告
        ├── text/              # TXT版
        └── audio/             # TTS版
```

---

## 关键规范

### 0. 项目标识规范（重要！）

**每个小说项目必须有唯一的 project_id**，用于区分不同作品的文件路径。

**确定 project_id 的规则**：
1. 如果用户明确指定项目名（如"创作《纵横天下》"），使用拼音或英文：`zongheng`
2. 如果工作区只有一个蓝图，自动使用该蓝图的目录名作为 project_id
3. 如果工作区有多个蓝图，**必须询问用户使用哪个**
4. 如果用户没有指定且没有蓝图，使用默认名 `novel-001`

**文件路径示例**（假设 project_id=zongheng）：
```
blueprints/zongheng/          # 蓝图目录
productions/zongheng/         # 制作目录
  ├── chapters/               # 章节必须在这里
  │   ├── chapter-001.md
  │   └── ...
  └── data/
      └── entities.md
releases/zongheng/            # 发布目录
```

**严禁**：
- 在工作区根目录创建 `chapters/` 目录
- 在 `productions/` 根目录直接创建章节文件
- 不同项目的章节混在一起

### 1. 书写规范

所有创作章节必须遵守 `WRITING_STYLE_GUIDE.md`：
- 文件命名: `chapter-{001}.md`（三位数字补零）
- 章节标题: `# 第1章 标题`（阿拉伯数字）
- 标点符号: 根据目标语言使用对应标点
- 数字规则: 年龄/境界/数量用阿拉伯数字

### 2. 实体管理

- 使用 Markdown 表格管理实体（不用 JSON）
- 位置: `productions/{project_id}/data/entities.md`
- chapter-writer 自动维护实体库

### 3. 知识库使用

- `libraries/knowledge/_base/` 存放通用参考知识（始终读取）
- 其他知识包根据用户需求动态加载
- Agent 读取知识库生成项目内容
- 不直接复制模板，而是根据需求生成

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
1. 检查文件是否生成到正确的用户工作区目录
2. 确认实体库格式正确（Markdown 表格）
3. 验证章节遵守 WRITING_STYLE_GUIDE.md

### 常见问题
- **路径错误**: 确保输出到用户工作区，不是 Plugin 目录
- **格式不符**: 检查 WRITING_STYLE_GUIDE.md 规范
- **实体不一致**: 检查 `productions/{project_id}/data/entities.md` 更新
- **知识缺失**: 检查是否正确加载了 `_base/` 和匹配的知识包

---

## 参考文档

- `WRITING_STYLE_GUIDE.md` - 强制书写规范
- `libraries/README.md` - 知识库和知识包说明
- `commands/README.md` - Commands 详细用法
