# Contributing to BookMind

感谢你考虑贡献 BookMind！🎉

## 开发环境

- Python ≥ 3.11
- 推荐使用 [uv](https://github.com/astral-sh/uv) 或 venv

```bash
git clone https://github.com/<your-org>/bookmind-agent-suite.git
cd bookmind-agent-suite
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,ocr,export,vector]"
```

## 跑测试

```bash
pytest -v
python -m bookmind.cli doctor
```

## 提交规范

我们用 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat: 新增概念同义词合并`
- `fix: 修复 review_agent 引用不存在的 citations 字段`
- `docs: 更新 README 安装说明`
- `refactor: 拆分 orchestrator`
- `test: 增加 QA agent 测试`

## Pull Request 流程

1. Fork 本仓库
2. 从 `main` 切新分支：`git checkout -b feat/your-feature`
3. 写代码 + 写测试
4. 跑 `pytest`，确保全部通过
5. 跑 `ruff check .` 和 `mypy bookmind/`
6. 提交 + 推送到你的 Fork
7. 在 GitHub 上发起 Pull Request

## 提 Issue 之前

- 搜索是否已有相关 issue
- 附上 `python -m bookmind.cli doctor` 输出
- 附上**不含版权内容**的最小复现 PDF / 命令
- 附上 Python 版本、操作系统、相关依赖版本

## 安全

如发现安全漏洞，请**不要**在公开 issue 中披露，邮件至：
`security@bookmind.example.com`

## License

提交 PR 即代表你同意按 Apache 2.0 License 贡献你的代码。
