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
        │   └── ch-audit-*.md      # 章节审核报告
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
| 章节审核报告 | `releases/{project_id}/reviews/ch-audit-{start}-{end}.md` |
| **发布（默认/单语言）** | |
| TXT合集 | `releases/{project_id}/text/full.txt` |
| Markdown发布版 | `releases/{project_id}/markdown/{NNNN}.md` |
| **有声书** | |
| 朗读文本 | `releases/{project_id}/tts/scripts/{NNNN}.txt` |
| 音频文件 | `releases/{project_id}/tts/audio/{NNNN}.mp3` |
| 字幕文件 | `releases/{project_id}/tts/subtitles/{NNNN}.srt` |
| **视频** | |
| 分镜脚本 | `releases/{project_id}/video/storyboard/storyboard.md` |
| 场景提示词 | `releases/{project_id}/video/prompts/scenes/{NNNN}.md` |
| 角色一致性提示词 | `releases/{project_id}/video/prompts/characters/{角色名}.md` |
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
| 章节审核报告 | `ch-audit-{start}-{end}.md` | `ch-audit-0001-0010.md` |
| TTS朗读文本 | `{NNNN}.txt` (四位数补零) | `0001.txt`, `0100.txt` |
| 音频文件 | `{NNNN}.mp3` | `0001.mp3` |
| 字幕文件 | `{NNNN}.srt` | `0001.srt` |
| **视频文件** | | |
| 分镜脚本 | `storyboard.md` | - |
| 场景提示词 | `scene-{NNNN}.md` | `scene-0001.md` |
| 角色一致性提示词 | `{角色名}.md` | `protagonist.md` |

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
├── storyboard/
│   ├── storyboard.md              # 分镜脚本（场景+时间码）
│   └── chapter-{NNNN}.json        # 章节分镜数据（可选）
├── prompts/
│   ├── scenes/                    # 场景图像/视频提示词
│   │   ├── scene-0001.md
│   │   └── ...
│   └── characters/                # 角色一致性提示词
│       ├── {角色名}.md
│       └── ...
├── images/                        # 用户放置的静态图（手动生成）
│   ├── scenes/
│   │   ├── scene-0001.png
│   │   └── ...
│   └── characters/                # 角色参考图（可选）
│       └── ...
├── kenburns/
│   ├── config.json                # 全局 Ken Burns 设置
│   └── scene-params.json          # 各场景动画参数
├── clips/                         # Ken Burns 动画片段（自动生成）
│   ├── scene-0001.mp4
│   └── ...
├── scripts/                       # ffmpeg 拼接脚本
│   └── assemble-chapter-{N}.sh
└── output/                        # 最终视频
    ├── chapter-0001.mp4
    └── ...
```

### 视频制作流程

```
SRT字幕 → 分镜脚本 → 场景提示词 → [用户手动生成图片] → Ken Burns动画 → 视频拼接
```

### 分镜脚本格式 (`storyboard.md`)

> 模板参考: `templates/storyboard-template.md`

```markdown
---
chapter: 1
source_srt: releases/{project_id}/tts/subtitles/0001.srt
total_duration: "00:12:35"
scene_count: 24
generated: 2024-01-15
---

# 第1章 分镜脚本

## 场景列表

| 场景 | 时间码 | 时长 | 地点 | 角色 | 情绪 | SRT序号 |
|------|--------|------|------|------|------|---------|
| 001 | 00:00:00-00:00:32 | 32s | 外门广场 | 萧羽, 李傲天 | 紧张 | 1-5 |
| 002 | 00:00:32-00:01:15 | 43s | 外门广场 | 萧羽（内心独白） | 坚定 | 6-12 |

## 场景详情

### 场景 001: 广场对峙

**时间码**: 00:00:00 - 00:00:32
**时长**: 32秒
**SRT序号**: #1-5

**地点**: 外门广场，清晨
**角色**: 萧羽（主角）、李傲天（反派）
**情绪**: 紧张、对峙

**画面描述**:
清晨的宗门广场，两名年轻人对峙。一人穿着破旧的灰色道袍（萧羽），
另一人身着华贵的红色锦袍（李傲天）。周围弟子围观。

**镜头建议**:
- 起始: 大远景，建立场景
- 运动: 缓慢推进至中景
- 结束: 越肩镜头，从萧羽视角看李傲天
```

### 场景提示词格式 (`scene-{NNNN}.md`)

> 模板参考: `templates/scene-prompt-template.md`

```markdown
---
scene_number: 1
chapter: 1
timecode_start: "00:00:00"
timecode_end: "00:00:32"
duration_seconds: 32
srt_range: [1, 5]
characters: ["萧羽", "李傲天"]
location: "外门广场"
emotion: "紧张"
---

