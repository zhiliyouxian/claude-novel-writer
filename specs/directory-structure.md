# 目录结构规范

本文件定义用户工作区的标准目录结构，所有 Agent、Command、Skill 必须遵循此规范。

---

## 四部门架构

```
素材池(Pools) → 策划(Blueprints) → 制作(Productions) → 发布(Releases)
```

---

## 工作区目录结构

用户执行 `/workspace-init` 后创建的标准结构：

```
{工作区根目录}/
├── pools/                          # 素材池部门
│   ├── {pool_name}/               # 素材池（用户放入参考小说）
│   └── analysis/                  # 分析报告（自动生成）
│
├── blueprints/                     # 策划部门
│   └── {project_id}/              # 蓝图（企划书）
│       ├── proposal.md            # 选题方案
│       ├── worldview.md           # 世界观
│       ├── characters.md          # 角色档案
│       └── outline.md             # 章节大纲
│
├── productions/                    # 制作部门
│   └── {project_id}/              # 制作项目
│       ├── blueprint.link         # 链接到蓝图
│       ├── chapters/              # 章节文件
│       │   ├── chapter-001.md
│       │   ├── chapter-002.md
│       │   └── ...
│       └── data/
│           └── entities.md        # 实体库
│
└── releases/                       # 发布部门
    └── {project_id}/
        ├── reviews/               # 审核报告
        │   └── batch-{start}-{end}-report.md
        ├── text/                  # TXT版
        └── audio/                 # TTS版
```

---

## 路径速查表

### 输入路径（读取）

| 内容 | 路径 |
|------|------|
| 蓝图目录 | `blueprints/{project_id}/` |
| 选题方案 | `blueprints/{project_id}/proposal.md` |
| 世界观 | `blueprints/{project_id}/worldview.md` |
| 角色档案 | `blueprints/{project_id}/characters.md` |
| 章节大纲 | `blueprints/{project_id}/outline.md` |
| 素材分析 | `pools/analysis/{pool_name}/` |
| 风格融合 | `pools/analysis/{pool_name}/style-fusion.md` |

### 输出路径（写入）

| 内容 | 路径 |
|------|------|
| 章节文件 | `productions/{project_id}/chapters/chapter-{NNN}.md` |
| 实体库 | `productions/{project_id}/data/entities.md` |
| 审核报告 | `releases/{project_id}/reviews/batch-{start}-{end}-report.md` |
| TXT导出 | `releases/{project_id}/text/` |
| 有声书导出 | `releases/{project_id}/audio/` |

---

## project_id 确定规则

1. 如果用户明确指定项目名（如"创作《纵横天下》"），使用拼音或英文：`zongheng`
2. 如果工作区只有一个蓝图，自动使用该蓝图的目录名
3. 如果工作区有多个蓝图，**必须询问用户使用哪个**
4. 如果用户没有指定且没有蓝图，使用默认名 `novel-001`

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 章节文件 | `chapter-{NNN}.md` (三位数补零) | `chapter-001.md`, `chapter-100.md` |
| 审核报告 | `batch-{start}-{end}-report.md` | `batch-001-010-report.md` |
| 实体库 | `entities.md` | - |

---

## 禁止事项

- 在工作区根目录创建 `chapters/` 目录
- 在 `productions/` 根目录直接创建章节文件
- 不同项目的章节混在一起
- 将审核报告保存到 `productions/` 目录
- 将章节文件保存到 `releases/` 目录

