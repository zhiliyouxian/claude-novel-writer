---
name: video-assembler
description: 根据分镜文件，将图片、动画、音频、字幕合成为完整视频。读取分镜 YAML 中的镜头运动参数，生成 ffmpeg 命令执行合成。用户想要合成视频、拼接视频时使用。
allowed-tools: Read, Bash, Glob
---

# 视频合成器

根据分镜文件中的参数，将镜头图片合成为带动画、音频、字幕的完整视频。

> **目录结构规范**: `specs/directory-structure.md`

## 输入文件

1. **分镜文件** — 包含镜头参数
   ```
   releases/{project_id}/video/storyboard/chapter-{NNNN}.yaml
   ```

2. **镜头图片** — 每个镜头对应一张图（按章节分目录）
   ```
   releases/{project_id}/video/images/shots/chapter-{NNNN}/shot-{NNN}.png
   ```

3. **音频文件**
   ```
   releases/{project_id}/tts/audio/{NNNN}.mp3
   ```

4. **字幕文件**
   ```
   releases/{project_id}/tts/subtitles/{NNNN}.srt
   ```

## 文件命名规范

| 文件类型 | 命名格式 | 示例 |
|----------|----------|------|
| 分镜文件 | `chapter-{NNNN}.yaml` | `chapter-0001.yaml` |
| 镜头图片目录 | `chapter-{NNNN}/` | `chapter-0001/` |
| 镜头图片 | `shot-{NNN}.png` | `shot-001.png` |
| 动画片段 | `shot-{NNN}.mp4` | `shot-001.mp4` |
| 输出视频 | `chapter-{NNNN}.mp4` | `chapter-0001.mp4` |

**说明**：
- 章节号 `{NNNN}` 使用四位数补零
- 镜头号 `{NNN}` 使用三位数补零，每章从 001 开始

---

## 工作流程

```
1. 读取分镜文件
    ↓
2. 检查图片是否齐全
    ↓
3. 为每个镜头生成 Ken Burns 动画
    ↓
4. 拼接所有视频片段
    ↓
5. 添加音频
    ↓
6. 烧录字幕
    ↓
7. 输出最终视频
```

---

## 依赖检查

执行前必须检查 ffmpeg：

```bash
which ffmpeg || echo "❌ ffmpeg 未安装"
```

如未安装，提示用户：
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`

---

## 步骤1: 读取分镜文件

从 YAML 文件中读取每个镜头的参数：

```yaml
shots:
  - id: "001"
    duration: 32.5
    camera:
      type: "push_in"
      start_scale: 1.0
      end_scale: 1.3
      start_position: [0.5, 0.5]
      end_position: [0.5, 0.45]
```

---

## 步骤2: 检查图片

```bash
# 检查所有镜头图片是否存在
for shot in 001 002 003 ...; do
  [ -f "releases/{project_id}/video/images/shots/shot-${shot}.png" ] || echo "缺少 shot-${shot}.png"
done
```

---

## 步骤3: 生成 Ken Burns 动画

### ffmpeg zoompan 滤镜

Ken Burns 效果通过 ffmpeg 的 `zoompan` 滤镜实现。

**命令模板**:

```bash
ffmpeg -y -loop 1 -i {input_image} \
  -vf "zoompan=z='min(max({start_scale}+{scale_delta}*(on-1),1),10)':x='(iw-iw/zoom)*({start_x}+{x_delta}*(on-1))':y='(ih-ih/zoom)*({start_y}+{y_delta}*(on-1))':d={total_frames}:s=1920x1080:fps=30" \
  -t {duration} \
  -c:v libx264 -pix_fmt yuv420p -preset medium -crf 23 \
  {output_video}
```

### 参数计算

| 参数 | 计算公式 |
|------|----------|
| `total_frames` | duration × 30 (fps) |
| `scale_delta` | (end_scale - start_scale) / total_frames |
| `x_delta` | (end_x - start_x) / total_frames |
| `y_delta` | (end_y - start_y) / total_frames |

### 示例

**分镜参数**:
```yaml
duration: 30
camera:
  type: "push_in"
  start_scale: 1.0
  end_scale: 1.3
  start_position: [0.5, 0.5]
  end_position: [0.5, 0.45]
```

**计算**:
- total_frames = 30 × 30 = 900
- scale_delta = (1.3 - 1.0) / 900 = 0.000333
- x_delta = (0.5 - 0.5) / 900 = 0
- y_delta = (0.45 - 0.5) / 900 = -0.0000556

**生成命令**:

```bash
ffmpeg -y -loop 1 -i shot-001.png \
  -vf "zoompan=z='min(max(1.0+0.000333*(on-1),1),10)':x='(iw-iw/zoom)*(0.5+0*(on-1))':y='(ih-ih/zoom)*(0.5+-0.0000556*(on-1))':d=900:s=1920x1080:fps=30" \
  -t 30 \
  -c:v libx264 -pix_fmt yuv420p -preset medium -crf 23 \
  shot-001.mp4
```

### 镜头运动预设

当分镜只指定 `type` 而没有详细参数时，使用预设值：

| 类型 | start_scale | end_scale | start_pos | end_pos |
|------|-------------|-----------|-----------|---------|
| push_in | 1.0 | 1.3 | [0.5, 0.5] | [0.5, 0.45] |
| pull_out | 1.3 | 1.0 | [0.5, 0.5] | [0.5, 0.5] |
| pan_left | 1.2 | 1.2 | [0.7, 0.5] | [0.3, 0.5] |
| pan_right | 1.2 | 1.2 | [0.3, 0.5] | [0.7, 0.5] |
| pan_up | 1.2 | 1.2 | [0.5, 0.7] | [0.5, 0.3] |
| pan_down | 1.2 | 1.2 | [0.5, 0.3] | [0.5, 0.7] |
| static | 1.0 | 1.0 | [0.5, 0.5] | [0.5, 0.5] |

---

## 步骤4: 拼接视频片段

### 创建 concat 文件

```bash
# 创建 concat.txt
> releases/{project_id}/video/concat.txt
for f in releases/{project_id}/video/clips/shot-*.mp4; do
  echo "file '$(realpath "$f")'" >> releases/{project_id}/video/concat.txt
