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

---

*由 /nw-init 生成 | Novel Writing Studio v{version}*
