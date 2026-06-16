# Skill 设计规范

BookMind 的所有 Skill 必须遵循本规范。

## 1. 目录结构

```
skills/<skill-name>/
├── SKILL.md            # 必需
├── scripts/            # 至少一个 entry script
│   └── run_<skill>.py
├── templates/          # 可选，Jinja2 模板
├── references/         # 可选，知识库 / 文档
└── tests/              # 可选，单元测试
```

## 2. SKILL.md 必备字段

```yaml
---
name: <skill-name>
description: 一句话说明 + 适用场景
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [...]
    category: ...
    requires_toolsets: [...]
---
```

正文部分必须包含：
- **When to Use**
- **Procedure**（步骤）
- **Safety and Copyright**
- **Verification**（验证标准）
- **Example**（命令示例）
- **Failure Handling**

## 3. 入口脚本

`scripts/run_<skill>.py` 必须：

1. 解析参数。
2. 调用 `bookmind.skills_runtime.skill_executor.execute_skill` 或子模块。
3. 把结果以 JSON 打印到 stdout。
4. 不抛未捕获异常。

## 4. 兼容性

- Skill 必须能在 OpenClaw 与 Hermes 中以相同入口运行。
- 任何 Hermes 专属能力必须通过 `metadata.hermes` 显式声明。

## 5. 安全

- 任何文件写入只能进入：
  - `BOOKMIND_OUTPUT_DIR`
  - `BOOKMIND_CACHE_DIR`
  - 用户明确指定目录
- 任何外部命令必须走 `CommandAllowlist`。
- 任何短引用必须可追溯到页码 / 章节。

## 6. 版本

`SKILL.md` 的 `version` 字段遵循 semver。
任何破坏性改动必须升 major。