# 场景 001: 广场对峙

## 静态图提示词

### Midjourney / DALL-E

```
Dramatic confrontation scene in an ancient Chinese martial arts sect plaza
at dawn, two young men facing each other in the center, one in worn gray
robes (protagonist) another in luxurious crimson robes (antagonist),
surrounded by disciples in a circle, traditional pagoda architecture in
background, golden hour lighting, cinematic composition, 4K,
oriental fantasy style, anime influenced
--ar 16:9 --style raw --v 6
```

## 视频提示词

### Runway Gen-3

```
Camera slowly pushes in on two young men facing off in an ancient Chinese
sect plaza. The protagonist in worn gray robes stands defiantly while his
antagonist in crimson robes sneers. Morning light creates dramatic shadows.
```

### Kling AI

```
[场景: 古代宗门广场，清晨]
两名修士对峙 - 灰袍青年（冷静、坚定）vs 红袍贵公子（轻蔑）
镜头: 大远景缓慢推进至中景，8秒
风格: 电影感，东方玄幻
```

### Sora / Veo

```
A cinematic scene in an ancient Chinese martial arts sect courtyard at dawn.
The camera starts with a wide establishing shot showing traditional pagodas
and a crowd of disciples forming a circle. It slowly pushes in to reveal
two young men in the center - a determined youth in worn gray robes facing
a sneering noble in expensive crimson robes. Golden morning light casts
long shadows. Style: Epic fantasy, anime-influenced. Duration: 8 seconds.
```

## Ken Burns 参数

```json
{
  "type": "push_in",
  "start": {"scale": 1.0, "x": 0.5, "y": 0.5},
  "end": {"scale": 1.3, "x": 0.5, "y": 0.45},
  "duration": 32,
  "easing": "ease-in-out"
}
```
```

### 角色一致性提示词格式 (`{角色名}.md`)

```markdown
---
character: 萧羽
role: protagonist
generated: 2024-01-15
---

# 萧羽 - 视觉参考提示词

## 一致性标签

| 特征 | 描述 |
|------|------|
| 脸型 | 棱角分明，下颌线锐利 |
| 头发 | 短发，微乱，黑色 |
| 眼睛 | 深褐色，眼神锐利 |
| 身材 | 175cm，清瘦，健壮 |
| 服饰 | 深蓝色道袍，银色云纹 |
| 风格锚点 | "年轻的剑修" |

## 复制用标签（英文）

```
young man, angular face, sharp jawline, short messy black hair,
deep brown intense eyes, 175cm tall, slender athletic build,
wearing dark blue robes with silver cloud embroidery
```

## 头像提示词 (3:4)

```
A 20-year-old East Asian man with sharp angular features, sword-like
eyebrows, short messy black hair, deep brown eyes with an intense gaze,
wearing a dark blue traditional Chinese robe with silver cloud embroidery,
portrait style, cinematic lighting, 4K, highly detailed, xianxia style
--ar 3:4 --style raw
```

## 全身提示词 (2:3)

```
Full body shot of a tall slender young man (175cm), confident stance,
wearing flowing dark blue robes with silver cloud patterns, hands
clasped behind back, ancient Chinese mountain temple background,
dramatic lighting, xianxia anime style
--ar 2:3 --style raw
```
```

### Ken Burns 配置格式 (`scene-params.json`)

```json
{
  "version": "1.0",
  "global_settings": {
    "fps": 30,
    "resolution": "1920x1080",
    "default_easing": "ease-in-out"
  },
  "scenes": [
    {
      "scene_id": "0001",
      "image": "scene-0001.png",
      "duration_seconds": 32,
      "animation": {
        "type": "push_in",
        "start": {"scale": 1.0, "x": 0.5, "y": 0.5},
        "end": {"scale": 1.3, "x": 0.5, "y": 0.45},
        "easing": "ease-in-out"
      }
    }
  ]
}
```

### Ken Burns 动画类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `push_in` | 缓慢推进（放大） | 强调、紧张、聚焦 |
| `pull_out` | 缓慢拉远（缩小） | 揭示全貌、结束 |
| `pan_left` | 向左平移 | 场景展示、跟随移动 |
| `pan_right` | 向右平移 | 场景展示、跟随移动 |
| `pan_up` | 向上平移 | 仰视、壮观 |
| `pan_down` | 向下平移 | 俯视、压迫 |
| `diagonal` | 斜向推进 | 动态感、戏剧性 |

---

## 禁止事项

- 在工作区根目录创建 `chapters/` 目录
- 在 `productions/` 根目录直接创建章节文件
- 不同项目的章节混在一起
- 将审核报告保存到 `productions/` 目录
- 将章节文件保存到 `releases/` 目录
- 混用单语言和多语言目录结构（选择一种）