done
```

### 执行拼接

```bash
ffmpeg -y -f concat -safe 0 \
  -i releases/{project_id}/video/concat.txt \
  -c copy \
  releases/{project_id}/video/temp/concat.mp4
```

---

## 步骤5: 添加音频

```bash
ffmpeg -y \
  -i releases/{project_id}/video/temp/concat.mp4 \
  -i releases/{project_id}/tts/audio/0001.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  -map 0:v:0 -map 1:a:0 \
  releases/{project_id}/video/temp/with_audio.mp4
```

**说明**:
- `-shortest`: 以较短的流为准（音频或视频）
- `-c:v copy`: 视频流直接复制，不重新编码
- `-c:a aac`: 音频转为 AAC 格式

---

## 步骤6: 烧录字幕

```bash
ffmpeg -y \
  -i releases/{project_id}/video/temp/with_audio.mp4 \
  -vf "subtitles='releases/{project_id}/tts/subtitles/0001.srt':force_style='FontSize=28,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" \
  -c:a copy \
  releases/{project_id}/video/output/chapter-0001.mp4
```

### 字幕样式参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| FontSize | 字体大小 | 28 |
| PrimaryColour | 字体颜色 (BGR) | &HFFFFFF (白) |
| OutlineColour | 描边颜色 | &H000000 (黑) |
| Outline | 描边宽度 | 2 |
| Shadow | 阴影 | 1 |
| MarginV | 底部边距 | 30 |

**完整样式示例**:
```
FontSize=28,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Shadow=1,MarginV=30
```

### 或: 添加字幕轨道（不烧录）

```bash
ffmpeg -y \
  -i releases/{project_id}/video/temp/with_audio.mp4 \
  -i releases/{project_id}/tts/subtitles/0001.srt \
  -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=chi \
  releases/{project_id}/video/output/chapter-0001.mp4
```

---

## 输出

```
releases/{project_id}/video/output/chapter-{NNNN}.mp4
```

---

## 完整执行示例

以第1章为例：

```bash
# 1. 检查依赖
which ffmpeg

# 2. 创建目录
mkdir -p releases/{project_id}/video/clips/chapter-0001
mkdir -p releases/{project_id}/video/temp
mkdir -p releases/{project_id}/video/output

# 3. 生成每个镜头的动画 (循环执行)
ffmpeg -y -loop 1 -i releases/{project_id}/video/images/shots/chapter-0001/shot-001.png \
  -vf "zoompan=z='min(max(1.0+0.000333*(on-1),1),10)':x='(iw-iw/zoom)*(0.5)':y='(ih-ih/zoom)*(0.5+-0.0000556*(on-1))':d=900:s=1920x1080:fps=30" \
  -t 30 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 23 \
  releases/{project_id}/video/clips/chapter-0001/shot-001.mp4

# ... 重复其他镜头 ...

# 4. 创建 concat 文件
> releases/{project_id}/video/concat.txt
for f in releases/{project_id}/video/clips/chapter-0001/shot-*.mp4; do
  echo "file '$(realpath "$f")'" >> releases/{project_id}/video/concat.txt
done

# 5. 拼接
ffmpeg -y -f concat -safe 0 \
  -i releases/{project_id}/video/concat.txt \
  -c copy \
  releases/{project_id}/video/temp/concat.mp4

# 6. 添加音频
ffmpeg -y \
  -i releases/{project_id}/video/temp/concat.mp4 \
  -i releases/{project_id}/tts/audio/0001.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  -map 0:v:0 -map 1:a:0 \
  releases/{project_id}/video/temp/with_audio.mp4

# 7. 烧录字幕
ffmpeg -y \
  -i releases/{project_id}/video/temp/with_audio.mp4 \
  -vf "subtitles='releases/{project_id}/tts/subtitles/0001.srt':force_style='FontSize=28,PrimaryColour=&HFFFFFF,Outline=2'" \
  -c:a copy \
  releases/{project_id}/video/output/chapter-0001.mp4

# 8. 清理临时文件（可选）
rm -rf releases/{project_id}/video/temp
rm releases/{project_id}/video/concat.txt
```

---

## 错误处理

### 图片缺失

```markdown
⚠️ 缺少镜头图片

分镜要求 24 个镜头，但只找到 22 张图片。
缺失: shot-005.png, shot-012.png

请补充缺失图片后重试。
```

### ffmpeg 错误

```markdown
❌ 视频处理失败

错误: {ffmpeg 输出}

可能原因:
1. 图片分辨率不一致 → 请统一为 1920x1080
2. 图片格式不支持 → 请使用 PNG 或 JPG
3. 磁盘空间不足
```

### 音视频时长不匹配

```markdown
⚠️ 时长不匹配

视频总时长: 00:12:35
音频时长: 00:12:40

已使用 -shortest 参数，以视频时长为准。
```

---

## 注意事项

1. **图片分辨率** — 建议统一为 1920x1080
2. **文件命名** — 镜头图片必须按 shot-001.png 格式命名
3. **执行顺序** — 必须按流程顺序执行
4. **磁盘空间** — 确保有足够空间存储中间文件
5. **字幕路径** — ffmpeg 字幕滤镜中的路径需要转义冒号
