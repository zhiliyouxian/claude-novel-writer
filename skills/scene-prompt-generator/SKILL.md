---
name: scene-prompt-generator
description: 根据分镜脚本为每个场景生成多平台图像/视频提示词（Midjourney、DALL-E、Runway、Kling、Sora 等）及 Ken Burns 动画参数。用户想要生成场景提示词、图像提示词时使用。
allowed-tools: Read, Write, Glob
---

# 场景提示词生成器

根据分镜脚本为每个场景生成多平台图像/视频提示词及 Ken Burns 动画参数。

> **目录结构规范**: `specs/directory-structure.md`
> **模板参考**: `templates/scene-prompt-template.md`

## 工作流程

```
releases/{project_id}/video/storyboard/storyboard.md
    ↓ 读取场景列表
    ↓ 引用角色一致性标签
    ↓ 生成多平台提示词
    ↓ 计算 Ken Burns 参数
releases/{project_id}/video/prompts/scenes/scene-{NNNN}.md
```

## 前置条件

必须先完成：
1. 角色提示词：`releases/{project_id}/video/prompts/characters/*.md`
2. 分镜脚本：`releases/{project_id}/video/storyboard/storyboard.md`

---

## 执行流程

### 步骤1: 读取分镜脚本

```bash
cat releases/{project_id}/video/storyboard/storyboard.md
```

提取场景列表和详情。

### 步骤2: 读取角色一致性标签

```bash
# 读取所有角色提示词文件
cat releases/{project_id}/video/prompts/characters/*.md
```

提取"复制用标签（英文）"部分。

### 步骤3: 读取世界观

```bash
cat blueprints/{project_id}/worldview.md
```

了解场景风格、地点描述等。

### 步骤4: 为每个场景生成提示词

对分镜中的每个场景：
1. 组合场景描述 + 角色标签
2. 转换为英文提示词
3. 适配各平台格式
4. 计算 Ken Burns 参数

### 步骤5: 输出文件

```bash
# 为每个场景创建提示词文件
releases/{project_id}/video/prompts/scenes/scene-0001.md
releases/{project_id}/video/prompts/scenes/scene-0002.md
...
```

---

## 多平台提示词格式

### 静态图（Midjourney / DALL-E）

```
{场景描述}
{环境细节: 地点、时间、天气、光线}
{角色描述: 引用一致性标签}
{动作/姿态}
{风格关键词: cinematic, 4K, xianxia style}
--ar 16:9 --style raw --v 6
```

### Runway Gen-3

```
{Camera movement}. {Scene description in present tense}.
{Character actions}. {Lighting and atmosphere}.
Duration: {N} seconds.
```

特点：
- 简洁直接
- 强调镜头运动
- 时长 4-10 秒

### Kling AI

```
[场景: {地点}，{时段}]
{角色动作描述 - 中文更好}
镜头: {镜头运动}，{时长}
风格: {风格关键词}
```

特点：
- 支持中文
- 结构化格式
- 国风效果好

### Sora / Veo

```
A cinematic scene in {location} at {time of day}.
The camera {starts with / slowly / smoothly} {camera movement}.
{Detailed description: characters, actions, environment, lighting}.
The atmosphere is {mood/emotion}.
Style: {style keywords}.
Duration: {N} seconds.
```

特点：
- 详细叙述
- 完整的场景构建
- 强调电影感

### Pika / Luma

```
{简短场景描述}
Motion: {camera or subject motion}
Style: {style keywords}
```

特点：
- 极简
- 强调动态
- 适合简单动画

---

## Ken Burns 参数计算

### 根据场景类型选择动画

| 场景类型 | Ken Burns 类型 | 参数 |
|----------|----------------|------|
| 对话/对峙 | `push_in` | scale: 1.0 → 1.3 |
| 场景建立 | `pull_out` | scale: 1.3 → 1.0 |
| 追逐/移动 | `pan_left/right` | x: 0.3 → 0.7 |
| 仰望 | `pan_up` | y: 0.7 → 0.3 |
| 俯瞰 | `pan_down` | y: 0.3 → 0.7 |
| 戏剧高潮 | `diagonal` | scale+x+y 组合 |

### 根据情绪调整速度

| 情绪 | 速度调整 | easing |
|------|----------|--------|
| 紧张 | 正常 | ease-in-out |
| 平静 | 慢 | ease-out |
| 激烈 | 快 | ease-in |
| 悬疑 | 很慢 | linear |

### 输出格式

```json
{
  "type": "push_in",
  "start": {"scale": 1.0, "x": 0.5, "y": 0.5},
  "end": {"scale": 1.3, "x": 0.5, "y": 0.45},
  "duration": 32,
  "easing": "ease-in-out"
}
```

