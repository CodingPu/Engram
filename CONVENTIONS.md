# Engram Wiki 规范

> 所有 Wiki 页面必须遵循本规范，确保结构一致、质量稳定、可追溯

**版本：** 1.0  
**最后更新：** 2026-05-02

---

## 页面结构

### 文件命名

```
规范：snake_case.md
示例：
  - spaced_repetition.md       (概念)
  - fsrs_algorithm.md          (算法)
  - claude_api.md              (工具/服务)
  - karpathy_llm_wiki.md       (来源)
```

### 目录结构

```
wiki/
├── concepts/        # 概念、理论、原理
│   ├── learning_science.md
│   ├── spaced_repetition.md
│   └── fsrs_algorithm.md
│
├── entities/        # 人物、组织、事件
│   ├── andrej_karpathy.md
│   └── anthropic.md
│
├── sources/         # 文献、论文、来源索引
│   ├── karpathy_llm_wiki.md
│   └── fsrs_research_papers.md
│
├── synthesis/       # 综合分析、笔记、感悟
│   ├── learning_strategies.md
│   └── spaced_repetition_practice.md
│
├── index.md         # 目录（自动维护）
└── log.md          # 操作日志（自动追加）
```

---

## 页面 Frontmatter 规范

每个页面开头必须有 YAML frontmatter：

```yaml
---
title: 间隔重复学习法
category: concepts           # concepts / entities / sources / synthesis
tags: [learning, fsrs, spaced-repetition]
confidence: high             # high / medium / low
created: 2026-05-02
last_modified: 2026-05-02
sources:
  - karpathy_llm_wiki.md
  - fsrs_research.pdf
related:
  - fsrs_algorithm.md
  - learning_science.md
author: 
  type: human | llm          # 创建者类型
  ingest_method: single | multi  # 单角色 / 多角色提取
---
```

**字段说明：**

| 字段 | 说明 | 取值 |
|------|------|------|
| `title` | 页面标题 | 字符串 |
| `category` | 分类（决定放在哪个目录） | concepts / entities / sources / synthesis |
| `tags` | 标签（用于检索） | 数组，中文或英文 |
| `confidence` | 置信度（数据可靠性） | high（✓） / medium（⚠️） / low（❌） |
| `created` | 创建日期 | YYYY-MM-DD |
| `last_modified` | 最后修改日期 | YYYY-MM-DD |
| `sources` | 来源文件 | 引用的源材料或来源页面 |
| `related` | 相关页面 | 关联的其他 Wiki 页面 |
| `author.type` | 作者类型 | human（手动）或 llm（AI 生成） |
| `author.ingest_method` | 摄入方式 | single（单角色）或 multi（多角色验证） |

---

## 内容规范

### 标题层次

```markdown
# 一级标题（页面标题，必须只有一个）

## 二级标题（大章节）

### 三级标题（小节）

#### 四级标题（子项）
```

### 列表格式

**无序列表：** 用 `-` 或 `*`

```markdown
- 第一点
- 第二点
  - 子点 2.1
  - 子点 2.2
```

**有序列表：** 用数字

```markdown
1. 第一步
2. 第二步
   1. 子步骤 2.1
   2. 子步骤 2.2
```

### 表格规范

```markdown
| 列1 | 列2 | 说明 |
|-----|-----|------|
| 值1 | 值2 | 描述 |
```

### 代码块

````markdown
```python
# Python 代码示例
def fsrs_interval(difficulty, stability, retrievability):
    return stability * (retrievability ** (1 / difficulty))
```
````

### 引用和说明

```markdown
> **重要：** 这是一个关键概念
> 多行说明文本

> **来源：** Karpathy 的 LLM Wiki  
> **链接：** https://gist.github.com/karpathy/...
```

---

## 置信度标记规范

### Frontmatter 中的 confidence

```yaml
confidence: high      # ✓ 数据可靠，可直接使用
confidence: medium    # ⚠️ 数据有歧义，需标注
confidence: low       # ❌ 数据不确定，待审核
```

### 页面中的标记

在内容中标注不确定的部分：

```markdown
## 费用表

| 项目 | 费用 | 置信度 |
|------|------|--------|
| 挖泥 | ¥850 | ✓ high |
| 运输 | ¥320 | ⚠️ medium |
| 安装 | ¥150 | ❌ low |

### 说明

- **high（✓）：** 三个 agent 一致，或审计员高度确信。可直接入库并生成学习活动。
- **medium（⚠️）：** 两个 agent 不一致，审计员有倾向。入库但不生成学习活动，等待人工确认。
- **low（❌）：** 三个 agent 都不确定。不入库，放入待审核队列。

### 审计备注

> **提取方式：** 三角色交叉验证（Agent A / B / C）  
> **矛盾：** 运输费在 Agent B（320）和 Agent A（280）间有分歧  
> **建议：** 查看原始 PDF 第 38 页，确认实际费用
```

---

## 跨链接规范

### Wiki 内部链接

```markdown
详见 [间隔重复学习法](../concepts/spaced_repetition.md)

或（相对路径）：
详见 [FSRS 算法](fsrs_algorithm.md)
```

### 外部链接

```markdown
参考 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
```

---

## 具体示例

### 示例 1：概念页面

**文件：** `wiki/concepts/spaced_repetition.md`

