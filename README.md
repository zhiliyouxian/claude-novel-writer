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
claude "/nw-analyze reference_1"
```

### 3. Generate Blueprint

```bash
claude "/nw-plan reference_1 玄幻 废柴流"
# Or for other genres:
claude "/nw-plan reference_1 fantasy hero's-journey"
```

Auto-generates:
1. 3 topic proposals
2. Complete worldview (power systems, factions, geography)
3. Character profiles (20+ characters)
4. 200+ chapter outline

### 4. Start Production

```bash
claude "/nw-write 1-10"
claude "/nw-write 11-20"
```

### 5. Review & Export

```bash
claude "/nw-review 1-10"
claude "/nw-export"
```

---

## Architecture

```
Pools (素材池) → Blueprints (策划) → Productions (制作) → Releases (发布)
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
        └── audio/             # TTS optimized
```

### project_id Naming Convention

Each novel project requires a unique `project_id` for directory naming:

| Rule | Description | Example |
|------|-------------|---------|
| Format | lowercase letters, numbers, underscores | `my_novel_01` |
| Length | 3-30 characters | ✅ `dao` ❌ `a` |
| Meaning | Short descriptive name | `urban_rebirth` |
| Forbidden | Chinese, spaces, special chars | ❌ `我的小说` |

---

## Commands

| Command | Description |
|---------|-------------|
| `/nw-init` | Initialize workspace structure |
| `/nw-analyze {name}` | Analyze reference materials |
| `/nw-plan` | Generate complete blueprint |
| `/nw-write 1-10` | Batch create chapters |
| `/nw-review 1-10` | Batch review chapters |
| `/nw-export` | Export all formats |

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
| chapter-writer | Write chapters |
| entity-manager | Manage entities |
| chapter-auditor | Review chapters |
| revision-writer | Revise chapters |

### Skills (5)
| Skill | Function |
|-------|----------|
| pool-analyzer | Analyze reference materials |
| blueprint-validator | Validate blueprint |
| consistency-checker | Check cross-chapter consistency |
| format-exporter | Export to various formats |
| audiobook-optimizer | Optimize for TTS |

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
- `CLAUDE.md` - Claude working instructions
