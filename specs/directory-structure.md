# 目录结构规范

本文件定义用户工作区的标准目录结构，所有 Agent、Command、Skill 必须遵循此规范。

---

## 四部门架构

```
素材池(Pools) → 策划(Blueprints) → 制作(Productions) → 发布(Releases)
```

---

## 工作区目录结构

用户执行 `/nw-init` 后创建的标准结构：

```
{工作区根目录}/
├── pools/                          # 素材池部门
│   ├── {pool_name}/               # 素材池（用户放入参考小说）
│   └── analysis/                  # 分析报告（自动生成）
│
├── blueprints/                     # 策划部门
│   └── {project_id}/              # 蓝图（企划书）
│       ├── proposal.md            # 选题方案
│       │
│       ├── worldview.md           # 世界观总览
│       └── worldview/             # 世界观详细模块
│       │   ├── power-system.md    # 力量体系（境界、功法、战斗）
│       │   ├── factions.md        # 势力（宗门、家族、组织）
│       │   ├── geography.md       # 地理（地图、场景、区域）
│       │   ├── history.md         # 历史（重大事件、时间线）
│       │   └── rules.md           # 规则（天道、因果、世界法则）
│       │
│       ├── characters.md          # 角色总览（列表、关系网）
│       └── characters/            # 角色详细档案
│       │   ├── character-{角色名}.md  # 单角色档案
│       │   └── ...
│       │
│       ├── outline.md             # 大纲框架（阶段、关键节点）
│       └── outlines/              # 分卷详细大纲
│           ├── vol-1.md           # 第一卷详细章节
│           ├── vol-2.md           # 第二卷详细章节
│           └── ...
│
├── productions/                    # 制作部门
│   └── {project_id}/              # 制作项目
│       ├── blueprint.link         # 链接到蓝图
│       ├── chapters/              # 章节文件
│       │   ├── chapter-0001.md
│       │   ├── chapter-0002.md
│       │   └── ...
│       └── data/
│           └── entities.md        # 实体库
│
└── releases/                       # 发布部门
    └── {project_id}/
        ├── reviews/               # 审核报告
        │   ├── bp-audit-report.md # 蓝图审核报告
        │   └── ch-audit-*.md      # 章节审核报告
        ├── tts/                   # 有声书
        │   ├── scripts/           # 朗读文本（去换行）
        │   │   ├── 0001.txt
        │   │   └── ...
        │   ├── audio/             # 音频文件（可选）
        │   │   ├── 0001.mp3
        │   │   └── ...
        │   └── subtitles/         # 字幕文件（可选）
        │       ├── 0001.srt
        │       └── ...
        ├── text/
        │   └── full.txt           # 完整合集
        └── markdown/              # 发布版 Markdown
            ├── 0001.md            # 去掉 yml 头
            └── ...
```

---

## 路径速查表

### 输入路径（读取）

| 内容 | 路径 |
|------|------|
| 蓝图目录 | `blueprints/{project_id}/` |
| 选题方案 | `blueprints/{project_id}/proposal.md` |
| **世界观** | |
| 世界观总览 | `blueprints/{project_id}/worldview.md` |
| 世界观-力量体系 | `blueprints/{project_id}/worldview/power-system.md` |
| 世界观-势力 | `blueprints/{project_id}/worldview/factions.md` |
| 世界观-地理 | `blueprints/{project_id}/worldview/geography.md` |
| 世界观-历史 | `blueprints/{project_id}/worldview/history.md` |
| 世界观-规则 | `blueprints/{project_id}/worldview/rules.md` |
| **角色** | |
| 角色总览 | `blueprints/{project_id}/characters.md` |
| 单角色档案 | `blueprints/{project_id}/characters/character-{角色名}.md` |
| **大纲** | |
| 大纲框架 | `blueprints/{project_id}/outline.md` |
| 分卷大纲 | `blueprints/{project_id}/outlines/vol-{N}.md` |
| **素材** | |
| 素材分析 | `pools/analysis/{pool_name}/` |
| 风格融合 | `pools/analysis/{pool_name}/style-fusion.md` |

### 输出路径（写入）

| 内容 | 路径 |
|------|------|
| 章节文件 | `productions/{project_id}/chapters/chapter-{NNNN}.md` |
| 实体库 | `productions/{project_id}/data/entities.md` |
| 蓝图审核报告 | `releases/{project_id}/reviews/bp-audit-report.md` |
| 章节审核报告 | `releases/{project_id}/reviews/ch-audit-{start}-{end}.md` |
| TXT合集 | `releases/{project_id}/text/full.txt` |
| 朗读文本 | `releases/{project_id}/tts/scripts/{NNNN}.txt` |
| 音频文件 | `releases/{project_id}/tts/audio/{NNNN}.mp3` |
| 字幕文件 | `releases/{project_id}/tts/subtitles/{NNNN}.srt` |
| Markdown发布版 | `releases/{project_id}/markdown/{NNNN}.md` |

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
| **蓝图文件** | | |
| 世界观模块 | `{module}.md` | `power-system.md`, `factions.md` |
| 角色档案 | `character-{角色名}.md` | `character-{主角}.md` |
| 分卷大纲 | `vol-{N}.md` | `vol-1.md`, `vol-2.md` |
| **制作文件** | | |
| 章节文件 | `chapter-{NNNN}.md` (四位数补零) | `chapter-0001.md`, `chapter-0100.md` |
| 实体库 | `entities.md` | - |
| **发布文件** | | |
| 蓝图审核报告 | `bp-audit-report.md` | - |
| 章节审核报告 | `ch-audit-{start}-{end}.md` | `ch-audit-0001-0010.md` |
| TTS朗读文本 | `{NNNN}.txt` (四位数补零) | `0001.txt`, `0100.txt` |
| 音频文件 | `{NNNN}.mp3` | `0001.mp3` |
| 字幕文件 | `{NNNN}.srt` | `0001.srt` |

---

## 禁止事项

- 在工作区根目录创建 `chapters/` 目录
- 在 `productions/` 根目录直接创建章节文件
- 不同项目的章节混在一起
- 将审核报告保存到 `productions/` 目录
- 将章节文件保存到 `releases/` 目录

