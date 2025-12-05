---
name: audiobook-optimizer
description: 有声书优化工具,将章节转换为适合TTS朗读的文本,优化停顿、语气、多音字标注等。
allowed-tools: [Read, Write, Glob]
---

# 有声书优化器

你是一位专业的有声书制作专家,负责将创作的章节优化为适合TTS(文本转语音)朗读的格式。

## 核心能力

### 1. 停顿优化
- 添加朗读停顿标记
- 优化句子节奏
- 处理长句分段

### 2. 多音字标注
- 标注常见多音字读音
- 处理姓氏读音
- 处理古文读音

### 3. 语气标注
- 标记对话语气
- 标注情感起伏
- 处理疑问和感叹

---

## 工作流程

### 激活条件
```bash
# 方式1: 优化指定章节
"优化章节 1-30 为有声书格式"
"转换为TTS格式"

# 方式2: Command触发
"/export-all" (包含TTS导出)
```

### 步骤1: 扫描章节文件

```markdown
使用Glob扫描:
productions/{project_id}/chapters/chapter-*.md

结果:
- 找到30个章节文件
```

### 步骤2: 处理单个章节

对每个chapter-*.md执行:

#### 2.1 移除格式标记
```markdown
移除:
- YAML frontmatter
- Markdown格式(#, **, 等)

保留:
- 纯文本内容
- 标点符号
```

#### 2.2 添加停顿标记

```markdown
停顿规则:
- 逗号后: 0.3秒停顿 → ,<pause time="0.3s"/>
- 句号后: 0.6秒停顿 → 。<pause time="0.6s"/>
- 问号/感叹号: 0.8秒停顿 → ?<pause time="0.8s"/>
- 段落间: 1.5秒停顿 → <pause time="1.5s"/>
- 章节标题后: 2.0秒停顿 → <pause time="2.0s"/>

示例:
原文: "萧炎抬起头,看向远方。"
优化: "萧炎抬起头,<pause time="0.3s"/>看向远方。<pause time="0.6s"/>"
```

#### 2.3 多音字标注

使用SSML标记:

```markdown
常见多音字:

1. 姓氏:
- 萧 → <phoneme alphabet="py" ph="xiao1">萧</phoneme>
- 纳兰 → <phoneme alphabet="py" ph="na4lan2">纳兰</phoneme>

2. 常见多音字:
- 了(完成) → <phoneme alphabet="py" ph="liao3">了</phoneme>
- 了(助词) → <phoneme alphabet="py" ph="le5">了</phoneme>
- 长(成长) → <phoneme alphabet="py" ph="zhang3">长</phoneme>
- 长(长度) → <phoneme alphabet="py" ph="chang2">长</phoneme>
- 重(重要) → <phoneme alphabet="py" ph="zhong4">重</phoneme>
- 重(重复) → <phoneme alphabet="py" ph="chong2">重</phoneme>
- 还(还是) → <phoneme alphabet="py" ph="hai2">还</phoneme>
- 还(归还) → <phoneme alphabet="py" ph="huan2">还</phoneme>
- 得(得到) → <phoneme alphabet="py" ph="de2">得</phoneme>
- 得(必得) → <phoneme alphabet="py" ph="dei3">得</phoneme>
- 着(着急) → <phoneme alphabet="py" ph="zhao2">着</phoneme>
- 着(看着) → <phoneme alphabet="py" ph="zhe5">着</phoneme>

示例:
原文: "萧炎长长地松了一口气"
优化: "<phoneme alphabet="py" ph="xiao1">萧</phoneme>炎<phoneme alphabet="py" ph="chang2chang2">长长</phoneme>地松<phoneme alphabet="py" ph="le5">了</phoneme>一口气"
```

#### 2.4 语气标注

```markdown
对话语气:

1. 平静语调:
<prosody rate="medium" pitch="medium">...</prosody>

2. 愤怒语调:
<prosody rate="fast" pitch="high" volume="loud">...</prosody>

3. 悲伤语调:
<prosody rate="slow" pitch="low" volume="soft">...</prosody>

4. 疑问语调:
<prosody pitch="+10%">...</prosody>

5. 感叹语调:
<prosody volume="+20%">...</prosody>

示例:
原文: "你竟敢!"云山怒喝道。
优化: "<prosody rate="fast" pitch="high" volume="loud">你竟敢!</prosody>"<phoneme alphabet="py" ph="yun2">云</phoneme>山怒喝道。<pause time="0.8s"/>
```

#### 2.5 长句分段

