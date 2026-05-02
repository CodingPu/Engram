# Engram 项目开发计划

> 🎯 目标：3 个月内完成 MVP，建立可运行的完整闭环

**更新时间：** 2026年5月2日  
**项目模式：** MIT + SaaS（开源社区 + 商业化版本）

---

## 第零阶段：基础准备（Week 1 - 现在）

### 任务清单

**架构和设计**
- [x] 完成 Readme 文档（已提交）
- [ ] 创建 CONVENTIONS.md（Wiki 规范）
- [ ] 创建 SCHEMA.md（LLM 行为定义）
- [ ] 设计数据结构（deck.json、log.md、wiki 格式）

**开发环境**
- [ ] 建立项目文件夹结构
- [ ] 创建 requirements.txt（依赖）
- [ ] 创建 .env.example（配置模板）
- [ ] 创建 docker-compose.yml（容器编排）

**验证**
- [ ] 选定主要技术栈（Python 版本、框架等）
- [ ] 确认 API 供应商（LLM、TTS、QQ Bot）
- [ ] 评估成本（单用户月均成本）

### 产出物
```
engram/
├── CONVENTIONS.md       # Wiki 规范（样例）
├── SCHEMA.md            # LLM prompt 规范（初稿）
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
├── docker-compose.yml   # 本地开发环境
├── DEVELOPMENT_PLAN.md  # 这个文件
└── wiki/
    ├── index.md         # Wiki 目录（示例）
    └── example.md       # Wiki 页面示例（含置信度格式）
```

---

## 第一阶段：MVP 核心（Week 2-4 | 3周）

**目标：** 能走通一个完整的"摄入→学习→推送→回复"闭环  
**验收标准：** 自己用它学一个领域的知识，全流程可用

### 1️⃣ Wiki 基础设施（Week 2）

**要做的：**
- [ ] 实现 Wiki 写入系统（Markdown 生成器）
  - 支持自动添加 frontmatter（日期、置信度、来源）
  - 支持模板填充（表格、列表等）
  - 维护 index.md（自动更新页面目录）
  - 维护 log.md（操作日志）

- [ ] Wiki 读取系统
  - 支持按 category/concept/entity 分类读取
  - 支持全文搜索（简单的正则/关键词）

**验收标准**
```
✓ 能手动创建一个 Wiki 页面，自动维护 index.md
✓ 能读取 Wiki，提取结构和内容
✓ 能追加操作到 log.md
```

**代码结构**
```python
tools/
├── wiki_writer.py      # Wiki 页面生成和维护
├── wiki_reader.py      # Wiki 查询和读取
└── wiki_indexer.py     # index.md + log.md 维护
```

---

### 2️⃣ 单角色 Ingest 管道（Week 2-3）

**要做的：**
- [ ] 内容预处理器
  ```python
  ingest/processors/
  ├── markdown.py        # Markdown 文章解析
  ├── pdf.py             # PDF → 图片转换（PyMuPDF）
  ├── text.py            # 纯文本解析
  └── url.py             # 网页链接爬取
  ```

- [ ] 单角色提取器（先用 Claude / MiMo）
  ```python
  ingest/agents/
  ├── extractor.py       # 通用提取模块
  └── prompts/
      └── extract.md     # 提取 prompt 模板
  ```

- [ ] Ingest 主管道
  ```python
  ingest/pipeline.py
  
  流程：
    1. 读取源材料（markdown / pdf / url）
    2. 预处理（格式转换、图片提取）
    3. 调用 LLM 提取关键信息
    4. 生成 Wiki 页面 + 活动卡片
    5. 追加到 log.md
  ```

**验收标准**
```
✓ python ingest/pipeline.py raw/articles/test.md
  生成 wiki/concepts/xxx.md 和对应的活动卡片
✓ log.md 自动追加 ingest 记录
```

**成本估算**
```
每次摄入 1 篇文章：~¥0.05 （一次 API 调用）
```

---

### 3️⃣ FSRS 调度核心（Week 3）

**要做的：**
- [ ] 活动队列数据结构
  ```python
  activities/deck.json
  
  {
    "activities": [
      {
        "id": "uuid",
        "type": "fact",  # fact|feynman|connection|scenario|teach
        "question": "FSRS 是什么？",
        "source_wiki_id": "fsrs.md",
        "created_at": "2026-05-02",
        "fsrs": {
          "difficulty": 5,
          "stability": 20,
          "retrievability": 0.9,
          "last_review": "2026-05-02",
          "next_review": "2026-05-05",
          "reps": 1,
          "lapses": 0
        }
      }
    ]
  }
  ```

- [ ] FSRS 调度算法
  ```python
  tools/scheduler.py
  
  功能：
    1. 计算 next_review（基于参数和间隔）
    2. 获取今日待复习（retrievability > 0.5）
    3. 更新 FSRS 参数（根据用户反馈）
  ```

