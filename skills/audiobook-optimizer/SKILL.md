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
章节文件 → prepare-tts.py → TTS纯文本 → edge-tts → MP3音频 + SRT字幕
```

> **脚本位置**: 所有脚本位于插件根目录的 `scripts/` 子目录下。
>
> **查找脚本路径**:
> ```bash
> # 方法1: 使用 find 定位已安装插件的脚本
> SCRIPT_DIR=$(find ~/.claude/plugins/cache -path "*/novel-writer/*/scripts" -type d 2>/dev/null | head -1)
>
> # 方法2: 直接使用 edge-tts 命令（推荐，无需脚本）
> edge-tts --voice zh-CN-XiaoxiaoNeural --file input.txt --write-media output.mp3 --write-subtitles output.srt
> ```

### 步骤1: 准备 TTS 文本

**推荐方式**: 直接用 Python 处理，无需外部脚本：

```python
import re
import os

def prepare_tts(input_path, output_path):
    """将 Markdown 章节转换为 TTS 纯文本"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 去除 YAML frontmatter
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    # 去除 Markdown 标记
    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
    content = re.sub(r'\*(.+?)\*', r'\1', content)
    # 规范化空白
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
```

**备用方式**: 使用插件脚本（需先定位路径）：

```bash
# 先定位脚本目录
SCRIPT_DIR=$(find ~/.claude/plugins/cache -path "*/novel-writer/*/scripts" -type d 2>/dev/null | head -1)

# 处理所有章节
python "$SCRIPT_DIR/prepare-tts.py" productions/{project_id}/chapters/ releases/{project_id}/tts/scripts/novel-tts.txt

# 处理指定范围
python "$SCRIPT_DIR/prepare-tts.py" productions/{project_id}/chapters/ releases/{project_id}/tts/scripts/novel-tts.txt --range 1-10
```

脚本功能：
- 去除 YAML frontmatter
- 去除 Markdown 格式（#、**等）
- 合并段落，规范化空白
- 输出纯文本

### 步骤2: 生成音频（可选同时生成字幕）

**推荐方式**: 直接使用 edge-tts 命令：

```bash
# 生成单个文件的音频 + 字幕
edge-tts --voice zh-CN-XiaoxiaoNeural \
  --file releases/{project_id}/tts/scripts/0001.txt \
  --write-media releases/{project_id}/tts/audio/0001.mp3 \
  --write-subtitles releases/{project_id}/tts/subtitles/0001.srt

# 批量处理多个文件
for f in releases/{project_id}/tts/scripts/*.txt; do
  name=$(basename "$f" .txt)
  edge-tts --voice zh-CN-XiaoxiaoNeural \
    --file "$f" \
    --write-media "releases/{project_id}/tts/audio/${name}.mp3" \
    --write-subtitles "releases/{project_id}/tts/subtitles/${name}.srt"
done
```

**备用方式**: 使用插件脚本（支持并发）：

```bash
# 先定位脚本目录
SCRIPT_DIR=$(find ~/.claude/plugins/cache -path "*/novel-writer/*/scripts" -type d 2>/dev/null | head -1)

# 分章节并行生成（默认10并发）
python "$SCRIPT_DIR/generate-audio.py" releases/{project_id}/tts/scripts/novel-tts.txt releases/{project_id}/tts/audio/ --split-chapters

# 分章节 + 字幕
python "$SCRIPT_DIR/generate-audio.py" releases/{project_id}/tts/scripts/novel-tts.txt releases/{project_id}/tts/audio/ --split-chapters --write-subtitles

# 指定并发数（最高20）
python "$SCRIPT_DIR/generate-audio.py" releases/{project_id}/tts/scripts/novel-tts.txt releases/{project_id}/tts/audio/ --split-chapters --concurrency 15

# 指定音色和语速
python "$SCRIPT_DIR/generate-audio.py" input.txt output.mp3 --voice yunxi --rate +10%
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `--voice` | 音色，默认 xiaoxiao |
| `--rate` | 语速，如 +10% 或 -10% |
| `--volume` | 音量，如 +10% 或 -10% |
| `--split-chapters` | 分章节生成 |
| `--concurrency` | 并发数，1-20 |
| `--write-subtitles` | 同时生成 SRT 字幕 |
| `--subtitle-dir` | 指定字幕目录 |

---

## 可用音色

### 小说推荐音色
| 完整名称 | 性别 | 适用场景 | 特点 |
|----------|------|----------|------|
| zh-CN-YunxiNeural | 男 | 小说 | 阳光活泼，**默认男声** |
| zh-CN-XiaoxiaoNeural | 女 | 新闻/小说 | 温暖，**默认女声** |
| zh-CN-YunjianNeural | 男 | 体育/小说 | 热情 |
| zh-CN-XiaoyiNeural | 女 | 动漫/小说 | 活泼 |
| zh-CN-YunxiaNeural | 男 | 动漫/小说 | 可爱 |

查看所有中文音色：
```bash
edge-tts --list-voices | grep zh-CN
```

---

## 输出目录结构

```
releases/{project_id}/tts/
├── scripts/                # TTS 纯文本
│   ├── novel-tts.txt       # 合并文本
│   ├── 0001.txt            # 分章文本（可选）
│   └── ...
├── audio/                  # 音频文件
│   ├── novel.mp3           # 合并音频（可选）
│   ├── chapter-001.mp3     # 分章音频（可选）
│   └── ...
└── subtitles/              # 字幕文件（可选）
    ├── 0001.srt
    └── ...
```

---

## 使用示例

### 示例1: 完整流程（音频+字幕）

```bash
用户: "生成有声书"

执行:
1. 读取每个章节文件，用 Python 处理为 TTS 纯文本
2. 为每个 TTS 文本调用 edge-tts 生成音频和字幕

# 示例命令
edge-tts --voice zh-CN-XiaoxiaoNeural \
  --file releases/zongheng/tts/scripts/0001.txt \
  --write-media releases/zongheng/tts/audio/0001.mp3 \
  --write-subtitles releases/zongheng/tts/subtitles/0001.srt

输出:
✅ 有声书生成完成!
   TTS文本: releases/zongheng/tts/scripts/ (30个文件)
   音频文件: releases/zongheng/tts/audio/ (30个文件)
   字幕文件: releases/zongheng/tts/subtitles/ (30个文件)
```

### 示例2: 分章节批量生成（带字幕）

```bash
用户: "生成有声书，每章单独文件，带字幕"

执行:
# 批量处理所有章节
for f in releases/zongheng/tts/scripts/*.txt; do
  name=$(basename "$f" .txt)
  edge-tts --voice zh-CN-XiaoxiaoNeural \
    --file "$f" \
    --write-media "releases/zongheng/tts/audio/${name}.mp3" \
    --write-subtitles "releases/zongheng/tts/subtitles/${name}.srt"
done

输出:
✅ 有声书生成完成!
   章节数: 30
   输出目录: releases/zongheng/tts/audio/
   字幕目录: releases/zongheng/tts/subtitles/
```

### 示例3: 只准备文本（不生成音频）

```bash
用户: "准备TTS文本"

执行:
# 用 Python 处理章节为 TTS 文本（内联代码，见步骤1）

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
