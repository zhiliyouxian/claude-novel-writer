---
name: character-visual-prompter
description: 从蓝图角色档案提取外貌描述，生成 Midjourney/DALL-E 等图像生成工具的英文提示词，确保角色视觉一致性。用户想要生成角色参考图提示词时使用。
allowed-tools: Read, Write, Glob
---

# 角色视觉提示词生成器

从蓝图角色档案生成 AI 图像生成提示词，确保角色视觉一致性。

> **目录结构规范**: `specs/directory-structure.md`

## 工作流程

```
blueprints/{project_id}/characters/character-{name}.md
    ↓ 读取外貌描述
    ↓ 转换为英文提示词
    ↓ 生成多种尺寸版本
releases/{project_id}/video/prompts/characters/{name}.md
```

## 执行流程

### 步骤1: 扫描角色档案

```bash
# 查找所有角色档案
ls blueprints/{project_id}/characters/character-*.md
```

### 步骤2: 读取角色信息

从每个角色档案提取：

| 字段 | 来源 |
|------|------|
| 角色名 | YAML frontmatter `name` |
| 角色定位 | YAML frontmatter `role` |
| 年龄外观 | 视觉参考表格 |
| 身材 | 视觉参考表格 |
| 发型发色 | 视觉参考表格 |
| 眼睛 | 视觉参考表格 |
| 特征 | 视觉参考表格 |
| 服饰 | 视觉参考表格 |

### 步骤3: 生成提示词

为每个角色生成：

1. **一致性标签**（英文，用于复制粘贴）
2. **头像提示词**（3:4 比例）
3. **全身提示词**（2:3 比例）
4. **动作姿势**（可选）

### 步骤4: 写入输出文件

```bash
# 输出位置
releases/{project_id}/video/prompts/characters/{角色名}.md
```

---

## 输出格式

```markdown
---
character: {角色名}
role: {protagonist/heroine/mentor/antagonist/supporting}
generated: {YYYY-MM-DD}
---

# {角色名} - 视觉参考提示词

## 一致性标签

| 特征 | 描述 |
|------|------|
| 脸型 | {描述} |
| 头发 | {描述} |
| 眼睛 | {描述} |
| 身材 | {描述} |
| 服饰 | {描述} |
| 风格锚点 | "{一句话描述}" |

## 复制用标签（英文）

\`\`\`
{英文外貌描述，用于复制到其他提示词中}
\`\`\`

## 头像提示词 (3:4)

\`\`\`
{Midjourney/DALL-E 格式的头像提示词}
--ar 3:4 --style raw
\`\`\`

## 全身提示词 (2:3)

\`\`\`
{全身照提示词}
--ar 2:3 --style raw
\`\`\`

## 动作姿势

### 战斗姿态
\`\`\`
{战斗场景提示词}
\`\`\`

### 日常状态
\`\`\`
{日常场景提示词}
\`\`\`
```

---

## 提示词生成规则

### 外貌描述转换

| 中文描述 | 英文提示词 |
|----------|------------|
| 剑眉星目 | sword-like eyebrows, bright star-like eyes |
| 面如冠玉 | jade-like complexion, handsome features |
| 国字脸 | square face, strong jawline |
| 瓜子脸 | oval face, delicate features |
| 柳叶眉 | willow-leaf shaped eyebrows |
| 丹凤眼 | phoenix eyes, upturned corners |
| 身材修长 | tall and slender build |
| 虎背熊腰 | broad shoulders, muscular build |

### 风格关键词

根据小说类型添加：

| 类型 | 风格关键词 |
|------|------------|
| 玄幻/仙侠 | xianxia style, oriental fantasy, Chinese cultivation |
| 都市 | modern urban, contemporary, realistic |
| 历史 | historical Chinese, ancient China, period accurate |
| 奇幻 | western fantasy, medieval, magical |

### 质量关键词

必须包含：
- `4K, highly detailed`
- `cinematic lighting`
- `portrait/full body shot`
- 比例参数：`--ar 3:4` 或 `--ar 2:3`

---

## 角色一致性策略

### 1. 建立锚点

为每个角色创建"风格锚点"短语：
- 主角："年轻的剑修，眼神坚定"
- 女主："冷艳的冰系天才，不食人间烟火"
- 导师："白发苍苍的老者，仙风道骨"

### 2. 特征优先级

按重要性排列外貌特征：
1. 面部特征（最易识别）
2. 发型发色
3. 标志性服饰/配饰
4. 体型姿态

### 3. 负面提示词

避免不一致：
```
--no multiple people, --no deformed, --no extra limbs
```

---

## 使用示例

### 示例1: 主角

输入（角色档案）:
```markdown
## 视觉参考
| 特征 | 描述 |
|------|------|
| 年龄外观 | 20岁左右 |
| 身材 | 175cm，清瘦但健壮 |
| 发型发色 | 黑色短发，略显凌乱 |
| 眼睛 | 深褐色，眼神锐利 |
| 服饰 | 深蓝色道袍，银色云纹 |
```

输出（提示词）:
```
A 20-year-old East Asian man with sharp angular features,
short messy black hair, deep brown eyes with an intense gaze,
wearing a dark blue traditional Chinese robe with silver cloud embroidery,
portrait style, cinematic lighting, 4K, highly detailed, xianxia style
--ar 3:4 --style raw
```

---

## 注意事项

1. **一致性**: 同一角色的所有提示词使用相同的核心描述
2. **可编辑**: 生成的提示词用户可自行调整
3. **多尝试**: 建议生成3-5张图片选择最满意的作为参考
