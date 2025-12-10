# Commands 使用指南

所有命令以 `nw-` 为前缀，便于识别和查找。在对话中通过 `/nw-xxx` 调用。

## 命令列表

| 命令 | 用途 | 示例 |
|------|------|------|
| `/nw-init` | 初始化工作区 | `/nw-init` |
| `/nw-analyze` | 分析素材池（可选） | `/nw-analyze xuanhuan_1` |
| `/nw-plan` | 生成蓝图 | `/nw-plan 玄幻 废柴流` |
| `/nw-write` | 批量创作章节 | `/nw-write 1-10` |
| `/nw-review` | 审核章节质量 | `/nw-review 1-10` |
| `/nw-export` | 导出章节 | `/nw-export --format txt` |

## 典型工作流

```bash
# 1. 初始化工作区
/nw-init

# 2. 分析素材（可选）
/nw-analyze xuanhuan_1

# 3. 生成蓝图
/nw-plan xuanhuan_1 玄幻 废柴流

# 4. 创作章节
/nw-write 1-10

# 5. 审核质量
/nw-review 1-10

# 6. 导出
/nw-export
```

## 命名规范

- `nw-` = novel-writer 前缀
- 命令名尽量简短，参数在命令后指定
- 范围参数格式：`1-10`（连续）或 `1,4,7`（离散）

详细使用方法见各命令的 md 文件。
