---
name: check-encoding
description: 检查章节文件的编码问题和乱码。用法: /check-encoding 或 /check-encoding 1-10
---

# 编码检查命令

检测章节文件中的乱码和特殊字符问题（如 `���`）。

## 用法

```bash
/check-encoding              # 检查所有章节
/check-encoding 1-10         # 检查指定范围
/check-encoding 5            # 检查单个章节
```

## 执行流程

收到此命令后，执行以下步骤：

### 步骤1: 确定检查范围

```markdown
如果无参数: 检查 productions/{project_id}/chapters/ 下所有章节
如果有范围参数(如 1-10): 只检查 chapter-001.md 到 chapter-010.md
如果有单个参数(如 5): 只检查 chapter-005.md
```

### 步骤2: 确定 project_id

```markdown
1. 检查 productions/ 目录下有多少项目
2. 如果只有一个项目，自动使用
3. 如果有多个项目，询问用户使用哪个
```

### 步骤3: 运行检测脚本

```bash
python scripts/check-encoding.py productions/{project_id}/chapters/
```

### 步骤4: 输出结果

根据检测结果输出报告。

## 输出示例

### 全部正常

```
【编码检查】
检测范围: productions/my_novel/chapters/

检测 30 个文件... ✅ 全部正常

============================================================
检测完成: 30 个文件
  ✅ 正常: 30
  ❌ 问题: 0
```

### 发现问题

```
【编码检查】
检测范围: productions/my_novel/chapters/

❌ chapter-003.md (5 个错误)
   第15行: ...不像��渎那样锋利...
   第187行: 我深吸一口���，正要开口——

❌ chapter-007.md (2 个错误)
   第59行: ...但���住，不要暴露...

============================================================
检测完成: 30 个文件
  ✅ 正常: 28
  ❌ 问题: 2
  📍 总错误数: 7

建议:
1. 根据上下文推断正确字符（如 "一口���" → "一口气"）
2. 手动修复或使用 revision-writer 修改
3. 修复后重新运行: /check-encoding
```

## 检测内容

脚本检测以下问题：
- Unicode 替换字符 `�` (U+FFFD)
- 常见乱码模式
- 不可打印的控制字符

## 修复建议

发现乱码后：
1. 根据上下文推断正确字符
2. 手动编辑修复，或使用 revision-writer
3. 修复后重新运行检测确认

## 与其他命令配合

```bash
# 先检查编码
/check-encoding 1-10

# 确认无乱码后审核
/review-batch 1-10

# 或者直接审核（会自动先检查编码）
/review-batch 1-10
```

## 相关命令

- `/review-batch` - 批量审核（包含编码检查）
- `/revise-chapters` - 修改章节

---

**提示**: 乱码通常由复制粘贴或编码不一致导致，建议使用 UTF-8 编码保存所有文件。
