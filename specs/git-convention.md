# Git 版本管理规范

本文件定义小说创作项目的 Git 版本管理策略。Git 管理是**可选增强**功能，有助于变更追踪和回退。

---

## 基本原则

1. **可选使用**：没有 git 环境也能正常工作
2. **自动提交**：Agent 完成操作后自动提交
3. **语义化消息**：使用规范的提交消息格式
4. **不强制推送**：只在本地提交，用户决定是否推送

---

## 检测 Git 环境

每个 Agent/Skill 在执行变更前检测：

```bash
# 检测是否有 git
if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null; then
    # 有 git 环境，执行完操作后提交
else
    # 无 git 环境，跳过提交步骤
fi
```

---

## 提交时机

| 操作 | 提交时机 | 提交消息示例 |
|------|----------|--------------|
| `/nw-init` | 初始化完成后 | `feat: 初始化工作区` |
| `/nw-bp-plan` | 蓝图生成完成后 | `feat: 生成蓝图 {project_id}` |
| 蓝图修改 | 每次修改后 | `fix: 调整 {project_id} 世界观设定` |
| `/nw-ch-write` | 每批章节完成后 | `feat: 创作 {project_id} 第1-10章` |
| 章节修订 | 修订完成后 | `fix: 修订 {project_id} 第3章` |
| `/nw-release` | 导出完成后 | `release: 导出 {project_id} tts格式` |

---

## 提交消息格式

```
<type>: <description>

[optional body]
```

### Type 类型

| type | 用途 |
|------|------|
| `feat` | 新增内容（新章节、新蓝图） |
| `fix` | 修改/修订（修改章节、调整设定） |
| `docs` | 文档更新（审核报告） |
| `release` | 发布导出 |

### 示例

```bash
# 蓝图相关
feat: 生成蓝图 xuanhuan_001
fix: 调整 xuanhuan_001 角色设定
fix: 修正 xuanhuan_001 大纲第50-60章

# 章节相关
feat: 创作 xuanhuan_001 第1-10章
feat: 创作 xuanhuan_001 第11-20章
fix: 修订 xuanhuan_001 第3章爽点密度

# 审核相关
docs: 蓝图审核报告 xuanhuan_001
docs: 章节审核报告 xuanhuan_001 第1-10章

# 发布相关
release: 导出 xuanhuan_001 tts格式
release: 导出 xuanhuan_001 全部格式
```

---

## 版本标签

在重要节点打标签：

| 时机 | 标签格式 | 示例 |
|------|----------|------|
| 蓝图完成 | `{project_id}-blueprint` | `xuanhuan_001-blueprint` |
| 里程碑 | `{project_id}-ch{N}` | `xuanhuan_001-ch100` |
| 完结 | `{project_id}-complete` | `xuanhuan_001-complete` |
| 正式发布 | `{project_id}-v{version}` | `xuanhuan_001-v1.0` |

---

## Agent 实现指南

在 Agent 的执行流程末尾添加：

```markdown
## Git 版本管理（可选）

完成本次操作后：

1. 检测环境是否有 git
   - 有 git → 继续步骤 2
   - 无 git → 跳过，不影响流程

2. 检查是否有变更
   ```bash
   git status --porcelain
   ```

3. 如果有变更，执行提交
   ```bash
   git add <相关文件>
   git commit -m "<type>: <description>"
   ```

4. 不自动推送（让用户决定）
```

---

## 好处

1. **随时回退**：蓝图改坏了可以恢复
2. **变更追踪**：看到每次修改了什么
3. **版本对比**：对比修订前后差异
4. **协作支持**：多人协作时避免冲突
5. **非阻断性**：没有 git 也能正常工作

---

## 注意事项

1. 不要提交敏感信息（API key 等）
2. 不要提交过大的素材文件（建议 .gitignore）
3. 提交消息使用中文，方便追溯
4. 批量操作一次提交，避免过多小提交

---

## 推荐 .gitignore

```gitignore
# 素材池（文件可能很大）
pools/*/*.txt

# 临时文件
*.tmp
*.bak

# 系统文件
.DS_Store
Thumbs.db
```
