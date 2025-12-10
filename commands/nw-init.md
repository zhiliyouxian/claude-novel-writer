---
name: nw-init
description: 初始化工作区。用法: /nw-init
---

# 工作区初始化命令

在当前目录创建小说创作工作区的标准目录结构，并生成项目级 CLAUDE.md 指导文件。

## 用法

```bash
/nw-init
```

## 功能

此命令会在**当前目录**创建以下目录结构和文件：

```
{当前目录}/
├── CLAUDE.md                   # 项目工作指南（新生成）
├── pools/                      # 素材池部门
│   └── analysis/              # 分析报告存放处
│
├── blueprints/                 # 策划部门
│   └── .gitkeep
│
├── productions/                # 制作部门
│   └── .gitkeep
│
└── releases/                   # 发布部门
    └── .gitkeep
```

## 执行指令

收到此命令后，执行以下步骤：

### 步骤1: 创建目录结构

```bash
mkdir -p pools/analysis blueprints productions releases
```

### 步骤2: 生成 CLAUDE.md

读取 Plugin 中的 `templates/project-CLAUDE.md` 模板，替换占位符后写入当前目录：

```markdown
占位符替换规则:
- {project_id} → "your_project"（提示用户后续指定）
- {created_date} → 当前日期（如 2024-01-20）
- {workspace_path} → 当前目录路径
```

**生成的 CLAUDE.md 包含**：
- project_id 命名规范
- 目录结构说明
- 常用命令参考
- 注意事项

### 步骤3: 输出完成信息

如果用户不在预期目录，先提示确认再执行。

## 输出示例

```
✅ 工作区初始化完成!

创建的目录结构:
├── CLAUDE.md        # 项目工作指南
├── pools/           # 放入参考小说进行分析
├── blueprints/      # 存放生成的蓝图(企划书)
├── productions/     # 存放创作中的小说项目
└── releases/        # 存放审核和导出的成品

📝 已生成 CLAUDE.md，包含:
- project_id 命名规范
- 目录结构说明
- 常用命令参考

下一步:
1. 准备素材: mkdir pools/xuanhuan_1 && cp 参考小说.txt pools/xuanhuan_1/
2. 分析素材: "/analyze-pool xuanhuan_1"
3. 生成蓝图: "/create-blueprint xuanhuan_1 玄幻 废柴流"

或者直接开始创作(不使用参考素材):
"我想写一个玄幻废柴流小说，主角有异火系统"
```

## 注意事项

1. **任意目录**: 可以在任何你想要的目录执行此命令
2. **不覆盖**: 如果目录或 CLAUDE.md 已存在，不会覆盖现有文件
3. **版本控制**: 创建的结构适合 Git 版本控制

## 已有工作区检测

如果当前目录已经包含工作区结构（存在 `pools/`、`blueprints/`、`productions/`、`releases/` 中的任一目录），会提示：

```
⚠️ 检测到已有工作区结构

现有目录/文件:
- CLAUDE.md ✓
- pools/ ✓
- blueprints/ ✓
- productions/ ✗ (不存在)
- releases/ ✗ (不存在)

是否补充缺失的目录? [Y/n]
```

## 相关命令

- `/status` - 查看工作区状态
- `/analyze-pool` - 分析素材池
- `/create-blueprint` - 创建蓝图
