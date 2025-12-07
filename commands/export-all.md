---
name: export-all
description: 一键导出所有章节为多种格式(TXT/平台格式/有声书)。用法: /export-all 或 /export-all --format txt
---

# 一键导出命令

快捷导出所有章节为多种发布格式的命令。

## 用法

```bash
/export-all [选项]
```

## 示例

```bash
# 导出所有格式(默认)
/export-all

# 只导出TXT纯文本
/export-all --format txt

# 只导出起点格式
/export-all --format qidian

# 导出有声书优化版
/export-all --format audio

# 导出指定章节范围
/export-all --range 1-100

# 组合选项
/export-all --format txt,audio --range 1-50
```

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
用户输入: /export-all
  ↓
解析选项: 默认导出所有格式
  ↓
扫描章节:
  ├─ 读取 productions/{project_id}/chapters/chapter-001.md ~ chapter-{N}.md
  ├─ 统计: 找到30个章节文件
  └─ 总字数: 93,000字
  ↓
格式转换:
  ├─ 调用 format-exporter Skill
  ├─ 移除Markdown标记
  ├─ 统一标点符号
  └─ 格式化章节标题
  ↓
For each 格式:
  ├─ 生成对应格式文件
  ├─ 显示进度
  └─ 验证输出
  ↓
有声书优化:
  ├─ 调用 audiobook-optimizer Skill
  ├─ 添加停顿标记
  ├─ 多音字注音
  └─ 生成SSML文件
  ↓
完成:
  ├─ 输出统计信息
  ├─ 生成导出报告
  └─ 提示文件位置
```

## 输出示例

### 完整导出

```
开始导出所有格式...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 扫描章节...
  找到: 30个章节
  总字数: 93,000字

📄 导出TXT纯文本...
  ✓ published/text/novel.txt (93,000字)
  ✓ published/text/novel-with-toc.txt (带目录)
  ✓ published/text/chapters/ (30个文件)

🏢 导出平台格式...
  ✓ published/platforms/qidian/ (起点中文网)
  ✓ published/platforms/jjwxc/ (晋江文学城)
  ✓ published/platforms/fanqie/ (番茄小说)

🎧 导出有声书格式...
  ✓ published/audio/novel-tts.txt (TTS优化版)
  ✓ published/audio/ssml/ (30个SSML文件)
  ✓ published/audio/tts-config.json (配置文件)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 导出完成!

导出统计:
- 章节数: 30章
- 总字数: 93,000字
- 预计朗读时长: 5.8小时

导出文件:
published/
├── text/
│   ├── novel.txt (93KB)
│   ├── novel-with-toc.txt (95KB)
│   └── chapters/ (30个文件)
├── platforms/
│   ├── qidian/ (起点格式)
│   ├── jjwxc/ (晋江格式)
│   └── fanqie/ (番茄格式)
└── audio/
    ├── novel-tts.txt (98KB)
    ├── ssml/ (30个SSML文件)
    └── tts-config.json

下一步建议:
1. 检查导出文件内容
2. 上传到对应平台
3. 使用TTS工具生成音频
```

### 指定格式导出

```
导出格式: txt

📄 导出TXT纯文本...
  ✓ published/text/novel.txt (93,000字)
  ✓ published/text/novel-with-toc.txt (带目录)
  ✓ published/text/chapters/ (30个文件)

✅ 导出完成!
文件位置: published/text/
```

## 选项说明

### --format

指定导出格式，多个格式用逗号分隔。

可选值:
- `txt` - TXT纯文本(含合并版、目录版、分章版)
- `qidian` - 起点中文网格式
- `jjwxc` - 晋江文学城格式
- `fanqie` - 番茄小说格式
- `audio` - 有声书TTS优化版
- `all` - 所有格式(默认)

### --range

指定导出章节范围。

示例:
- `--range 1-10` - 导出1-10章
- `--range 1-100` - 导出前100章
- 不指定则导出全部章节

### --output

指定输出目录(默认: published/)。

示例:
- `--output ~/Desktop/my-novel/`

## 错误处理

### 错误1: 无章节文件

```
错误: productions/{project_id}/chapters/ 目录为空或不存在
建议: 请先创作章节,使用 /write-chapters 1-10
```

### 错误2: 章节不连续

```
警告: 章节文件不连续
缺失: chapter-005.md, chapter-012.md
建议: 补充缺失章节或使用 --ignore-missing 选项
```

### 错误3: 格式错误

```
警告: chapter-007.md 格式不规范
问题: 缺少YAML frontmatter
建议: 运行 /review-batch 7 检查并修正
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

## 最佳实践

### 建议1: 审核后再导出

```bash
# 确保质量达标后再导出
/review-batch 1-30
# 修正问题
/export-all
```

### 建议2: 分批导出测试

```bash
# 先导出前10章测试
/export-all --range 1-10 --format txt

# 确认无误后导出全部
/export-all
```

### 建议3: 平台适配

```bash
# 根据目标平台选择格式
/export-all --format qidian   # 上传起点
/export-all --format jjwxc    # 上传晋江
```

## 与其他组件协作

### 被调用

- **用户直接调用**: `/export-all [选项]`

### 调用

- **format-exporter Skill**: 执行格式转换
- **audiobook-optimizer Skill**: 生成有声书格式

### 前置条件

- **productions/{project_id}/chapters/**: 必须存在章节文件
- **建议**: 先通过审核再导出

## 输出目录结构

```
published/
├── text/                          # 纯文本版
│   ├── novel.txt                  # 合并版
│   ├── novel-with-toc.txt         # 带目录版
│   └── chapters/                  # 分章版
│       ├── 001_废柴少年.txt
│       ├── 002_药老现身.txt
│       └── ...
│
├── platforms/                     # 平台格式
│   ├── qidian/                    # 起点中文网
│   │   ├── 作品简介.txt
│   │   ├── 卷一_崛起之路/
│   │   └── ...
│   ├── jjwxc/                     # 晋江文学城
│   └── fanqie/                    # 番茄小说
│
├── audio/                         # 有声书
│   ├── novel-tts.txt              # TTS纯文本版
│   ├── ssml/                      # SSML标记版
│   │   ├── chapter-001.xml
│   │   └── ...
│   └── tts-config.json            # TTS配置
│
└── export-report.md               # 导出报告
```

## 相关命令

- `/write-chapters 1-10` - 批量创作章节
- `/review-batch 1-10` - 批量审核章节
- `/revise-chapters 1,4,7` - 修改指定章节

---

**提示**: 导出前请确保所有章节已通过审核,避免导出后发现问题需要重新处理。