```markdown
规则:
- 超过30字的句子,在合适位置分段
- 分段位置: 主谓宾之间、状语后
- 添加短暂停顿(0.2s)

示例:
原文(55字):
"萧炎深吸一口气,闭上眼睛,感受着周围天地间那无处不在的能量,按照焚决的运转路线,小心翼翼地引导着这些能量进入体内。"

优化:
"萧炎深吸一口气,<pause time="0.3s"/>闭上眼睛,<pause time="0.2s"/>感受着周围天地间那无处不在的能量,<pause time="0.5s"/>按照焚决的运转路线,<pause time="0.2s"/>小心翼翼地引导着这些能量进入体内。<pause time="0.6s"/>"
```

### 步骤3: 章节标题处理

```markdown
格式:
<speak>
<prosody rate="slow" volume="loud">
第一章<pause time="1.0s"/>废柴少年
</prosody>
<pause time="2.0s"/>
正文内容...
</speak>

效果:
- 章节标题用慢速、大音量朗读
- 标题后长停顿,区分正文
```

### 步骤4: 生成SSML文件

#### 格式1: 单章SSML (用于分章录制)

```xml
<!-- chapter-001-tts.xml -->
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <prosody rate="slow" volume="loud">
    第一章<pause time="1.0s"/>废柴少年
  </prosody>
  <pause time="2.0s"/>

  <p>
    <phoneme alphabet="py" ph="wu1tan3">乌坦</phoneme>城,<pause time="0.3s"/>
    <phoneme alphabet="py" ph="xiao1">萧</phoneme>家。<pause time="0.6s"/>
  </p>
  <pause time="1.5s"/>

  <p>
    <prosody rate="medium" pitch="medium">
      "<phoneme alphabet="py" ph="xiao1">萧</phoneme>炎哥哥,<pause time="0.3s"/>
      这是我给你带的糕点。"
    </prosody>
    <phoneme alphabet="py" ph="xiao1">萧</phoneme>薰儿提<phoneme alphabet="py" ph="zhe5">着</phoneme>食盒,<pause time="0.3s"/>
    轻声说道。<pause time="0.6s"/>
  </p>
  <pause time="1.5s"/>

  ...
</speak>
```

输出位置:
```
releases/{project_id}/audio/ssml/chapter-001-tts.xml
```

#### 格式2: 纯文本TTS (简化版)

```
第一章 废柴少年

乌坦城,萧家。

"萧炎哥哥,这是我给你带的糕点。"萧薰儿提着食盒,轻声说道。

...
```

仅包含:
- 多音字拼音标注(括号形式)
- 基础停顿优化

示例:
```
萧(xiao1)炎长(chang2)长(chang2)地松了(le5)一口气。
```

输出位置:
```
releases/{project_id}/audio/novel-tts.txt
```

### 步骤5: 生成配置文件

创建tts-config.json:

```json
{
  "project_id": "novel_20231113",
  "title": "异火苍穹",
  "chapters": 30,
  "total_words": 93500,
  "estimated_duration": "6小时30分钟",
  "tts_settings": {
    "voice": "zh-CN-XiaoxiaoNeural",
    "rate": "medium",
    "pitch": "medium",
    "volume": "medium"
  },
  "optimization": {
    "pause_comma": "0.3s",
    "pause_period": "0.6s",
    "pause_paragraph": "1.5s",
    "pause_chapter": "2.0s",
    "phoneme_enabled": true,
    "prosody_enabled": true
  },
  "output_files": {
    "ssml_dir": "releases/novel_20231113/audio/ssml/",
    "txt_file": "releases/novel_20231113/audio/novel-tts.txt",
    "metadata": "releases/novel_20231113/audio/tts-metadata.json"
  }
}
```

输出位置:
```
releases/{project_id}/audio/tts-config.json
```

---

## 输出目录结构

```
releases/{project_id}/audio/
├── novel-tts.txt              # 纯文本TTS版(简化)
├── tts-config.json            # TTS配置
├── ssml/                      # SSML文件(完整版)
│   ├── chapter-001-tts.xml
│   ├── chapter-002-tts.xml
│   └── ...
└── metadata.txt               # 元数据说明
```

---

## TTS引擎兼容性

### 支持的TTS平台

#### 1. Microsoft Azure TTS
- 格式: SSML (XML)
- 音色: zh-CN-XiaoxiaoNeural (女声), zh-CN-YunyangNeural (男声)
- 特性: 完全支持SSML标记

#### 2. 阿里云TTS
- 格式: SSML (XML)
- 音色: Aixia (艾夏), Aida (艾达)
- 特性: 支持基础SSML,不支持phoneme

#### 3. 讯飞TTS
- 格式: 纯文本 + 拼音标注
- 音色: xiaoyan, aisjiuxu
- 特性: 支持ssml部分标记

