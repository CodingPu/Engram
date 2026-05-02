# Engram 快速开始指南

**前置要求：**
- Python 3.10+
- Git
- Claude API Key（免费注册：https://console.anthropic.com）

---

## 1️⃣ 克隆并初始化项目

```bash
git clone https://github.com/YOUR_USERNAME/engram.git
cd engram

# 初始化项目（创建目录和示例文件）
python init_project.py
```

**输出应该看起来像：**
```
🚀 Engram 项目初始化

1️⃣  验证项目结构...
   ✓ 所有目录已创建

2️⃣  检查关键配置文件...
   ✓ CONVENTIONS.md
   ...

✅ 项目初始化完成！
```

---

## 2️⃣ 配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑 .env（用你的编辑器）
code .env
```

**需要填的项目：**

```
# Claude API Key（必需）
CLAUDE_API_KEY=sk-ant-...

# QQ Bot 配置（暂可跳过，后期补充）
QQ_BOT_ID=123456789
QQ_USER_IDS=你的QQ号
```

**获取 Claude API Key：**
1. 访问 https://console.anthropic.com
2. 创建账户并充值（推荐 $10-20）
3. 在 API Keys 页面创建新 key
4. 复制到 `.env`

---

## 3️⃣ 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
source venv/bin/activate       # Linux/Mac
# or
venv\Scripts\activate           # Windows

# 安装依赖
pip install -r requirements.txt
```

**预期耗时：** 2-3 分钟

---

## 4️⃣ 验证安装

```bash
# 检查 Claude API
python -c "import anthropic; print('✓ Claude SDK installed')"

# 检查项目结构
ls -la wiki/
ls -la activities/

# 查看示例活动
cat activities/deck.json
```

---

## 5️⃣ 浏览项目文档

```bash
# Wiki 规范（所有页面必须遵循）
cat CONVENTIONS.md

# LLM 定义（Prompt 和输出格式）
cat SCHEMA.md

# 开发计划（路线图和任务）
cat DEVELOPMENT_PLAN.md
```

---

## 📝 项目结构速查

```
engram/
├── wiki/                      # 💾 知识库（Markdown 文件）
│   ├── concepts/             # 概念页面
│   ├── index.md              # 目录（自动维护）
│   └── log.md                # 操作日志（自动追加）
│
├── ingest/                    # 🔄 摄入管道
│   ├── agents/               # LLM agents（单角色、多角色）
│   ├── processors/           # 内容预处理（PDF、Markdown 等）
│   └── prompts/              # Claude Prompt 模板
│
├── bot/                       # 🤖 推送服务
│   ├── server.py             # QQ Bot 服务器
│   ├── scheduler.py          # FSRS 调度
│   └── channels/             # 推送通道（QQ、Telegram、终端）
│
├── activities/               # 📚 学习活动
│   └── deck.json            # 活动队列（FSRS 数据）
│
├── tools/                    # 🛠 工具函数
│   ├── wiki_writer.py        # Wiki 生成
│   ├── scheduler.py          # FSRS 调度
│   └── activity_manager.py   # 活动管理
│
├── CONVENTIONS.md            # Wiki 规范
├── SCHEMA.md                 # LLM Prompt 定义
├── DEVELOPMENT_PLAN.md       # 项目路线图
├── requirements.txt          # 项目依赖
├── .env.example              # 环境变量模板
└── docker-compose.yml        # Docker 配置
```

---

## 🧪 第一个测试：加载示例活动

```bash
python -c "
import json
with open('activities/deck.json') as f:
    data = json.load(f)
    print(f'✓ 加载了 {len(data[\"activities\"])} 个活动')
    for activity in data['activities'][:2]:
        print(f\"  - {activity['type'].upper()}: {activity['question']}\")
"
```

**预期输出：**
```
✓ 加载了 3 个活动
  - FACT: 什么是间隔重复？
  - FEYNMAN: 用自己的话解释 Ebbinghaus 遗忘曲线。
```

---

## 🎯 下一步：开始开发第一阶段

### Week 2：Wiki 和 Ingest 基础

我们将创建：
1. `tools/wiki_writer.py` — Wiki 页面生成和维护
2. `ingest/pipeline.py` — 单角色摄入管道
3. 基础的 Claude Prompt

### 任务清单

- [ ] 完成 Wiki 读写模块
- [ ] 实现单角色 Ingest 管道
- [ ] 测试：能从 Markdown 文章生成 Wiki 页面 + 活动
- [ ] 通过集成测试

**预计耗时：** 1-2 周

---

## 🆘 常见问题

### Q: 装完依赖后说找不到 claude？

**A:** 检查虚拟环境激活了没

```bash
which python  # 应该输出 venv 路径下的 python
```

### Q: Claude API Key 怎么获取？

**A:** 
1. 访问 https://console.anthropic.com
2. 邮箱注册账户
3. 绑定信用卡充值（最少 $5）
4. API Keys 页面创建新 key
5. 复制到 `.env` 文件

### Q: 能用免费的 LLM 吗？

**A:** 可以，但需要修改代码。后期支持：
- Ollama（本地运行 Llama 等）
- MiMo（国内替代方案）
- 自建模型

### Q: 没有 QQ 账号怎么测试 Bot？

**A:** 前期可以跳过，等 ingest 和 Wiki 模块稳定后再加 Bot。我们会分步实现。

---

## 📚 学习资源

- **Claude API 文档** — https://docs.anthropic.com
- **FSRS 论文** — https://github.com/open-spaced-repetition/fsrs4anki
- **Engram 规范** — 项目根目录的 CONVENTIONS.md 和 SCHEMA.md

---

**有问题？** 在 GitHub Issues 提问。

**准备好了？** 继续查看 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) 了解详细的第一阶段任务。