- [ ] 活动管理
  ```python
  tools/activity_manager.py
  
  功能：
    1. 创建活动（从 Wiki 生成）
    2. 获取下一个活动
    3. 提交反馈（again/hard/good/easy）
  ```

**验收标准**
```
✓ 手动创建一个活动，自动计算 next_review
✓ 获取今日待复习的活动
✓ 提交反馈后，FSRS 参数更新正确
```

**参考**
```
FSRS 4 参数：
  - difficulty: 1-10，问题难度
  - stability: 回忆力强度（天数）
  - retrievability: 0-1，当前可回忆的概率
  
简单规则：
  - again: difficulty++, stability/=2
  - hard: difficulty+=0.5, stability*=0.9
  - good: difficulty不变, stability*=1.1
  - easy: difficulty-=1, stability*=1.3
```

---

### 4️⃣ 推送渠道：终端（Week 3-4）

**要做的：**
- [ ] 终端推送脚本
  ```bash
  shell/engram_prompt.sh
  
  功能：
    1. 从 activities/deck.json 读取今日活动
    2. 随机选一个
    3. 格式化成弹窗
    4. 读取用户输入（Enter / Esc / c）
  ```

- [ ] 集成到 shell
  ```bash
  ~/.zshrc 或 ~/.bashrc
  
  if command -v python &> /dev/null; then
    python ~/.engram/terminal_push.py
  fi
  ```

**验收标准**
```
✓ 每次打开新终端，自动弹一条 Engram 推送
✓ Enter 查看对话，Esc 跳过，c 标记已掌握
✓ 可正确读取用户反馈，更新 FSRS
```

**示例**
```
┌─ Engram ──────────────────────────────┐
│                                       │
│  💡 小安想请教你：                    │
│                                       │
│  "FSRS 的四个参数是什么？              │
│   我老是记混。"                       │
│                                       │
│  [Enter 查看]  [Esc 跳过]  [c 掌握]   │
│  今日进度: 1/3  │  连续: 3 天         │
└───────────────────────────────────────┘
```

---

### 5️⃣ 推送渠道：QQ Bot（Week 3-4）

**要做的：**
- [ ] QQ Bot 框架
  ```python
  bot/server.py
  
  使用 NapCat / Lagrange（OneBot 11 标准）
  - 连接到本地 QQ 客户端
  - 监听消息事件
  - 发送消息
  ```

- [ ] 人格化消息生成
  ```python
  bot/persona.py
  
  功能：
    1. 将活动转化成"朋友请教"的语气
    2. 根据活动类型生成不同的问题措辞
    3. 处理用户回复逻辑
  ```

- [ ] 推送调度
  ```python
  bot/scheduler.py
  
  功能：
    1. 定时获取今日待推送活动
    2. 选择合适的时间段推送（早上/中午/晚上）
    3. 处理用户反馈
  ```

**验收标准**
```
✓ QQ Bot 能接收并回复消息
✓ 能主动推送一条"朋友请教"式的活动
✓ 能读取用户的文字回复，记录反馈
```

**人格示例**
```
"诶，我最近在学 FSRS，有个地方没想明白。
 四个核心参数到底是什么啊？我老记混。
 你这块熟吗？能给我讲讲不？"
```

---

### 6️⃣ 集成和测试（Week 4）

**要做的：**
- [ ] 本地完整流程测试
  ```
  1. ingest 一篇文章 → Wiki + 活动
  2. 查看活动列表
  3. 终端弹出推送
  4. 用户回复
  5. FSRS 更新
  6. QQ Bot 推送（如果已连接）
  ```

- [ ] 文档
  ```markdown
  docs/
  ├── SETUP.md         # 本地开发环境搭建
  ├── CONVENTIONS.md   # Wiki 和活动规范
  ├── API_KEYS.md      # 配置 LLM / QQ Bot
  └── WORKFLOW.md      # 日常使用流程
  ```

- [ ] 样例数据
  ```
  raw/
  ├── articles/
  │   └── example.md   # 示例文章
  └── papers/
      └── example.pdf  # 示例 PDF
  
  wiki/
  ├── index.md         # 生成的目录
  ├── example.md       # 生成的 Wiki 页面
  └── log.md          # 操作日志
  ```

---

## 第二阶段：多角色审计（Week 5-8 | 4周）

**前置条件：** 第一阶段完全验证成功

**目标：** 加入知识质量管理  
**验收标准：** 多角色能有效发现数据矛盾，置信度标记准确

### 核心工作

- [ ] 多角色框架
  ```python
  ingest/agents/
  ├── strict.py        # Agent A：严格提取
  ├── interpretive.py  # Agent B：理解提取
  ├── auditor.py       # Agent C：审计员
  └── prompts/
      ├── strict.md
      ├── interpretive.md
      └── audit.md
  ```

- [ ] 置信度评分
  ```python
  ingest/confidence.py
  
  输出：
    high   → 直接入库
    medium → 标记待验证，不生成活动
    low    → 待审核队列，通知用户
  ```

