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
│       │   ├── character-{角色名}.md  # 单角色档案（含图像提示词）
│       │   ├── character-{角色名}/    # 角色视觉素材（可选）
│       │   │   ├── portrait.png       # 头像/半身像
│       │   │   └── full-body.png      # 全身像
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
        │   └── batch-*.md         # 章节审核报告
        │
        ├── {locale}/              # 多语言发布（可选）
        │   ├── text/              # TXT版
        │   ├── markdown/          # Markdown版
        │   ├── tts/               # 有声书
        │   │   ├── scripts/       # 朗读文本
        │   │   ├── audio/         # 音频文件
        │   │   └── subtitles/     # 字幕文件
        │   └── video/             # 视频（可选）
        │       ├── storyboard/    # 分镜脚本
        │       └── prompts/       # 图像/视频生成提示词
        │
        ├── text/                  # 默认（单语言）TXT版
        │   └── full.txt           # 完整合集
        ├── markdown/              # 默认（单语言）Markdown版
        │   ├── 0001.md            # 去掉 yml 头
        │   └── ...
        ├── tts/                   # 默认（单语言）有声书
        │   ├── scripts/           # 朗读文本（去换行）
        │   │   ├── 0001.txt
        │   │   └── ...
        │   ├── audio/             # 音频文件（可选）
        │   │   ├── 0001.mp3
        │   │   └── ...
        │   └── subtitles/         # 字幕文件（可选）
        │       ├── 0001.srt
        │       └── ...
        └── video/                 # 默认（单语言）视频（可选）
            ├── storyboard/        # 分镜脚本
            │   └── storyboard.md  # 场景列表+时间码
            └── prompts/           # 图像/视频生成提示词
                ├── scenes/        # 场景提示词
                └── characters/    # 角色一致性提示词
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
| 角色视觉素材 | `blueprints/{project_id}/characters/character-{角色名}/` |
| **大纲** | |
| 大纲框架 | `blueprints/{project_id}/outline.md` |
| 分卷大纲 | `blueprints/{project_id}/outlines/vol-{N}.md` |
| **素材** | |
| 素材分析 | `pools/analysis/{pool_name}/` |
| 风格融合 | `pools/analysis/{pool_name}/style-fusion.md` |

### 输出路径（写入）

| 内容 | 路径 |
|------|------|
| **制作** | |
| 章节文件 | `productions/{project_id}/chapters/chapter-{NNNN}.md` |
| 实体库 | `productions/{project_id}/data/entities.md` |
| **审核** | |
| 蓝图审核报告 | `releases/{project_id}/reviews/bp-audit-report.md` |
| 章节审核报告 | `releases/{project_id}/reviews/batch-{NNNN}-{NNNN}-report.md` |
| **发布（默认/单语言）** | |
| TXT合集 | `releases/{project_id}/text/full.txt` |
| Markdown发布版 | `releases/{project_id}/markdown/{NNNN}.md` |
| **有声书** | |
| 朗读文本 | `releases/{project_id}/tts/scripts/{NNNN}.txt` |
| 音频文件 | `releases/{project_id}/tts/audio/{NNNN}.mp3` |
| 字幕文件 | `releases/{project_id}/tts/subtitles/{NNNN}.srt` |
| **视频** | |
| 分镜文件 | `releases/{project_id}/video/storyboard/chapter-{NNNN}.yaml` |
| 镜头图片 | `releases/{project_id}/video/images/shots/chapter-{NNNN}/shot-{NNN}.png` |
| 动画片段 | `releases/{project_id}/video/clips/chapter-{NNNN}/shot-{NNN}.mp4` |
| 输出视频 | `releases/{project_id}/video/output/chapter-{NNNN}.mp4` |
| **多语言发布** | |
| 多语言TXT | `releases/{project_id}/{locale}/text/` |
| 多语言有声书 | `releases/{project_id}/{locale}/tts/` |
| 多语言视频 | `releases/{project_id}/{locale}/video/` |

---

## project_id 命名规范

> 详细规范见 `specs/project-naming.md`

### 自动生成规则

**格式**: `{主题材前缀}_{序号}`

