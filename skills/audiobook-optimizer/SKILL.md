---
name: audiobook-optimizer
description: 有声书生成工具，将章节转换为TTS文本并生成音频文件。
allowed-tools: Read, Write, Bash, Glob
---

# 有声书生成器

将创作的章节转换为有声书音频文件。

> **目录结构规范**: `specs/directory-structure.md`

## 依赖检查

**必须先检查 edge-tts 是否安装**:

```bash
which edge-tts
```

如果未安装，提示用户：
```
❌ edge-tts 未安装

请执行以下命令安装:
pip install edge-tts
```

---

## 工作流程

```
章节文件 → 文本处理 → TTS纯文本 → edge-tts → MP3音频 + SRT字幕
```

### 步骤1: 准备 TTS 文本

读取章节文件，去除格式标记，输出纯文本。

**处理规则**:
- 去除 YAML frontmatter (`---` 包裹的内容)
- 去除 Markdown 标记 (`#`、`**`、`*` 等)
- 去除行号标记 (`数字→`)
- 规范化段落间距（合并多余空行）
- 保留章节标题

**输出**: `releases/{project_id}/tts/scripts/0001.txt`, `0002.txt`, ...

### 步骤2: 生成音频

直接调用 `edge-tts` 命令，**默认增量生成**（只处理有变更的文件）：

```bash
# 增量生成：只处理需要更新的文件
for f in releases/{project_id}/tts/scripts/*.txt; do
  name=$(basename "$f" .txt)
  audio_file="releases/{project_id}/tts/audio/${name}.mp3"

  # 增量检查：跳过已是最新的文件
  if [ -f "$audio_file" ] && [ "$audio_file" -nt "$f" ]; then
    echo "跳过 ${name} (已是最新)"
    continue
  fi

  echo "生成 ${name}.mp3 ..."
  edge-tts --voice zh-CN-YunxiNeural \
    --file "$f" \
    --write-media "$audio_file" \
    --write-subtitles "releases/{project_id}/tts/subtitles/${name}.srt"
done
```

**强制全量生成** (使用 `--force` 参数时):
```bash
for f in releases/{project_id}/tts/scripts/*.txt; do
  name=$(basename "$f" .txt)
  edge-tts --voice zh-CN-YunxiNeural \
    --file "$f" \
    --write-media "releases/{project_id}/tts/audio/${name}.mp3" \
    --write-subtitles "releases/{project_id}/tts/subtitles/${name}.srt"
done
```

---

## edge-tts 参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--voice` | 音色 | `zh-CN-YunxiNeural` |
| `--file` | 输入文本文件 | `input.txt` |
| `--write-media` | 输出音频文件 | `output.mp3` |
| `--write-subtitles` | 输出字幕文件 | `output.srt` |
| `--rate` | 语速调整 | `+10%` 或 `-10%` |
| `--volume` | 音量调整 | `+10%` 或 `-10%` |

---

## 可用音色

### 小说推荐音色

| 完整名称 | 性别 | 适用场景 | 特点 |
|----------|------|----------|------|
| zh-CN-YunxiNeural | 男 | 小说 | 阳光活泼，**默认** |
| zh-CN-XiaoxiaoNeural | 女 | 新闻/小说 | 温暖 |
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
│   ├── 0001.txt
│   ├── 0002.txt
│   └── ...
├── audio/                  # 音频文件
│   ├── 0001.mp3
│   ├── 0002.mp3
│   └── ...
└── subtitles/              # 字幕文件
    ├── 0001.srt
    ├── 0002.srt
    └── ...
```

---

## 使用示例

### 示例1: 生成有声书（音频+字幕）

```
用户: "生成有声书"

执行:
1. 检查 edge-tts 是否安装
2. 读取章节，生成 TTS 纯文本
3. 调用 edge-tts 生成音频和字幕

输出:
✅ 有声书生成完成!
   TTS文本: releases/{project_id}/tts/scripts/ (30个文件)
   音频文件: releases/{project_id}/tts/audio/ (30个文件)
   字幕文件: releases/{project_id}/tts/subtitles/ (30个文件)
```

### 示例2: 只生成 TTS 文本

```
用户: "准备TTS文本"

执行:
1. 读取章节，去除格式标记
2. 输出纯文本到 tts/scripts/

输出:
✅ TTS文本准备完成!
   文件: releases/{project_id}/tts/scripts/ (30个文件)
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

1. **依赖检查**: 必须先确认 edge-tts 已安装
2. **网络要求**: edge-tts 需要联网调用微软 TTS 服务
3. **长文本**: 超长文本建议分章节生成，避免超时
4. **音色选择**: 默认 YunxiNeural (男声)，女主视角用 XiaoxiaoNeural

---

激活条件: 用户说"生成有声书"、"TTS"、"朗读版"、"合成音频"等关键词