- [ ] Wiki 置信度标记
  ```markdown
  # 定额表
  
  | 项目 | 费用 | 置信度 |
  |------|------|--------|
  | 挖泥 | 850  | ✓ high |
  | 运输 | 320  | ⚠️ medium |
  
  > 来源：定额.pdf 第 38 页
  > 提取：三角色验证
  ```

---

## 第三阶段：语音 + 深度学习（Week 9-13 | 5周）

**前置条件：** 第二阶段完全验证

**目标：** 多种学习活动类型，语音推送  
**验收标准：** 用户反馈学习体验 > Anki

### 核心工作

- [ ] TTS 集成（MiMo / Edge）
- [ ] 费曼挑战模式（自由输入 + LLM 批改）
- [ ] 连接挑战（跨领域概念）
- [ ] 情境应用（场景化）
- [ ] 教学模拟（讲解评分）

---

## 第四阶段：SaaS 版本（Week 14+）

**目标：** 商业化版本  
**模式：** 云端托管 + 多用户 + 付费

### 核心工作

- [ ] 后端 API（FastAPI / Django）
- [ ] 前端 Web / 移动端
- [ ] 用户认证和账户管理
- [ ] 云端 Wiki 存储和同步
- [ ] 定价模型（$9.99/月 或 $79.99/年）

---

## 关键决策点

### 1. 技术栈确认

```
后端：Python 3.10+
  - 核心框架：FastAPI (API) + Click (CLI)
  - LLM 集成：claude-3.5-sonnet（主要） + MiMo（备选）
  - 数据库：SQLite (MVP) → PostgreSQL (SaaS)
  - 调度：APScheduler（定时任务）
  - TTS：MiMo SDK / Edge TTS API

前端（SaaS 阶段）：
  - Web：React + TypeScript
  - 移动：React Native / Flutter

Bot：
  - QQ：NapCat / Lagrange
  - Telegram：python-telegram-bot

容器：Docker Compose
```

### 2. API 供应商

```
LLM：
  ✓ Claude API ($0.003 / 1K input tokens)
  ✓ MiMo API ($0.000035 / 1K tokens，更便宜)
  
TTS：
  ✓ MiMo TTS（中文质量好）
  ✓ Edge TTS（免费，质量可)
  
QQ Bot：
  ✓ NapCat（最活跃）
  ✓ Lagrange（备选）
```

### 3. 成本预估

```
单用户，每个月（假设每天 1 个推送）：

Ingest（每周 2 篇文章）：
  2 × $0.005 = $0.01

Review（每天 1 个，30 天）：
  30 × $0.005 = $0.15

TTS（每天 1 次，30 天，15 秒）：
  30 × $0.02 = $0.60

合计：~$0.76 / 月

多角色（可选）：3 倍成本 → $2.28 / 月
```

---

## 时间线总结

```
Week 1   | 基础准备        ✓ 进行中
Week 2-4 | MVP 核心       → 开始
Week 5-8 | 多角色审计      → 4 周
Week 9+ | 语音 + SaaS     → 后续

总耗时：3-4 个月完成 MVP + 多角色
```

---

## 里程碑

- **2026 年 5 月底** | MVP 可用（单用户，本地版）
- **2026 年 6 月中** | 多角色审计验证
- **2026 年 7 月** | 内测版本（邀请 5-10 个用户）
- **2026 年 8 月** | 第一版开源发布 + SaaS 公测
- **2026 年 9 月+** | 持续迭代和商业化

---

## 立刻要做的

### 今天 / 明天（优先级排序）

1. **创建 CONVENTIONS.md**（Wiki 规范）
   - 定义 wiki 页面的 frontmatter 格式
   - 定义置信度标记的方式
   - 给出 3-5 个具体示例

2. **创建 SCHEMA.md**（LLM 行为定义）
   - 单角色提取的 prompt 模板
   - 各活动类型的生成规则

3. **建立项目文件夹结构**
   ```bash
   mkdir -p {ingest/{agents,processors,prompts},
             bot/{channels},
             wiki/{concepts,entities,sources,synthesis},
             raw/{articles,papers,books},
             activities/templates,
             tools,
             tests,
             docs}
   ```

4. **确认技术栈和 API**
   - 选定主要 LLM（Claude 还是 MiMo）
   - 选定 QQ Bot 框架（NapCat 还是 Lagrange）
   - 申请 API Key

5. **创建 requirements.txt**
   ```
   python-dotenv
   pydantic
   fastapi (后期)
   apscheduler
   click
   openai (Claude 调用)
   ```

---

## 问题列表

需要你确认的：

- [ ] 优先用 Claude 还是 MiMo？（价格 vs 性能）
- [ ] QQ Bot 首先用哪个？（NapCat 还是 Lagrange）
- [ ] 有没有现成的 QQ 账号和群组用于测试？
- [ ] 开发过程中想邀请谁参与内测？
- [ ] 商业化方向：SaaS $9.99/月，还是其他模式？

---

**下一步行动：** 等待 push 完成后，从"立刻要做的"开始推进 ✨