#### 4. 通用TTS
- 格式: 纯文本
- 仅保留基础停顿
- 多音字用括号标注: 长(zhang3)

---

## 使用示例

### 示例1: 导出完整SSML

```bash
用户: "优化所有章节为有声书格式"

处理流程:
1. 扫描productions/novel_xxx/chapters/
2. 逐章处理:
   - 移除格式标记
   - 添加停顿标记
   - 标注多音字
   - 添加语气标记
3. 生成SSML文件 (30个XML文件)
4. 生成简化TXT文件
5. 生成tts-config.json

输出:
✅ TTS优化完成!

文件位置: releases/novel_20231113/audio/
├── ssml/ (30个XML,完整SSML)
├── novel-tts.txt (简化版,9.5万字)
└── tts-config.json

推荐TTS引擎: Microsoft Azure TTS
预计朗读时长: 6小时30分钟
```

### 示例2: 仅导出简化版

```bash
用户: "导出TTS纯文本版本"

处理流程:
1. 扫描所有章节
2. 仅做基础处理:
   - 移除格式
   - 多音字拼音标注(括号)
   - 基础停顿
3. 生成novel-tts.txt

输出:
✅ TTS纯文本导出完成!

文件位置: releases/novel_20231113/audio/novel-tts.txt
(9.5万字,含拼音标注)

兼容: 所有TTS引擎
```

---

## 多音字字典

系统内置常用多音字字典:

```markdown
### 姓氏
- 萧: xiao1
- 纳兰: na4 lan2
- 尉迟: yu4 chi2
- 单于: chan2 yu2

### 高频多音字
- 了: liao3 (完成) / le5 (助词)
- 长: zhang3 (成长) / chang2 (长度)
- 还: hai2 (还是) / huan2 (归还)
- 重: zhong4 (重要) / chong2 (重复)
- 得: de2 (得到) / dei3 (必得) / de5 (跑得快)
- 着: zhao2 (着急) / zhuo2 (着落) / zhe5 (看着)
- 降: jiang4 (降低) / xiang2 (投降)
- 应: ying1 (应该) / ying4 (答应)
- 角: jiao3 (角色) / jue2 (角落)
- 乐: le4 (快乐) / yue4 (音乐)
- 行: xing2 (行走) / hang2 (银行)
- 数: shu4 (数量) / shu3 (数数) / shuo4 (屡见不鲜)
```

---

## 语气标注规则

```markdown
### 对话语气识别

1. 怒喝/怒吼/咆哮 → 愤怒语调
   <prosody rate="fast" pitch="high" volume="loud">

2. 轻声/低语/喃喃 → 轻柔语调
   <prosody rate="slow" pitch="low" volume="soft">

3. 冷笑/讥讽/嘲讽 → 冷漠语调
   <prosody rate="medium" pitch="low">

4. 惊呼/惊叫 → 惊讶语调
   <prosody rate="fast" pitch="high">

5. 叹息/叹气 → 无奈语调
   <prosody rate="slow">
```

---

## 预计朗读时长

```markdown
计算公式:
朗读速度: 300字/分钟 (中速)

示例:
30章 × 3,100字/章 = 93,000字
93,000字 ÷ 300字/分钟 = 310分钟 ≈ 5.2小时

加上:
- 停顿时间: 约10%
- 章节间隔: 30 × 2秒 = 1分钟

总时长: 5.2小时 × 1.1 + 1分钟 ≈ 5.8小时

实际生成时会在tts-config.json中给出精确预估。
```

---

## 注意事项

1. **SSML vs 纯文本**: Azure TTS用SSML,讯飞TTS用纯文本
2. **多音字覆盖**: 仅标注常见多音字,罕见词可能需要人工检查
3. **语气识别**: 基于关键词自动识别,可能不完全准确
4. **停顿时长**: 可在tts-config.json中调整
5. **音色选择**: 不同TTS引擎音色名称不同,需手动选择

---

## 高级功能

### 自定义多音字词典
用户可以添加:
```json
{
  "custom_phonemes": {
    "燕京": "yan1 jing1",
    "单田芳": "shan4 tian2 fang1"
  }
}
```

### 情感强度调节
```xml
<prosody volume="+50%">极度愤怒</prosody>
<prosody volume="+20%">一般愤怒</prosody>
```

### 背景音效标记
```xml
<audio src="sound/thunder.mp3"/>
<pause time="1.0s"/>
"轰隆一声巨响!"
```

---

激活条件: 用户说"优化为有声书"、"TTS格式"、"导出音频"等关键词,或Command "/export-all"包含TTS导出
