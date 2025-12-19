# 小说创作工作区

本工作区使用 **Novel Writing Studio** 插件进行小说创作。

## 工作流

```
素材池(pools/) → 策划(blueprints/) → 制作(productions/) → 发布(releases/)
```

## 快速开始

| 操作 | 命令/说法 |
|------|----------|
| 分析素材 | `/nw-scan {pool_name}` |
| 生成蓝图 | `/nw-bp-plan {类型} {流派}` 或 "帮我策划一个玄幻小说" |
| 创作章节 | `/nw-ch-write 1-10` 或 "写第1章" |
| 导出发布 | `/nw-release` 或 "生成有声书" |

## 目录说明

- `pools/` - 放入参考小说，用于分析学习
- `blueprints/{project_id}/` - 蓝图（世界观、角色、大纲）
- `productions/{project_id}/chapters/` - 章节文件
- `releases/{project_id}/` - 导出成品（TXT、有声书等）

## 蓝图文件索引

> Agent 查询入口：按需求类型定位文件

| 查询需求 | 文件路径 |
|----------|----------|
| 选题/金手指/规模 | blueprints/{project_id}/proposal.md |
| 世界观总览 | blueprints/{project_id}/worldview.md |
| 力量体系/势力/地理 | blueprints/{project_id}/worldview/*.md |
| 角色总览/索引 | blueprints/{project_id}/characters.md |
| 角色详情 | blueprints/{project_id}/characters/{角色名}.md |
| 总纲/戏剧结构 | blueprints/{project_id}/outline.md |
| 卷详细大纲 | blueprints/{project_id}/outlines/vol-{N}.md |
| 实体当前状态 | productions/{project_id}/entities.md |

---

*由 /nw-init 生成 | Novel Writing Studio v{version}*
