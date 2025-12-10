# Commands 使用指南

所有命令以 `nw-` 为前缀，便于识别和查找。在对话中通过 `/nw-xxx` 调用。

## 命令列表

| 命令 | 用途 | 示例 |
|------|------|------|
| `/nw-init` | 初始化工作区 | `/nw-init` |
| `/nw-scan` | 扫描分析素材池 | `/nw-scan xuanhuan_1` |
| `/nw-bp-plan` | 生成蓝图（策划阶段） | `/nw-bp-plan 玄幻 废柴流` |
| `/nw-bp-audit` | 审核蓝图质量 | `/nw-bp-audit` |
| `/nw-ch-write` | 批量创作章节（创作阶段） | `/nw-ch-write 1-10` |
| `/nw-ch-audit` | 审核章节质量 | `/nw-ch-audit 1-10` |
| `/nw-release` | 发布导出 | `/nw-release tts` |

## 命令体系

```
准备阶段
  └─ /nw-init          初始化工作区

素材阶段（可选）
  └─ /nw-scan          扫描分析素材池

策划阶段 (bp = blueprint)
  ├─ /nw-bp-plan       生成蓝图
  └─ /nw-bp-audit      审核蓝图

创作阶段 (ch = chapter)
  ├─ /nw-ch-write      批量创作
  └─ /nw-ch-audit      审核章节

发布阶段
  └─ /nw-release       发布导出
```

## 典型工作流

```bash
# 1. 初始化工作区
/nw-init

# 2. 分析素材（可选）
/nw-scan xuanhuan_1

# 3. 生成蓝图
/nw-bp-plan xuanhuan_1 玄幻 废柴流

# 4. 审核蓝图
/nw-bp-audit

# 5. 创作章节
/nw-ch-write 1-10

# 6. 审核章节
/nw-ch-audit 1-10

# 7. 发布导出
/nw-release all
```

## 阶段上下文

执行 `/nw-bp-plan` 或 `/nw-ch-write` 后会进入对应阶段：
- **蓝图阶段**：后续对话可直接讨论蓝图修改
- **章节阶段**：后续对话可直接讨论章节修改

无需重复输入命令，AI 会根据上下文理解意图。

## 命名规范

- `nw-` = novel-writer 前缀
- `bp-` = blueprint（蓝图/策划）
- `ch-` = chapter（章节/创作）
- 范围参数格式：`1-10`（连续）或 `1,4,7`（离散）

详细使用方法见各命令的 md 文件。
