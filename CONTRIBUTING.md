# Contributing to BookMind

首先，感谢你花时间为这个项目贡献代码！以下是贡献指南：

## Code of Conduct

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。

## How to Contribute

### Reporting Bugs
- GitHub Issues 提交
- 附上：复现步骤、环境、预期、日志

### Suggesting Features
- GitHub Issues 使用 "Feature Request" 模板
- 说明使用场景和理由

### Pull Requests
1. Fork 本仓库并检出 main 分支
2. 确保所有测试通过 (`pytest -xvs`)
3. 运行质量检查：`ruff check` + `mypy` + `black .`
4. 提交 PR 并描述你的改动

## Dev Setup

```bash
cd bookmind-agent-suite
pip install -e "[dev,ocr,vector,export]"
pytest
```

## Code Style

- Python: PEP8 (via black/ruff)
- 类型注解：完整 mypy 覆盖
- 文档：中文注释 + 英文 docstring
- 提交信息：conventional commits 格式

---

欢迎任何形式的贡献 — PRs、Bug 报告、文档翻译、使用分享！
