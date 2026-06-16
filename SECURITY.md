# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**请勿**在公开 GitHub issue 中披露安全漏洞。

请通过以下方式私密报告：
- 邮件：security@bookmind.example.com
- 或使用 GitHub Security Advisories 的 "Private vulnerability reporting"

我们会在 72 小时内确认收到，并在 14 天内评估与修复。

## 安全设计要点

- 路径白名单 + deny 规则（参见 `bookmind/utils/security.py`）
- 外部命令 allowlist（`ocrmypdf / tesseract / pdftotext / weasyprint` 等）
- 短引用裁剪：默认 ≤ 60 词
- 不执行 PDF 内嵌脚本
- 默认所有产物保存在本地（`~/.bookmind/`、`~/BookMind/`）
- 缓存与日志目录可由环境变量配置

详细安全说明见 [docs/security.md](docs/security.md)。
