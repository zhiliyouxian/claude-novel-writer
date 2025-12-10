# Commands 使用指南

所有命令以 `nw-` 为前缀，便于识别和查找。在对话中通过 `/nw-xxx` 调用。

## 命令列表

| 命令 | 用途 | 示例 |
|------|------|------|
| `/nw-init` | 初始化工作区 | `/nw-init` |
| `/nw-write` | 批量创作章节 | `/nw-write 1-10` |
| `/nw-review` | 审核章节质量 | `/nw-review 1-10` |
| `/nw-export` | 导出章节 | `/nw-export --format txt` |
| `/nw-check` | 检查编码乱码 | `/nw-check 1-10` |

## 典型工作流

```bash
# 1. 初始化工作区
/nw-init

# 2. 创作章节
/nw-write 1-10

# 3. 审核质量
/nw-review 1-10

# 4. 修正问题后导出
/nw-export
```

## 命名规范

- `nw-` = novel-writer 前缀
- 命令名尽量简短，参数在命令后指定
- 范围参数格式：`1-10`（连续）或 `1,4,7`（离散）

详细使用方法见各命令的 md 文件。
