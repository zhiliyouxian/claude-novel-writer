---
name: audiobook-optimizer
description: 有声书生成工具，将章节转换为TTS文本并生成音频文件。
allowed-tools: Read, Write, Bash, Glob
---

# 有声书生成器

将创作的章节转换为有声书音频文件。

> **目录结构规范**: `specs/directory-structure.md`

## 工作流程

```
章节文件 → prepare-tts.py → TTS纯文本 → edge-tts → MP3音频
```

### 步骤1: 准备 TTS 文本

使用 `scripts/prepare-tts.py` 处理章节：

```bash
# 处理所有章节
python scripts/prepare-tts.py productions/{project_id}/chapters/ releases/{project_id}/audio/novel-tts.txt

# 处理指定范围
python scripts/prepare-tts.py productions/{project_id}/chapters/ releases/{project_id}/audio/novel-tts.txt --range 1-10

# 处理单个章节
python scripts/prepare-tts.py productions/{project_id}/chapters/ releases/{project_id}/audio/chapter-001.txt --single 1
```

脚本功能：
- 去除 YAML frontmatter
- 去除 Markdown 格式（#、**等）
- 合并段落，规范化空白
- 输出纯文本

### 步骤2: 生成音频

使用 `scripts/generate-audio.py` 调用 edge-tts：

```bash
# 生成单个合并音频
python scripts/generate-audio.py releases/{project_id}/audio/novel-tts.txt releases/{project_id}/audio/novel.mp3

# 分章节生成
python scripts/generate-audio.py releases/{project_id}/audio/novel-tts.txt releases/{project_id}/audio/chapters/ --split-chapters

# 指定音色和语速
python scripts/generate-audio.py input.txt output.mp3 --voice yunxi --rate +10%
```

---

## 可用音色

### 女声（推荐）
| 快捷名 | 完整名称 | 特点 |
|--------|----------|------|
| xiaoxiao | zh-CN-XiaoxiaoNeural | 温柔女声，推荐 |
| xiaoyan | zh-CN-XiaoyanNeural | 甜美女声 |
| xiaochen | zh-CN-XiaochenNeural | 成熟女声 |

### 男声
| 快捷名 | 完整名称 | 特点 |
|--------|----------|------|
| yunxi | zh-CN-YunxiNeural | 年轻男声，推荐 |
| yunjian | zh-CN-YunjianNeural | 成熟男声 |
| yunyang | zh-CN-YunyangNeural | 新闻播报风格 |

查看所有音色：
```bash
python scripts/generate-audio.py --list-voices
```

---

## 输出目录结构

```
releases/{project_id}/audio/
├── novel-tts.txt           # TTS 纯文本
├── novel.mp3               # 合并音频（可选）
└── chapters/               # 分章音频（可选）
    ├── chapter-001.mp3
    ├── chapter-002.mp3
    └── ...
```

---

## 使用示例

### 示例1: 完整流程

```bash
用户: "生成有声书"

执行:
1. python scripts/prepare-tts.py productions/zongheng/chapters/ releases/zongheng/audio/novel-tts.txt
2. python scripts/generate-audio.py releases/zongheng/audio/novel-tts.txt releases/zongheng/audio/novel.mp3

输出:
✅ 有声书生成完成!
   TTS文本: releases/zongheng/audio/novel-tts.txt (9.5万字)
   音频文件: releases/zongheng/audio/novel.mp3 (约6小时)
```

### 示例2: 分章节生成

```bash
用户: "生成有声书，每章单独文件"

执行:
1. python scripts/prepare-tts.py ...
2. python scripts/generate-audio.py ... --split-chapters

输出:
✅ 有声书生成完成!
   章节数: 30
   输出目录: releases/zongheng/audio/chapters/
```

### 示例3: 只准备文本（不生成音频）

```bash
用户: "准备TTS文本"

执行:
python scripts/prepare-tts.py productions/zongheng/chapters/ releases/zongheng/audio/novel-tts.txt

输出:
✅ TTS文本准备完成!
   可使用任意TTS工具朗读
```

---

## 依赖安装

```bash
pip install edge-tts
```

---

## 预计时长

| 字数 | 预计时长 |
|------|----------|
| 3万字 | ~1.5小时 |
| 10万字 | ~5.5小时 |
| 30万字 | ~16小时 |

计算公式：字数 ÷ 300字/分钟

---

## 注意事项

1. **网络要求**: edge-tts 需要联网调用微软 TTS 服务
2. **长文本**: 超长文本建议分章节生成，避免超时
3. **音色选择**: 小说推荐 xiaoxiao（女声）或 yunxi（男声）
4. **语速调整**: 可通过 --rate 调整，如 +10% 加快、-10% 减慢

---

激活条件: 用户说"生成有声书"、"TTS"、"朗读版"等关键词
