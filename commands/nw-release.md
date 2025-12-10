---
name: nw-release
description: 发布导出。用法: /nw-release <格式>
---

# 发布导出命令

将创作内容导出为多种发布格式。

## 用法

```bash
/nw-release <格式>
```

## 格式说明

| 格式 | 输出 | 说明 |
|------|------|------|
| `tts` | `releases/{project_id}/tts/scripts/` | 语音文本（去换行、优化朗读） |
| `txt` | `releases/{project_id}/text/full.txt` | 完整合集（单文件） |
| `md` | `releases/{project_id}/markdown/` | 发布版 Markdown（去 yml 头） |
| `all` | 以上全部 | |

## 示例

```bash
# 导出语音朗读文本
/nw-release tts

# 导出完整合集
/nw-release txt

# 导出发布版 Markdown
/nw-release md

# 导出所有格式
/nw-release all
```

也可以通过自然语言触发，如：
- "导出有声书文本"
- "生成语音版本"
- "合成音频" → 会生成 tts/scripts + audio + subtitles

## 支持的导出格式

### 1. TXT纯文本 (txt)

**文件**: `published/text/novel.txt`

特点:
- 所有章节合并为单文件
- 移除YAML frontmatter
- 移除Markdown标记
- 统一中文标点
- 章节间空行分隔

示例输出:
```
第1章 废柴少年

乌坦城，萧家。

"萧炎哥哥，这是我给你带的糕点。"萧薰儿提着食盒，轻声说道。
...

第2章 药老现身

...
```

### 2. 带目录TXT (txt-toc)

**文件**: `published/text/novel-with-toc.txt`

特点:
- 文件开头包含目录
- 目录包含章节名和字数
- 便于快速定位

示例输出:
```
【目录】

第1章 废柴少年 (3,200字)
第2章 药老现身 (3,150字)
第3章 斗气觉醒 (2,980字)
...

总字数: 93,000字
总章节: 30章

═══════════════════════════════

第1章 废柴少年

乌坦城，萧家。
...
```

### 3. 分章TXT (txt-chapters)

**目录**: `published/text/chapters/`

特点:
- 每章单独文件
- 文件名: `001_废柴少年.txt`
- 便于分章上传

### 4. 起点中文网格式 (qidian)

**目录**: `published/platforms/qidian/`

特点:
- 符合起点上传规范
- 章节标题格式化
- 自动分卷(每100章一卷)
- 生成作品简介模板

文件结构:
```
qidian/
├── 作品简介.txt
├── 卷一_崛起之路/
│   ├── 001_第1章_废柴少年.txt
│   ├── 002_第2章_药老现身.txt
│   └── ...
└── 卷二_成长之旅/
    └── ...
```

### 5. 晋江文学城格式 (jjwxc)

**目录**: `published/platforms/jjwxc/`

特点:
- 符合晋江上传规范
- 自动添加作者按语位置
- 适配晋江字数统计

### 6. 番茄小说格式 (fanqie)

**目录**: `published/platforms/fanqie/`

特点:
- 符合番茄上传规范
- 每章2000-4000字优化
- 自动章节编号

### 7. 有声书TTS优化版 (audio)

**目录**: `published/audio/`

特点:
- 添加停顿标记
- 多音字注音
- 语气标注
- 长句分段

文件:
```
audio/
├── novel-tts.txt         # 纯文本TTS版
├── ssml/                 # SSML标记版
│   ├── chapter-001.xml
│   └── ...
└── tts-config.json       # TTS配置
```

TTS优化示例:
```xml
<speak>
  <p>
    <s>乌坦城<break time="300ms"/>萧家<break time="600ms"/></s>
  </p>
  <p>
    <s><prosody rate="medium">"萧炎哥哥，这是我给你带的糕点。"</prosody>
    萧薰儿提着食盒，轻声说道<break time="600ms"/></s>
  </p>
</speak>
```

## 执行流程

```
用户输入: /nw-release tts
  ↓
确定 project_id:
  ├─ 检查 productions/ 下有几个项目
  ├─ 如果只有一个 → 自动使用
  └─ 如果有多个 → 询问用户选择
  ↓
扫描章节:
  ├─ 读取 productions/{project_id}/chapters/
  └─ 统计章节数和总字数
  ↓
根据格式执行:
  ├─ tts → 调用 audiobook-optimizer，生成朗读文本
  ├─ txt → 调用 format-exporter，合并为单文件
  └─ md → 调用 format-exporter，去除 yml 头
  ↓
完成:
  └─ 提示文件位置
```

