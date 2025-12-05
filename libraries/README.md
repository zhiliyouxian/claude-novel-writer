# Knowledge Library

本目录包含 **Agent 生成内容时的参考知识**，不是直接给用户的模板。

---

## Directory Structure

```
libraries/
└── knowledge/
    ├── _base/                    # 通用知识（始终加载）
    │   ├── story-structures.md   # 故事结构模式
    │   └── character-archetypes.md # 角色原型
    │
    ├── chinese-webnovel/         # 中文网文知识包
    │   ├── xuanhuan-patterns.md  # 玄幻套路
    │   ├── power-systems.md      # 境界体系
    │   └── goldfinger-types.md   # 金手指类型
    │
    └── {your-pack}/              # 自定义知识包
        └── *.md                  # 知识文件
```

---

## Knowledge Pack System

### How It Works

1. **`_base/` is mandatory** - Always loaded for every project
   - Contains universal writing knowledge
   - Story structures (Three-Act, Hero's Journey, 起承转合)
   - Character archetypes and relationship patterns

2. **Other packs are auto-discovered** - Based on user keywords
   - Agent scans `libraries/knowledge/*/` for available packs
   - Matches directory names against user requirements
   - Loads relevant `.md` files from matched directories

### Keyword Matching Examples

| User Says | Matched Pack | Files Loaded |
|-----------|--------------|--------------|
| "玄幻小说" / "网文" / "修仙" | `chinese-webnovel/` | xuanhuan-patterns.md, power-systems.md |
| "异世界" / "轻小说" / "转生" | `japanese-lightnovel/` | isekai-patterns.md |
| "fantasy" / "epic" / "magic" | `western-fantasy/` | magic-systems.md |

### No Match Behavior

If user requirements don't match any knowledge pack, Agents use only `_base/` knowledge and rely on their general capabilities.

---

## Adding a New Knowledge Pack

### Step 1: Create Directory

```bash
mkdir libraries/knowledge/your-pack-name/
```

Use descriptive names that match potential user keywords:
- `japanese-lightnovel/` - 日本轻小说
- `western-fantasy/` - Western fantasy
- `romance/` - 言情/爱情
- `mystery-thriller/` - 悬疑推理

### Step 2: Add Knowledge Files

Create `.md` files with relevant knowledge:

```
your-pack-name/
├── patterns.md       # Genre-specific tropes and patterns
├── power-systems.md  # Power/magic system templates
├── character-types.md # Common character archetypes
└── plot-structures.md # Typical plot structures
```

### Step 3: File Content Guidelines

Each knowledge file should include:

1. **Overview** - What this file covers
2. **Categories** - Organized knowledge sections
3. **Examples** - Concrete examples for each pattern
4. **Variations** - Common modifications

Example structure:

```markdown
# [Topic Name]

本文档包含 [topic] 相关的参考知识。

---

## Category 1

### Pattern 1.1
- **Description**: ...
- **Example**: ...
- **Usage**: ...

### Pattern 1.2
...

---

## Category 2
...
```

---

## Agent Usage

### For Agent Developers

When building Agents that use knowledge packs:

```markdown
### Knowledge Discovery Flow

1. **Always load base knowledge**:
   Read {plugin_dir}/libraries/knowledge/_base/*.md

2. **Discover available packs**:
   Glob {plugin_dir}/libraries/knowledge/*/

3. **Match user keywords to directory names**:
   - User says "玄幻" → match "chinese-webnovel"
   - User says "isekai" → match "japanese-lightnovel"

4. **Load matched pack files**:
   Read {plugin_dir}/libraries/knowledge/{matched-pack}/*.md
```

### Knowledge Priority

1. **Project-specific settings** (from user's `blueprints/`) - Highest
2. **Knowledge pack content** (from matched pack) - Medium
3. **Base knowledge** (from `_base/`) - Lowest (always available)

---

## Reference Novels

### Correct Workflow

Reference novels should be placed in **user's workspace**, not in plugin directory:

```
{user-workspace}/
└── pools/
    ├── reference_1/           # User places reference novels here
    │   ├── novel1.txt
    │   └── novel2.txt
    └── analysis/              # Auto-generated analysis reports
        └── reference_1/
            ├── style-fusion.md
            └── pattern-extract.md
```

### Usage Steps

```bash
# 1. Initialize workspace
cd ~/my-project
claude "/workspace-init"

# 2. Create pool and add references
mkdir pools/reference_1
cp ~/Downloads/novel.txt pools/reference_1/

# 3. Analyze pool
claude "/analyze-pool reference_1"

# 4. Use analysis in blueprint
claude "/create-blueprint reference_1 玄幻 废柴流"
```

---

## Important Notes

1. **Copyright**: Don't store copyrighted novel content in plugin directory
2. **Privacy**: Project materials go in user workspace, not plugin directory
3. **Space**: After analysis, original files can be deleted
4. **Paths**: Skills can read any path in user workspace

---

## Summary

| Directory | Content | Loaded When |
|-----------|---------|-------------|
| `_base/` | Universal writing knowledge | Always |
| `chinese-webnovel/` | 中文网文套路、境界、金手指 | User mentions relevant keywords |
| `japanese-lightnovel/` | 异世界、转生、轻小说套路 | User mentions relevant keywords |
| `{custom}/` | Your custom knowledge | User mentions relevant keywords |

---

## Contributing

To contribute a new knowledge pack:

1. Fork the repository
2. Create your knowledge pack directory
3. Add comprehensive `.md` files
4. Submit a pull request

See [README.md](../README.md) for contribution guidelines.
