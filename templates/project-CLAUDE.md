# CLAUDE.md

本文件为当前小说创作项目的工作指南。

---

## 项目信息

- **项目ID**: {project_id}
- **创建时间**: {created_date}
- **工作区位置**: {workspace_path}

---

## project_id 命名规范

每个小说项目必须有唯一的 project_id，用于区分不同作品的文件路径。

| 规则 | 说明 | 示例 |
|------|------|------|
| 格式 | 小写字母、数字、下划线 | `my_novel_01` |
| 长度 | 3-30 字符 | ✅ `dao` ❌ `a` |
| 语义 | 有意义的简短名称 | `urban_rebirth` |
| 禁止 | 中文、空格、特殊字符 | ❌ `我的小说` |

**确定 project_id 的规则**：
1. 如果你明确指定项目名（如"创作《纵横天下》"），使用拼音或英文：`zongheng`
2. 如果工作区只有一个蓝图，自动使用该蓝图的目录名
3. 如果工作区有多个蓝图，需要指定使用哪个
4. 如果没有指定且没有蓝图，使用默认名 `novel_001`

---

## 目录结构

```
{workspace_path}/
├── pools/                      # 素材池（放入参考小说）
│   ├── {pool_name}/           # 素材目录
│   └── analysis/              # 分析报告
│
├── blueprints/                 # 蓝图（企划书）
│   └── {project_id}/          # 本项目蓝图
│       ├── proposal.md        # 选题方案
│       ├── worldview.md       # 世界观
│       ├── characters.md      # 角色档案
│       └── outline.md         # 章节大纲
│
├── productions/                # 制作中的章节
│   └── {project_id}/          # 本项目制作目录
│       ├── blueprint.link     # 链接到蓝图
│       ├── chapters/          # 章节文件（重要！）
│       │   ├── chapter-001.md
│       │   └── ...
│       └── data/
│           └── entities.md    # 实体库
│
└── releases/                   # 导出成品
    └── {project_id}/
        ├── reviews/           # 审核报告
        ├── text/              # TXT版
        └── audio/             # TTS版
```

---

## 常用命令

| 命令 | 功能 |
|------|------|
| `/write-chapters 1-10` | 批量创作第1-10章 |
| `/write-chapters 11-20` | 继续创作第11-20章 |
| `/review-batch 1-10` | 批量审核章节 |
| `/export-all` | 导出所有格式 |

---

## 注意事项

1. **章节位置**：所有章节文件必须在 `productions/{project_id}/chapters/` 目录下
2. **实体库**：位于 `productions/{project_id}/data/entities.md`，创作时自动维护
3. **书写规范**：遵守 `WRITING_STYLE_GUIDE.md` 中的格式要求
4. **命名格式**：章节文件命名为 `chapter-{001}.md`（三位数字补零）

---

## 四部门工作流

```
素材池(Pools) → 策划(Blueprints) → 制作(Productions) → 发布(Releases)
```

1. **素材池**：放入参考小说，执行分析
2. **策划**：生成世界观、角色、大纲等蓝图文件
3. **制作**：根据蓝图批量创作章节
4. **发布**：审核、修订、导出成品

---

*由 Novel Writing Studio Plugin 的 `/workspace-init` 命令生成*
