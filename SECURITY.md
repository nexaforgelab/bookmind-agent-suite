# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

如果你发现了安全漏洞，请通过以下方式联系维护者：

- Email: security@bookmind.dev
- GitHub Security Advisory (private vulnerability reporting)

**请不要公开开 issue。**

我们会在 48 小时内首次响应，然后在 7 个工作日内修复或给出计划。

## Scope

本项目已实现的安全边界：

1. **路径白名单**：所有文件操作仅允许在配置的目录内
2. **命令白名单**：外部命令严格过滤，不允许任意 shell 执行
3. **引用裁剪**：导出的引用内容默认按比例裁剪，避免版权问题

---

Thanks for helping keep BookMind safe and trustworthy.