```yaml
---
title: 间隔重复（Spaced Repetition）
category: concepts
tags: [learning, memory, neuroscience]
confidence: high
created: 2026-05-02
sources:
  - ebbinghaus_forgetfulness.pdf
related:
  - fsrs_algorithm.md
  - learning_science.md
author:
  type: llm
  ingest_method: single
---

# 间隔重复（Spaced Repetition）

## 定义

间隔重复是一种基于遗忘曲线的学习方法。核心思想是：**在你即将遗忘某个知识点时，再次复习它**。

## 原理

根据 Ebbinghaus 遗忘曲线：
- 学习后 1 小时：保留 50%
- 学习后 1 天：保留 30%
- 学习后 1 周：保留 20%

通过在关键时间点复习，可以大幅提升长期记忆。

## 现代算法

- **SM-2（1987）：** 最早的算法，Anki 采用
- **FSRS（2022）：** 新一代算法，比 SM-2 高效 30%+

详见 [FSRS 算法](fsrs_algorithm.md)

## 参考文献

> 来源：Ebbinghaus (1885) *Memory*  
> 现代应用：[FSRS 论文](https://github.com/open-spaced-repetition/fsrs4anki)

---
```

### 示例 2：数据页面（多角色审计）

**文件：** `wiki/sources/construction_quotas.md`

```yaml
---
title: 码头工程定额
category: sources
tags: [construction, quotas, civil-engineering]
confidence: medium
created: 2026-05-02
sources:
  - 码头工程定额.pdf
author:
  type: llm
  ingest_method: multi
---

# 码头工程定额

## 基槽挖泥费用表

| 项目 | 一类费(¥) | 二类费(¥) | 置信度 |
|------|----------|----------|--------|
| 挖泥船 450m³/h | 850 | 320 | ✓ high |
| 挖泥船 980m³/h | 1200 | 405 | ⚠️ medium |
| 挖泥船 1500m³/h | 1800 | 550 | ✓ high |

## 数据说明

> **来源文件：** 码头工程定额.pdf 第 38-39 页  
> **提取方式：** 三角色交叉验证  
> **提取时间：** 2026-05-02

### 置信度标记说明

- **high（✓）：** 表格清晰，三个 agent 提取结果一致
- **medium（⚠️）：** 980m³/h 的二类费在 Agent B（420）和 Agent A（405）间有 15 的差异
  - Agent A（严格）：405（精确逐行扫描）
  - Agent B（理解）：420（根据比例推算）
  - 建议采用 Agent A（405），B 可能看串了第 4 行和第 5 行

### 使用建议

- high 的数据可直接用于教学
- medium 的数据可用，但建议标注"来源有歧义"
- low 的数据不建议使用，需人工确认

---
```

### 示例 3：合成页面（人工笔记）

**文件：** `wiki/synthesis/learning_workflow.md`

```yaml
---
title: 我的学习工作流
category: synthesis
tags: [learning, workflow, personal]
confidence: high
created: 2026-05-02
author:
  type: human
related:
  - spaced_repetition.md
  - fsrs_algorithm.md
---

# 我的学习工作流

## 流程

1. **摄入阶段** - 找到一篇文章或教程
   - Engram 自动提取关键信息
   - 生成 Wiki 页面 + 学习活动

2. **审核阶段** - 检查数据质量
   - 检查置信度标记
   - 如果有歧义，手动补充说明

3. **学习阶段** - 通过多种活动主动回忆
   - 费曼挑战：用自己的话解释
   - 连接挑战：联系多个概念
   - 情境应用：在真实场景中使用

4. **推送阶段** - 系统定时推送
   - 终端弹窗（每次打开终端）
   - QQ Bot（早中晚推送，包括语音）

## 心得

- 置信度很重要，直接影响学习质量
- 多种活动类型比单调的卡片有效
- 推送找你比你主动打开 app 的坚持率高 10 倍

---
```

---

## 自动维护的文件

### index.md（目录）

**自动生成内容：**

```markdown
# Wiki 目录

## Concepts（概念，共 15 页）

- [间隔重复学习法](concepts/spaced_repetition.md) — 基于遗忘曲线的高效学习方法
- [FSRS 算法](concepts/fsrs_algorithm.md) — 新一代间隔重复算法
- ...

## Entities（实体，共 8 页）

- [Andrej Karpathy](entities/andrej_karpathy.md) — LLM 研究先驱
- ...

## Sources（来源，共 12 页）

- [Karpathy 的 LLM Wiki](sources/karpathy_llm_wiki.md) — Engram 的灵感来源
- ...

## Synthesis（综合，共 5 页）

- [我的学习工作流](synthesis/learning_workflow.md) — 个人实践总结
- ...

---

**最后更新：** 2026-05-02  
**总页数：** 40  
**total words：** ~50,000  
```

### log.md（操作日志）

**自动追加格式：**

```markdown
# Wiki 操作日志

## 2026-05-02

### 09:30 - Ingest

```
来源：DEVELOPMENT_PLAN.md
类型：摄入（Ingest）
方式：单角色提取
生成页面：concepts/spaced_repetition.md
生成活动数：3
状态：✓ 完成
```

### 08:15 - Query

```
问题："FSRS 和 SM-2 有什么区别？"
回答者：Claude
数据来源：concepts/fsrs_algorithm.md, concepts/spaced_repetition.md
质量评分：high
Wiki 更新：concepts/fsrs_algorithm.md （加入对比内容）
```

---
```

---

## 质量检查清单

每次 Ingest / Query / Lint 后，检查：

- [ ] Frontmatter 完整（title, category, confidence, sources）
- [ ] 内部链接有效（没有断链）
- [ ] 代码块有语言标记（\`\`\`python）
- [ ] 表格格式正确（对齐）
- [ ] 置信度标记准确
- [ ] 没有敏感或错误信息
- [ ] 长度合理（2000-5000 字）

---

## 版本历史

| 版本 | 日期 | 改动 |
|------|------|------|
| 1.0 | 2026-05-02 | 初始规范 |

---

**维护者：** Engram 开发团队  
**反馈：** 在 GitHub Issues 提交建议
