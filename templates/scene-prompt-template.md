---
scene_number: {N}
chapter: {chapter_number}
timecode_start: "{HH:MM:SS}"
timecode_end: "{HH:MM:SS}"
duration_seconds: {seconds}
srt_range: [{start}, {end}]
characters: ["{角色1}", "{角色2}"]
location: "{地点}"
emotion: "{情绪}"
---

# 场景 {NNN}: {场景标题}

## 概览

| 属性 | 值 |
|------|---|
| 时间码 | {HH:MM:SS} - {HH:MM:SS} |
| 时长 | {seconds}秒 |
| 地点 | {地点} |
| 时段 | {清晨/白天/黄昏/夜晚} |
| 天气 | {晴朗/阴天/雨天/...} |
| 角色 | {角色列表} |
| 情绪 | {情绪关键词} |

---

## 静态图提示词

### Midjourney / DALL-E

```
{场景描述，英文}
{环境细节}
{人物描述，引用角色一致性标签}
{光线/氛围}
{风格关键词: cinematic, 4K, oriental fantasy, anime influenced}
--ar 16:9 --style raw --v 6
```

### 备选构图

**特写版**（用于情感高潮）:
```
{人物特写提示词}
--ar 3:4 --style raw
```

**大远景版**（用于场景建立）:
```
{环境大远景提示词}
--ar 21:9 --style raw
```

---

## 视频提示词

### Runway Gen-3

```
{Camera movement description}. {Scene description}. {Character actions}.
{Lighting and atmosphere}. {Duration: X seconds}.
```

### Kling AI

```
[场景: {地点}，{时段}]
{角色动作描述 - 中文}
镜头: {镜头运动}，{时长}
风格: {风格关键词}
```

### Sora / Veo

```
A cinematic scene in {location}. The camera {camera movement}.
{Detailed scene description including characters, actions, environment}.
{Lighting description}. Style: {style keywords}. Duration: {X} seconds.
```

### Pika / Luma

```
{简短场景描述}
Motion: {camera/subject motion}
Style: {style}
```

---

## Ken Burns 参数

```json
{
  "type": "{push_in|pull_out|pan_left|pan_right|pan_up|pan_down|diagonal}",
  "start": {
    "scale": 1.0,
    "x": 0.5,
    "y": 0.5
  },
  "end": {
    "scale": 1.3,
    "x": 0.5,
    "y": 0.45
  },
  "duration": {seconds},
  "easing": "ease-in-out"
}
```

### Ken Burns 类型选择指南

| 场景类型 | 推荐动画 | 说明 |
|----------|----------|------|
| 对话/对峙 | `push_in` | 缓慢推进增加紧张感 |
| 场景建立 | `pull_out` | 从细节拉远展示全貌 |
| 追逐/移动 | `pan_left/right` | 跟随运动方向 |
| 仰望/崇敬 | `pan_up` | 从下往上，增加威严感 |
| 俯瞰/压迫 | `pan_down` | 从上往下，增加压迫感 |
| 戏剧高潮 | `diagonal` | 斜向推进，增加动态感 |
| 平静/叙述 | `push_in` (慢速) | 微微推进，保持关注 |

---

## 角色一致性引用

> 从 `video/prompts/characters/{角色名}.md` 复制以下标签到提示词中

### {角色1}

```
{从角色一致性文件复制的英文标签}
```

### {角色2}

```
{从角色一致性文件复制的英文标签}
```

---

## 制作备注

- [ ] 图片已生成并放入 `video/images/scenes/scene-{NNN}.png`
- [ ] 检查角色一致性（与参考图对比）
- [ ] 确认画面比例正确（16:9）
- [ ] Ken Burns 参数已确认

---

## 参考

- 对应字幕: `tts/subtitles/{NNNN}.srt` 第 {start}-{end} 条
- 角色档案: `blueprints/{project_id}/characters/character-{角色名}.md`
- 世界观: `blueprints/{project_id}/worldview.md`