| 主题材 | 前缀 | 示例 |
|--------|------|------|
| 玄幻 | `xuanhuan` | `xuanhuan_001` |
| 仙侠 | `xianxia` | `xianxia_001` |
| 都市 | `dushi` | `dushi_001` |
| 科幻 | `kehuang` | `kehuang_001` |
| 历史 | `lishi` | `lishi_001` |
| 游戏 | `youxi` | `youxi_001` |
| 奇幻 | `qihuan` | `qihuan_001` |
| 悬疑 | `xuanyi` | `xuanyi_001` |
| 轻小说 | `qingxiaoshuo` | `qingxiaoshuo_001` |

**生成流程**:
1. 识别主题材 → 确定前缀
2. 扫描 `blueprints/` 目录 → 找出同前缀最大序号
3. 序号+1 → 生成新 project_id

**多题材处理**: 使用主题材（世界观背景）
- 都市修仙 → `dushi_XXX`
- 历史玄幻 → `lishi_XXX`

### 确定规则

1. **创建新蓝图**: 自动生成（如 `xuanhuan_001`）
2. **手动覆盖**: 使用 `--id` 参数指定
3. **已有项目**:
   - 工作区只有一个蓝图 → 自动使用
   - 工作区有多个蓝图 → **必须询问用户**

### 书名与 project_id

| 属性 | project_id | book_title |
|------|------------|------------|
| 用途 | 目录命名 | 作品名称 |
| 修改 | 创建后不可改 | 随时可改 |
| 必填 | 自动生成 | 发布前确定 |

书名设置在 `proposal.md` 的 `book_title` 字段。

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| **蓝图文件** | | |
| 世界观模块 | `{module}.md` | `power-system.md`, `factions.md` |
| 角色档案 | `character-{角色名}.md` | `character-林凡.md` |
| 角色素材目录 | `character-{角色名}/` | `character-林凡/` |
| 角色头像 | `portrait.png` | - |
| 角色全身像 | `full-body.png` | - |
| 分卷大纲 | `vol-{N}.md` | `vol-1.md`, `vol-2.md` |
| **制作文件** | | |
| 章节文件 | `chapter-{NNNN}.md` (四位数补零) | `chapter-0001.md`, `chapter-0100.md` |
| 实体库 | `entities.md` | - |
| **发布文件** | | |
| 蓝图审核报告 | `bp-audit-report.md` | - |
| 章节审核报告 | `batch-{NNNN}-{NNNN}-report.md` | `batch-0001-0010-report.md` |
| TTS朗读文本 | `{NNNN}.txt` (四位数补零) | `0001.txt`, `0100.txt` |
| 音频文件 | `{NNNN}.mp3` | `0001.mp3` |
| 字幕文件 | `{NNNN}.srt` | `0001.srt` |
| **视频文件** | | |
| 分镜文件 | `chapter-{NNNN}.yaml` | `chapter-0001.yaml` |
| 镜头图片目录 | `chapter-{NNNN}/` | `chapter-0001/` |
| 镜头图片 | `shot-{NNN}.png` | `shot-001.png` |
| 动画片段 | `shot-{NNN}.mp4` | `shot-001.mp4` |
| 输出视频 | `chapter-{NNNN}.mp4` | `chapter-0001.mp4` |

---

## 多语言发布

当需要发布多语言版本时，使用 `{locale}` 子目录区分：

| locale 代码 | 语言 |
|-------------|------|
| `zh-CN` | 简体中文 |
| `zh-TW` | 繁体中文 |
| `en-US` | 英语 |
| `ja-JP` | 日语 |
| `ko-KR` | 韩语 |

**单语言项目**（默认）：直接使用 `releases/{project_id}/text/`, `tts/`, `video/` 等目录。

**多语言项目**：使用 `releases/{project_id}/{locale}/` 结构。

```
releases/xuanhuan_001/
├── zh-CN/                    # 中文版
│   ├── text/
│   ├── tts/
│   └── video/
├── en-US/                    # 英文版
│   ├── text/
│   ├── tts/
│   └── video/
└── reviews/                  # 审核报告（共用）
```

---

## 视频生成

视频相关文件结构：