---

## 场景描述转换规则

### 中文→英文转换

| 中文表达 | 英文提示词 |
|----------|------------|
| 宗门广场 | martial arts sect plaza |
| 山巅之上 | mountain peak, summit |
| 悬崖边 | cliff edge, precipice |
| 密林深处 | deep within the forest |
| 洞府内 | inside the cave dwelling |
| 拍卖会场 | auction hall |
| 战场之上 | battlefield |
| 皇宫大殿 | imperial palace throne room |

### 时间/光线

| 中文 | 英文 |
|------|------|
| 清晨 | dawn, golden hour, morning light |
| 正午 | midday, harsh sunlight |
| 黄昏 | dusk, sunset, golden hour |
| 夜晚 | night, moonlight, torchlight |
| 阴天 | overcast, soft diffused light |

### 情绪/氛围

| 情绪 | 氛围关键词 |
|------|------------|
| 紧张 | tense, dramatic shadows, suspenseful |
| 悲伤 | melancholic, soft light, muted colors |
| 愤怒 | intense, harsh contrast, red undertones |
| 喜悦 | warm, bright, vibrant colors |
| 神秘 | mysterious, foggy, ethereal |

---

## 输出示例

### scene-0001.md

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

## 概览

| 属性 | 值 |
|------|---|
| 时间码 | 00:00:00 - 00:00:32 |
| 时长 | 32秒 |
| 地点 | 外门广场 |
| 时段 | 清晨 |
| 角色 | 萧羽, 李傲天 |
| 情绪 | 紧张 |

---

## 静态图提示词

### Midjourney / DALL-E

\`\`\`
Dramatic confrontation scene in an ancient Chinese martial arts sect plaza
at dawn, two young men facing each other in the center,
protagonist: young man, angular face, short messy black hair, deep brown
intense eyes, wearing dark blue robes with silver cloud embroidery,
antagonist: arrogant young man in luxurious crimson robes with gold trim,
surrounded by disciples in a circle, traditional pagoda architecture,
golden hour lighting, cinematic composition, 4K, xianxia style
--ar 16:9 --style raw --v 6
\`\`\`

## 视频提示词

### Runway Gen-3

\`\`\`
Camera slowly pushes in on two young men facing off in an ancient Chinese
sect plaza. Morning light creates dramatic shadows. The protagonist in
dark blue robes stands defiant while his antagonist in crimson sneers.
Duration: 8 seconds.
\`\`\`

### Kling AI

\`\`\`
[场景: 古代宗门广场，清晨]
两名修士对峙 - 蓝袍青年冷静坚定，红袍贵公子轻蔑嘲讽
周围弟子围观，气氛紧张
镜头: 大远景缓慢推进至中景，8秒
风格: 电影感，东方玄幻
\`\`\`

### Sora / Veo

\`\`\`
A cinematic scene in an ancient Chinese martial arts sect courtyard at dawn.
The camera starts with a wide establishing shot showing traditional pagodas
and disciples forming a circle, then slowly pushes in to reveal two young
men in the center - a determined youth in dark blue robes facing a sneering
noble in expensive crimson robes. Golden morning light casts long shadows
across the stone plaza. The atmosphere is tense and confrontational.
Style: Epic fantasy, xianxia, anime-influenced. Duration: 8 seconds.
\`\`\`

---

## Ken Burns 参数

\`\`\`json
{
  "type": "push_in",
  "start": {"scale": 1.0, "x": 0.5, "y": 0.5},
  "end": {"scale": 1.3, "x": 0.5, "y": 0.45},
  "duration": 32,
  "easing": "ease-in-out"
}
\`\`\`

---

## 角色一致性引用

### 萧羽
\`\`\`
young man, angular face, sharp jawline, short messy black hair,
deep brown intense eyes, 175cm tall, slender athletic build,
wearing dark blue robes with silver cloud embroidery
\`\`\`

### 李傲天
\`\`\`
arrogant young man, well-groomed appearance, slightly taller,
expensive crimson robes with gold trim, condescending posture
\`\`\`
```

---

## 批量生成

支持批量生成所有场景的提示词：

```bash
# 遍历分镜中的所有场景
for scene in storyboard.scenes:
    generate_prompt(scene)
    write_file(f"scene-{scene.number:04d}.md")
```

---

## 注意事项

1. **角色一致性**: 始终引用角色一致性标签
2. **风格统一**: 同一章节保持风格关键词一致
3. **时长匹配**: 视频提示词时长 ≈ 场景时长 / 4（Ken Burns 会填充）
4. **可编辑**: 生成的提示词是建议，用户可自行调整
