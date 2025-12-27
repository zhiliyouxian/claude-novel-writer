# 项目命名规范

本文档定义 `project_id` 的命名规则，确保项目目录命名统一、可追溯。

---

## 命名格式

```
{主题材前缀}_{序号}
```

**示例**：`xuanhuan_001`, `dushi_002`, `xianxia_015`

---

## 主题材列表

| 主题材 | project_id前缀 | 包含的融合题材 |
|--------|---------------|---------------|
| 玄幻 | `xuanhuan` | 东方玄幻、异世大陆、领主流、王朝争霸 |
| 仙侠 | `xianxia` | 修仙、凡人流、洪荒、古典仙侠 |
| 都市 | `dushi` | 都市修仙、都市异能、重生都市、职场 |
| 科幻 | `kehuang` | 末世、星际、机甲、赛博朋克、时间穿越 |
| 历史 | `lishi` | 历史穿越、架空历史、宫廷、战争 |
| 游戏 | `youxi` | 网游、电竞、游戏异界、无限流 |
| 奇幻 | `qihuan` | 西方奇幻、魔法世界、剑与魔法 |
| 悬疑 | `xuanyi` | 推理、灵异、探险、惊悚 |
| 轻小说 | `qingxiaoshuo` | 日系轻小说、校园、恋爱、日常 |

---

## 命名规则

### 1. 主题材选择

**单一题材**：直接使用对应前缀
- 玄幻小说 → `xuanhuan_XXX`
- 修仙小说 → `xianxia_XXX`

**多题材融合**：使用**主题材**前缀
- 都市修仙 → `dushi_XXX`（主题材是都市）
- 科幻修仙 → `kehuang_XXX`（主题材是科幻）
- 历史玄幻 → `lishi_XXX`（主题材是历史）

**判断主题材**：故事的主要世界观背景
- 现代都市为背景 → `dushi`
- 古代仙侠世界为背景 → `xianxia`
- 西方魔法世界为背景 → `qihuan`

### 2. 序号规则

- 格式：三位数字，从 `001` 开始
- 自动递增：扫描已有项目，生成下一个序号
- 示例：已有 `xuanhuan_001`, `xuanhuan_002` → 新项目为 `xuanhuan_003`

### 3. 自动生成

执行 `/nw-bp-plan` 时自动生成：

```
输入: /nw-bp-plan 都市 重生流

系统处理:
  1. 识别主题材: 都市 → dushi
  2. 扫描已有项目: blueprints/dushi_001/, blueprints/dushi_002/
  3. 生成新ID: dushi_003

输出:
  ✅ 创建蓝图: blueprints/dushi_003/
```

### 4. 手动覆盖

用户可指定自定义 `project_id`：

```bash
/nw-bp-plan 都市 重生流 --id my_custom_name
# → project_id: my_custom_name
```

**自定义命名限制**：
- 仅允许：小写字母、数字、下划线
- 长度：3-30 字符
- 禁止：中文、空格、特殊字符

---

## 书名与 project_id 的关系

### 设计原则

| 属性 | project_id | 书名 |
|------|------------|------|
| 用途 | 文件系统目录名 | 作品正式名称 |
| 格式 | 英文+数字 | 中文书名 |
| 修改 | 创建后不可改 | — |
| 定义时机 | 创建时自动生成 | 发布时输入 |

### 书名定义流程

**蓝图阶段**：不定义书名，专注于内容策划

**发布阶段**：执行 `/nw-release` 时输入书名
- 书名用于导出文件的标题
- 书名不保存到蓝图文件中
- 每次发布可使用不同书名

---

## 示例

### 新建玄幻项目

```
用户: /nw-bp-plan 玄幻 废柴流

系统:
  主题材: 玄幻 → xuanhuan
  已有项目: (无)
  生成ID: xuanhuan_001

结果:
  blueprints/xuanhuan_001/
  ├── proposal.md      # project_id: xuanhuan_001
  ├── worldview.md
  ├── characters.md
  └── outline.md
```

### 新建都市修仙项目

```
用户: /nw-bp-plan 都市 修仙 重生

系统:
  主题材: 都市 → dushi
  融合题材: 修仙、重生
  已有项目: dushi_001, dushi_002
  生成ID: dushi_003

结果:
  blueprints/dushi_003/
  ├── proposal.md      # project_id: dushi_003, 题材标签: 都市+修仙+重生
  └── ...
```

### 发布时输入书名

```
用户: /nw-release dushi_003

系统:
  📖 请确认书名:
     当前项目: dushi_003
     请输入正式书名（如：都市仙尊）:

用户: 都市仙尊

系统:
  ✅ 发布完成!
  📚 书名: 《都市仙尊》
  ...
```

---

## 相关文件

- `commands/nw-bp-plan.md` - 蓝图创建命令（自动生成 project_id）
- `templates/proposal-template.md` - 选题模板
- `commands/nw-release.md` - 发布命令（发布时询问书名）
- `specs/directory-structure.md` - 目录结构规范
