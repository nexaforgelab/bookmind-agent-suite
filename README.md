# BookMind Multi-Agent Reading Suite

> **书脑·整本书深度解读多智能体** — 一个可商用的整本书深度解读多 Agent 系统，专为 OpenClaw 和 Hermes 设计。

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-10-purple)](skills/)
[![Agents](https://img.shields.io/badge/agents-13-orange)](bookmind/agents/)

BookMind 是一个 Skill-first 的多智能体系统，把一本 PDF 图书自动拆解为：

- 📖 全书结构与逻辑主线
- 🧠 章节摘要与核心问题
- 💡 概念词典与论证图谱
- 🧐 批判性分析
- 🎯 面向读者目标的可执行方案
- 🗒️ 读书笔记、复习卡片、思维导图
- 📤 多格式导出（Markdown / HTML / JSON / Anki / Obsidian / Mermaid）

## ✨ 核心特性

- **多 Agent 协作**：13 个专职 Agent，分工明确，质量可审计
- **Skill-first 架构**：每个能力都是独立可分发的 Skill，符合 OpenClaw / Hermes 标准
- **版权安全**：默认只做摘要、短引用、观点提炼，所有引用带页码
- **长文档友好**：分块、章节处理、上下文压缩、断点续跑、缓存
- **多语言支持**：中、英、中英混排
- **多 PDF 场景**：文字 PDF / 扫描 PDF / 图片 PDF / 混合排版 / 带目录 / 无目录
- **工程化**：类型标注、日志、错误处理、单元测试、Docker、可扩展

## 🏗️ 架构

```
                ┌──────────────────────────────┐
                │  BookDirectorAgent (总导演)   │
                └──────────────┬───────────────┘
                               │
       ┌────────────┬──────────┼──────────┬────────────┐
       ▼            ▼          ▼          ▼            ▼
 Structure    ChapterSummary Concept  Argument  Evidence
   Agent          Agent       Agent     Agent     Agent
       │            │          │          │            │
       └────────────┴──────────┼──────────┴────────────┘
                               ▼
                  CriticalThinking / Application / Notes
                               ▼
                  Mindmap / Review / ReportEditor
                               ▼
                   📤 多格式导出
```

## 📦 安装

### 方式一：本地安装

```bash
git clone <your-repo> bookmind-agent-suite
cd bookmind-agent-suite
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 方式二：Docker

```bash
docker-compose up --build
```

### 方式三：OpenClaw 一键安装

```bash
./install_openclaw.sh
```

### 方式四：Hermes 一键安装

```bash
./install_hermes.sh
```

## 🚀 快速开始

### CLI 方式

```bash
python -m bookmind.cli analyze /path/to/book.pdf \
  --mode deep \
  --goal 通识理解 \
  --output-language zh-CN \
  --export markdown,html,json \
  --output-dir ~/BookMind/reports
```

### 问答模式

```bash
python -m bookmind.cli ask ./book_index.sqlite "这本书的核心观点是什么？"
```

### 导出

```bash
python -m bookmind.cli export ./book_insight.json --format obsidian --out ~/Notes
```

### 健康检查

```bash
python -m bookmind.cli doctor
```

### 清理缓存

```bash
python -m bookmind.cli clean-cache
```

## 🛠️ 在 OpenClaw 中使用

参见 [docs/openclaw_usage.md](docs/openclaw_usage.md) 和 [examples/openclaw_usage.md](examples/openclaw_usage.md)。

```bash
openclaw agent --message "/book-deep-reading /path/to/book.pdf --mode deep --goal 通识理解"
```

## 🛠️ 在 Hermes 中使用

参见 [docs/hermes_usage.md](docs/hermes_usage.md) 和 [examples/hermes_usage.md](examples/hermes_usage.md)。

```bash
hermes
/book-reading-suite /path/to/book.pdf --mode deep --goal 商业应用
```

## 📋 阅读模式

| 模式       | 描述               | 适合场景               |
|----------|------------------|--------------------|
| `quick`  | 10 分钟速读          | 选书、判断要不要读          |
| `standard` | 标准读书报告         | 大多数阅读场景            |
| `deep`   | 整本书深度拆解         | 系统性学习、读书会、知识库建设    |
| `expert` | 专家级批判性分析        | 学术研究、专业评论、二次创作     |

## 🎯 读者目标

- 通识理解
- 商业应用
- 投资研究
- 产品经理视角
- 学术研究
- 教师备课
- 考试复习
- 写作素材提炼
- 个人成长实践

## 📁 导出格式

- Markdown (`.md`)
- HTML (`.html`)
- JSON (`.json`)
- CSV (`evidence_table.csv`)
- Anki CSV (`anki_cards.csv`)
- Obsidian Vault（每章一篇 + 双链 + 标签）
- Mermaid 思维导图（`.mmd`）
- 可选 PDF 报告（依赖 weasyprint）

## 🧪 运行测试

```bash
pytest -q
```

## 🛡️ 安全与版权

参见 [docs/security.md](docs/security.md)。

- 默认不输出大段原文
- 短引用必须带页码
- 不执行 PDF 内嵌脚本
- 对外部命令 allowlist
- 路径安全检查

## 📜 License

Apache 2.0，商用友好，详见 [LICENSE](LICENSE)。

## 🗺️ Roadmap

- [ ] 多模态支持（图表解析、公式识别）
- [ ] 多书对比阅读
- [ ] 跨书知识图谱
- [ ] Web UI
- [ ] 多用户协作读书会
- [ ] 移动端 App
- [ ] 知识库自动同步到 Notion / Logseq
