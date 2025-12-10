---
name: nw-ch-write
description: 批量创作章节（创作阶段）。用法: /nw-ch-write 1-10
---

# 批量章节创作命令

快捷批量创作多个章节的命令。

执行此命令后进入**章节阶段**，后续对话可直接讨论章节修改，无需重复输入命令。

## 用法

```bash
/nw-ch-write <起始章节>-<结束章节>
```

## 示例

```bash
# 创作第1-10章
/nw-ch-write 1-10

# 创作第11-20章
/nw-ch-write 11-20

# 创作第47-56章
/nw-ch-write 47-56
```

## 功能

此命令会:

1. **解析范围**: 提取起始和结束章节号
2. **调用Agent**: 循环调用 `chapter-writer` Agent
3. **逐章创作**: 从起始章节到结束章节,逐个创作
4. **自动管理**: 每章创作完自动更新 `entities.md`
5. **进度追踪**: 完成后更新 `progress.md`

## 执行流程

```
用户输入: /nw-ch-write 1-10
  ↓
确定 project_id:
  ├─ 检查 blueprints/ 下有几个项目
  ├─ 如果只有一个 → 自动使用
  ├─ 如果有多个 → 询问用户选择哪个项目
  └─ 如果没有蓝图 → 提示先创建蓝图
  ↓
解析: 起始=1, 结束=10, 共10章
  ↓
确保目录存在: mkdir -p productions/{project_id}/chapters productions/{project_id}/data
  ↓
For each 章节 from 1 to 10:
  ├─ 调用 chapter-writer Agent
  ├─ 传入: 章节号, outline.md, entities.md
  ├─ 等待创作完成
  ├─ 保存 productions/{project_id}/chapters/chapter-{N}.md
  ├─ 更新 productions/{project_id}/data/entities.md
  └─ 显示进度: "已完成 {N}/10 章"
  ↓
全部完成后:
  ├─ 更新 productions/{project_id}/data/progress.md
  └─ 提示用户: "10章创作完成,建议运行 /nw-ch-audit 1-10 进行审核"
```

## 参数验证

- **范围检查**: 起始 < 结束
- **重复检查**: 如果章节文件已存在,询问是否覆盖
- **大纲检查**: 确保 `outline.md` 包含对应章节

## 错误处理

### 错误1: 大纲缺失
```
错误: blueprints/{project_id}/outline.md 不存在
建议: 请先使用 /create-blueprint 或 outline-architect Agent 创建大纲
```

### 错误2: 范围超出大纲
```
错误: 大纲只有200章,但请求创作201-210章
建议: 请调整范围或扩展大纲
```

### 错误3: 章节已存在
```
警告: chapter-001.md 已存在
选项: [覆盖] [跳过] [取消]
```

## 最佳实践

### 建议1: 每次10章
```bash
# 推荐: 每批10章,便于审核和修改
/nw-ch-write 1-10
/nw-ch-write 11-20
/nw-ch-write 21-30
```

### 建议2: 创作后及时审核
```bash
/nw-ch-write 1-10
/nw-ch-audit 1-10    # 立即审核
# 根据审核意见修改后,再写下一批
```

### 建议3: 检查一致性
```bash
/nw-ch-write 1-10
# 系统会自动运行 consistency-checker Skill
# 检查实体一致性
```

## 输出示例

```
开始批量创作: 第1-10章
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/10] 创作 第1章 废柴少年...
  ✓ 完成 (2847字)
  ✓ 更新实体库: +3个人物, +2个地点

[2/10] 创作 第2章 玉佩之秘...
  ✓ 完成 (2901字)
  ✓ 更新实体库: +1个物品

[3/10] 创作 第3章 签到系统...
  ✓ 完成 (2876字)
  ✓ 更新实体库: 境界更新(炼气3层→炼气5层)

...

[10/10] 创作 第10章 外门大比...
  ✓ 完成 (2955字)
  ✓ 更新实体库: +4个人物

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 批量创作完成!

统计信息:
- 创作章节: 10章
- 总字数: 28,734字
- 新增实体: 15个人物, 8个地点, 3个物品
- 境界更新: 炼气3层 → 炼气9层

文件位置:
- 章节文件: productions/{project_id}/chapters/chapter-001.md ~ chapter-010.md
- 实体库: productions/{project_id}/data/entities.md (已更新)
- 进度记录: productions/{project_id}/data/progress.md (已更新)

下一步建议:
1. 运行 /nw-ch-audit 1-10 进行审核
2. 查看 productions/{project_id}/data/entities.md 检查实体一致性
3. 审核通过后,继续创作下一批: /nw-ch-write 11-20
```

## 中断与恢复

### 中断处理
如果创作过程中断(如网络问题):
```
警告: 创作在第5章时中断

已完成:
- chapter-001.md ~ chapter-004.md ✓

未完成:
- chapter-005.md ~ chapter-010.md ✗

恢复建议:
/nw-ch-write 5-10
```

### 断点续写
系统会自动检测已存在的章节,只创作缺失的部分。

## 性能优化

### 并行创作 (未来功能)
```bash
# 当前: 串行创作(逐章)
# 未来: 可选并行模式
/nw-ch-write 1-10 --parallel
# 同时创作多章,速度更快
```

## 相关命令

- `/nw-ch-audit 1-10` - 批量审核创作的章节
- `/nw-release` - 导出发布

---

**提示**: 执行此命令后进入章节阶段，可直接通过对话修改章节内容，无需重复输入命令。
