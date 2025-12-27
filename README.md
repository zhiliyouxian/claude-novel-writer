# Novel Writing Studio Plugin

> A comprehensive novel creation framework with extensible knowledge packs

从素材分析到小说发布的全自动化创作流程，支持多种小说类型。

---

## Features

### Core Framework
- **Four-Department Architecture**: Pools → Blueprints → Productions → Releases
- **8 Specialized Agents**: Worldview, Character, Outline, Chapter writing, etc.
- **5 Automated Skills**: Analysis, Validation, Consistency check, Export
- **4 Batch Commands**: Initialize, Write, Review, Export

### Extensible Knowledge Packs
- `_base/` - Universal story structures, character archetypes (always loaded)
- `chinese-webnovel/` - 中文网文知识 (玄幻、修仙、系统流等)
- `japanese-lightnovel/` - 日本轻小说 (异世界、转生等) [planned]
- `western-fantasy/` - Western fantasy (epic, magic systems) [planned]

**Add your own**: Simply create a new directory under `libraries/knowledge/`

---

## Quick Start

### 1. Initialize Workspace

```bash
claude "/nw-init"
```

Creates the standard four-department directory structure in current directory.

### 2. Prepare Reference Materials (Optional)

```bash
mkdir pools/reference_1
# Add reference novels: novel1.txt, novel2.txt...
claude "/nw-scan reference_1"
```

### 3. Generate Blueprint

```bash
claude "/nw-bp-plan reference_1 玄幻 废柴流"
# Or for other genres:
claude "/nw-bp-plan reference_1 fantasy hero's-journey"
```

Auto-generates:
1. 3 topic proposals
2. Complete worldview (power systems, factions, geography)
3. Character profiles (20+ characters)
4. 200+ chapter outline

### 4. Audit Blueprint

```bash
claude "/nw-bp-audit"
```

### 5. Start Production

```bash
claude "/nw-ch-write 1-10"
claude "/nw-ch-write 11-20"
```

### 6. Review & Release

```bash
claude "/nw-ch-audit 1-10"
claude "/nw-release all"
```

---

## Architecture

```
Pools (素材池) → Blueprints (策划) → Productions (制作) → Releases (发布)
```

### Department Collaboration

```
┌─────────────────────────────────────────────────────────────────┐
│                     策划团队 (Blueprints)                        │
├─────────────────────────────────────────────────────────────────┤
│ worldview-architect → character-designer → outline-architect   │
│                              ↓                                  │
│                    blueprint-auditor (质量门槛)                  │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                     创作团队 (Productions)                       │
├─────────────────────────────────────────────────────────────────┤
│ production-initializer                                          │
│         ↓                                                       │
│ chapter-writer (创作) ←──────────────┐                          │
│         ↓                            │                          │
│ chapter-auditor (审核)               │                          │
│         ↓                            │                          │
│     (修订模式) ─────────────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                     发布团队 (Releases)                          │
├─────────────────────────────────────────────────────────────────┤
│ release-manager → format-exporter / audiobook-optimizer         │
│                 → video-director → video-assembler              │
└─────────────────────────────────────────────────────────────────┘
```

### Workspace Structure

```
{your-directory}/
├── CLAUDE.md                   # Project guide (auto-generated)
├── pools/                      # Reference materials
│   ├── {pool_name}/           # Put reference novels here
│   └── analysis/              # Auto-generated analysis
│
├── blueprints/                 # Planning department
│   └── {project_id}/          # Blueprint (project plan)
│       ├── proposal.md        # Topic proposals
│       ├── worldview.md       # World settings
│       ├── characters.md      # Character profiles
│       └── outline.md         # Chapter outline
│
├── productions/                # Production department
│   └── {project_id}/          # Production project
│       ├── blueprint.link     # Link to blueprint
│       ├── chapters/          # Chapter files
│       └── data/
│           └── entities.md    # Entity database
│
└── releases/                   # Publishing department
    └── {project_id}/
        ├── reviews/           # Review reports
        ├── text/              # TXT format
        ├── markdown/          # Markdown format
        └── tts/               # TTS audio
            ├── scripts/       # TTS text
            └── audio/         # MP3 files
```

### Chapter Status Flow

章节从初稿到可发布的状态流转：

```
                    ┌─────────────────────┐
                    ▼                     │
draft ──审核──> final                     │
          │                               │
          └──> pending ──修订──> revised ──复审──> final
                  ▲                   │
                  └───────────────────┘
                    (复审仍有问题)
```

| 状态 | 含义 | 设置者 |
|------|------|--------|
| `draft` | 初稿完成，等待首次审核 | chapter-writer |
| `pending` | 审核发现问题，等待修订 | chapter-auditor |
| `revised` | 修订完成，等待复审 | chapter-writer (修订模式) |
| `final` | 审核通过，可发布 | chapter-auditor |