```
releases/{project_id}/video/
├── storyboard/                    # 分镜文件（结构化 YAML）
│   ├── chapter-0001.yaml          # 第1章分镜
│   ├── chapter-0002.yaml          # 第2章分镜
│   └── ...
├── images/                        # 镜头图片（用户生成后放入）
│   └── shots/
│       ├── chapter-0001/          # 第1章镜头图片
│       │   ├── shot-001.png
│       │   ├── shot-002.png
│       │   └── ...
│       └── chapter-0002/          # 第2章镜头图片
│           └── ...
├── clips/                         # Ken Burns 动画片段（自动生成）
│   └── chapter-0001/
│       ├── shot-001.mp4
│       └── ...
├── temp/                          # 临时文件
└── output/                        # 最终视频
    ├── chapter-0001.mp4
    └── ...
```

### 视频制作流程

```
SRT + 章节内容 → 分镜文件(YAML) → [用户生成镜头图片] → Ken Burns动画 → 视频合成
```

### 分镜文件格式 (`chapter-{NNNN}.yaml`)

分镜文件使用 YAML 格式，包含镜头提示词、运动参数、时长等结构化数据：

```yaml
# releases/{project_id}/video/storyboard/chapter-0001.yaml

chapter: 1
source_srt: "releases/{project_id}/tts/subtitles/0001.srt"
source_chapter: "productions/{project_id}/chapters/chapter-0001.md"
total_duration: "00:12:35"

shots:
  - id: "001"
    srt_range: [1, 8]
    start_time: "00:00:00.000"
    end_time: "00:00:32.500"
    duration: 32.5

    # 画面内容
    location: "外门广场"
    characters: ["萧羽", "李傲天"]
    description: "外门广场上，弟子们围成一圈。李傲天身着红袍傲然而立，嘲讽萧羽。"
    mood: "紧张对峙"

    # AI 绘图提示词
    image_prompt: |
      Chinese fantasy scene, outer sect plaza, disciples gathered in circle,
      young man in red robe standing arrogantly, another young man facing him calmly,
      ancient Chinese architecture background, dramatic lighting, cinematic composition,
      high detail, 8k, masterpiece
    negative_prompt: "blurry, low quality, deformed, text, watermark"

    # 镜头运动
    camera:
      type: "push_in"
      start_scale: 1.0
      end_scale: 1.3
      start_position: [0.5, 0.5]
      end_position: [0.5, 0.45]

  - id: "002"
    srt_range: [9, 15]
    start_time: "00:00:32.500"
    end_time: "00:01:05.000"
    duration: 32.5
    # ... 更多镜头
```

### 分镜文件命名规范

| 文件类型 | 命名格式 | 示例 |
|----------|----------|------|
| 分镜文件 | `chapter-{NNNN}.yaml` | `chapter-0001.yaml` |
| 镜头图片目录 | `chapter-{NNNN}/` | `chapter-0001/` |
| 镜头图片 | `shot-{NNN}.png` | `shot-001.png` |
| 动画片段 | `shot-{NNN}.mp4` | `shot-001.mp4` |
| 输出视频 | `chapter-{NNNN}.mp4` | `chapter-0001.mp4` |

**说明**：
- 章节号 `{NNNN}` 使用四位数补零，与章节文件对应
- 镜头号 `{NNN}` 使用三位数补零，每章从 001 开始
- 镜头图片按章节分目录存放，便于管理

### Ken Burns 动画类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `push_in` | 缓慢推进（放大） | 强调、紧张、聚焦 |
| `pull_out` | 缓慢拉远（缩小） | 揭示全貌、结束 |
| `pan_left` | 向左平移 | 场景展示、跟随移动 |
| `pan_right` | 向右平移 | 场景展示、跟随移动 |
| `pan_up` | 向上平移 | 仰视、壮观 |
| `pan_down` | 向下平移 | 俯视、压迫 |
| `static` | 静止 | 对话、平静场景 |

---

## 禁止事项

- 在工作区根目录创建 `chapters/` 目录
- 在 `productions/` 根目录直接创建章节文件
- 不同项目的章节混在一起
- 将审核报告保存到 `productions/` 目录
- 将章节文件保存到 `releases/` 目录
- 混用单语言和多语言目录结构（选择一种）

