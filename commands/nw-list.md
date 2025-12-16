---
name: nw-list
description: 快速列出所有项目
---

# /nw-list

快速列出工作区中的所有项目，按阶段分类显示。

## 用法

```
/nw-list
/nw-list blueprints
/nw-list productions
```

## 执行流程

### 无参数 - 列出所有项目

```bash
# 扫描所有阶段
ls blueprints/
ls productions/
ls releases/
```

输出：

```
📁 项目列表

蓝图 (3):
  dao_immortal, zongheng, new_project

制作中 (2):
  dao_immortal (45章), zongheng (120章)

已发布 (1):
  zongheng
```

### 指定阶段

```
/nw-list blueprints
```

输出：

```
📁 蓝图项目

dao_immortal
  ├── proposal.md ✅
  ├─��� worldview.md ✅
  ├── characters.md ✅
  └── outline.md ✅

zongheng
  ├── proposal.md ✅
  ├── worldview.md ✅
  ├── characters.md ✅
  └── outline.md ✅

new_project
  ├── proposal.md ✅
  ├── worldview.md ✅
  ├── characters.md ⚠️ 空文件
  └── outline.md ❌ 缺失
```

## 输出格式

### 简洁模式（默认）

单行列出项目名，适合快速查看。

### 详细模式

```
/nw-list --detail
```

显示每个项目的文件结构和状态。

## 与 /nw-status 的区别

| 命令 | 用途 |
|------|------|
| `/nw-list` | 快速查看有哪些项目 |
| `/nw-status` | 查看项目详细进度 |

## 相关命令

- `/nw-status` - 详细状态
- `/nw-init` - 初始化工作区
