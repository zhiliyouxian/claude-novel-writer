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

# 场景 {NNN}：{场景标题}

## 概览

| 属性 | 值 |
|------|---|
| 时间码 | {HH:MM:SS} - {HH:MM:SS} |
| 时长 | {seconds}秒 |
| 地点 | {地点} |
| 时段 | {清晨/白天/黄昏/夜晚} |
| 天气 | {晴朗/阴天/雨天} |
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
{风格关键词}
--ar 16:9 --style raw --v 6
```

### 备选构图

**特写版**：
```
{人物特写提示词}
--ar 3:4 --style raw
```

**大远景版**：
```
{环境大远景提示词}
--ar 21:9 --style raw
```

---

## 视频提示词

### Runway Gen-3

```
{Camera movement}. {Scene description}. {Character actions}.
{Lighting}. Duration: {X} seconds.
```

### Kling AI

```
[场景：{地点}，{时段}]
{角色动作描述}
镜头：{镜头运动}，{时长}
风格：{风格关键词}
```

### Sora / Veo

```
A cinematic scene in {location}. The camera {movement}.
{Detailed scene description}. {Lighting}.
Style: {style}. Duration: {X} seconds.
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

---

## 角色一致性引用

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
- [ ] 检查角色一致性
- [ ] 确认画面比例正确（16:9）
- [ ] Ken Burns 参数已确认