## 输出示例

### /nw-release all

```
开始发布导出...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 扫描章节...
  找到: 30个章节
  总字数: 93,000字

📄 导出 TXT 合集...
  ✓ releases/xuanhuan_001/text/full.txt

📝 导出 Markdown 发布版...
  ✓ releases/xuanhuan_001/markdown/ (30个文件)

🎧 导出 TTS 朗读文本...
  ✓ releases/xuanhuan_001/tts/scripts/ (30个文件)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 导出完成!
```

### /nw-release tts

```
🎧 导出 TTS 朗读文本...
  ✓ releases/xuanhuan_001/tts/scripts/001.txt
  ✓ releases/xuanhuan_001/tts/scripts/002.txt
  ...
  ✓ releases/xuanhuan_001/tts/scripts/030.txt

✅ 导出完成! 共30个文件
```

### 自然语言: "合成音频"

```
🎧 生成有声书...

1. 导出朗读文本...
  ✓ releases/xuanhuan_001/tts/scripts/ (30个文件)

2. 调用 edge-tts 合成音频...
  ✓ releases/xuanhuan_001/tts/audio/001.mp3
  ✓ releases/xuanhuan_001/tts/subtitles/001.srt
  ...

✅ 音频合成完成!
```

## 错误处理

### 错误1: 无章节文件

```
错误: productions/{project_id}/chapters/ 目录为空或不存在
建议: 请先创作章节,使用 /nw-ch-write 1-10
```

### 错误2: 章节不连续

```
警告: 章节文件不连续
缺失: chapter-005.md, chapter-012.md
建议: 补充缺失章节后重新导出
```

## 格式转换规则

### Markdown → 纯文本

```markdown
原始Markdown:
---
chapter_number: 1
title: 废柴少年
---

# 第1章 废柴少年

乌坦城，萧家。

**萧炎**缓缓睁开双眼。

> "这里是...萧家?"

转换后纯文本:
第1章 废柴少年

乌坦城，萧家。

萧炎缓缓睁开双眼。

"这里是...萧家?"
```

### 标点统一

- `"` → `"`
- `"` → `"`
- `'` → `'`
- `'` → `'`
- `...` → `……`
- `--` → `——`

### 段落处理

- 保留单个空行作为段落分隔
- 移除多余空行
- 章节间插入分隔符

## 有声书优化详情

### 停顿标记

| 标点 | 停顿时间 |
|------|----------|
| ， | 300ms |
| 。 | 600ms |
| ！ | 700ms |
| ？ | 800ms |
| …… | 500ms |
| 段落结束 | 1500ms |
| 章节结束 | 3000ms |

### 多音字标注

常见多音字自动标注:
- 萧(xiāo)
- 炎(yán)
- 斗(dòu)气
- 还(hái/huán)
- 朝(cháo/zhāo)

### 语气标注

对话语气自动识别:
- 怒喝 → `<prosody rate="fast" pitch="+20%">`
- 轻声 → `<prosody rate="slow" volume="-20%">`
- 冷笑 → `<prosody pitch="-10%">`
- 惊呼 → `<prosody rate="fast" volume="+30%">`

## 输出目录结构

```
releases/{project_id}/
├── tts/                       # 语音发布
│   ├── scripts/              # 朗读文本（去换行）
│   │   ├── 001.txt
│   │   └── ...
│   ├── audio/                # 音频文件（可选）
│   │   ├── 001.mp3
│   │   └── ...
│   └── subtitles/            # 字幕文件（可选）
│       ├── 001.srt
│       └── ...
│
├── text/
│   └── full.txt              # 完整合集
│
├── markdown/                  # 发布版 Markdown
│   ├── 001.md                # 去掉 yml 头
│   └── ...
│
└── reviews/                   # 审核报告
    ├── bp-audit-report.md    # 蓝图审核报告
    └── ch-audit-*.md         # 章节审核报告
```

## 各格式处理逻辑

| 格式 | 处理 |
|------|------|
| `tts` | 去换行、优化标点停顿、多音字标注 |
| `txt` | 合并所有章节为单文件、保留章节标题分隔 |
| `md` | 去掉 `---` yml frontmatter、保留正文 |

## 相关命令

- `/nw-ch-write` - 批量创作章节
- `/nw-ch-audit` - 审核章节质量

---

**提示**: 导出前建议先通过 `/nw-ch-audit` 审核，确保章节质量达标。