---

### project_id Naming Convention

> Details: `specs/project-naming.md`

**Auto-generated format**: `{genre_prefix}_{sequence}`

| Genre | Prefix | Example |
|-------|--------|---------|
| 玄幻 | `xuanhuan` | `xuanhuan_001` |
| 仙侠 | `xianxia` | `xianxia_001` |
| 都市 | `dushi` | `dushi_001` |
| 科幻 | `kehuang` | `kehuang_001` |
| 历史 | `lishi` | `lishi_001` |
| 游戏 | `youxi` | `youxi_001` |
| 奇幻 | `qihuan` | `qihuan_001` |
| 悬疑 | `xuanyi` | `xuanyi_001` |
| 轻小说 | `qingxiaoshuo` | `qingxiaoshuo_001` |

**Rules**:
- Auto-generated based on main genre + sequence number
- Multi-genre: use main genre (e.g., "都市修仙" → `dushi_XXX`)
- Manual override: `/nw-bp-plan 玄幻 废柴流 --id custom_name`

**Book Title**:
- Not stored in blueprint files
- Input when running `/nw-release`
- Each release can use a different title

---

## Commands

| Command | Description |
|---------|-------------|
| `/nw-init` | Initialize workspace structure |
| `/nw-scan {name}` | Scan and analyze reference materials |
| `/nw-bp-plan` | Generate complete blueprint |
| `/nw-bp-audit` | Audit blueprint quality |
| `/nw-ch-write 1-10` | Batch create chapters |
| `/nw-ch-audit 1-10` | Batch audit chapters |
| `/nw-release` | Export and release |

---

## Knowledge Pack System

### How It Works

1. **Base knowledge** (`_base/`) is always loaded
   - `story-structures.md` - Three-act, Hero's Journey, 起承转合
   - `character-archetypes.md` - Universal character patterns

2. **Genre-specific packs** are auto-discovered based on user keywords
   - "玄幻/网文/修仙" → loads `chinese-webnovel/`
   - "isekai/light novel" → loads `japanese-lightnovel/`

3. **Adding new packs**: Create directory + add .md files
   ```
   libraries/knowledge/
   ├── _base/                 # Always loaded
   ├── chinese-webnovel/      # Loaded when relevant
   ├── your-new-pack/         # Auto-discovered
   │   ├── patterns.md
   │   └── tropes.md
   ```

---

## Components

### Agents (8)
| Agent | Function |
|-------|----------|
| worldview-architect | Build world settings |
| character-designer | Design characters |
| outline-architect | Create chapter outline |
| production-initializer | Initialize production |
| chapter-writer | Write chapters (with revision mode) |
| chapter-auditor | Review chapters |
| release-manager | Export and publish (TTS, audio, txt, video) |
| video-director | Generate video scripts and storyboards |

### Skills (9)
| Skill | Function |
|-------|----------|
| pool-analyzer | Analyze reference materials |
| blueprint-auditor | Audit blueprint quality |
| blueprint-sync-checker | Check blueprint changes impact |
| consistency-checker | Check cross-chapter consistency |
| encoding-checker | Check encoding issues |
| format-exporter | Export to various formats |
| audiobook-optimizer | TTS text and audio generation |
| character-visual-prompter | Generate character image prompts |
| video-assembler | Assemble video clips with effects |

---

## Design Principles

1. **Knowledge-Driven**: Plugin provides reference knowledge, not project data
2. **Auto-Generated**: All settings generated by Agents, not copied templates
3. **Directory Convention**: Fixed structure for indexing, no JSON config needed
4. **Markdown First**: Entity database uses tables, not JSON (LLM-friendly)
5. **Creation Priority**: Blueprint defines framework, writing fills details

---

## Supported Genres

**Currently Included:**
- Chinese Web Novels (玄幻、仙侠、都市、科幻)

**Planned / Contribute:**
- Japanese Light Novels
- Western Fantasy
- Romance
- Mystery/Thriller

---

## Contributing

To add a new knowledge pack:
1. Create directory under `libraries/knowledge/`
2. Add relevant `.md` files (patterns, tropes, power systems, etc.)
3. Follow naming convention: descriptive filenames in English or target language
4. Submit PR to [claude-novel-writer](https://github.com/zhiliyouxian/claude-novel-writer)

---

## License

MIT License - see [LICENSE](LICENSE)

---

## References

- `specs/writing-style.md` - Writing style rules
- `specs/directory-structure.md` - Directory structure specification
- `specs/project-naming.md` - Project naming convention
- `specs/project-detection.md` - Project detection logic
- `specs/git-convention.md` - Git version management
