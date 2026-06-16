# 商用二次开发建议

## 1. 场景

- 付费读书产品：把 BookMind 包装为 SaaS / 桌面端。
- 企业读书会：批量处理内部指定书目。
- 教育产品：教师备课 / 学生复习。
- 投研工作流：研究报告自动化。

## 2. 二次定制点

| 定制点 | 文件 | 说明 |
| --- | --- | --- |
| 读者目标 | `bookmind/agents/domain_application_agent.py` | 在 `_GOAL_TEMPLATES` 中加新行业 |
| 概念合并 | `bookmind/agents/concept_agent.py` `_SYNONYM_GROUPS` | 接入自定义同义词库 |
| 报告模板 | `bookmind/templates/*.j2` | 改写为品牌风格 |
| 导出格式 | `bookmind/pipeline/export.py` | 增加新格式分支 |
| 模型接入 | `bookmind/agents/chapter_summary_agent.py` 等 | 注入外部 LLM provider |
| 缓存 | `bookmind/pipeline/cache.py` | 接入 Redis / S3 |

## 3. 模型接入

### OpenAI / Anthropic
- 在 `bookmind/llm/` 中新增 provider。
- 让 `ChapterSummaryAgent` 等 Agent 在 `_llm_available` 时优先调用模型；否则走启发式。
- 失败时自动 fallback。

### 私有模型
- 暴露一个 `BaseLLMProvider` 抽象。
- 部署在内部 GPU 服务器的模型通过 OpenAI 兼容 API 调用。

## 4. 多租户

- 建议把 `BOOKMIND_OUTPUT_DIR` 改为按用户划分：
  - `~/BookMind/reports/<user_id>/<book_id>/`
- 在 settings 中加 `multi_tenant` 开关。
- 把 `cache_dir` 也按用户隔离。

## 5. 监控

- 暴露 `ReviewAgent` 的 `quality_report` 分数。
- 设置阈值（建议 80 分），低于阈值时人工复核或自动重跑。
- 收集每本书的耗时、章节数、引用数，统计 SLA。

## 6. 计费

- 简化方案：按"本"计费。
- 精细方案：按页 / token / 章节数计费。
- BookMind 的 `BookInsight` 已经结构化，便于自动化计费。

## 7. 推荐部署架构

```
        ┌─────────────────┐
        │  Web/Mobile App │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │  API Gateway    │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │  Worker Pool    │  (BookMind)
        │  (Python Worker)│
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │  Object Storage │  (reports / cache)
        └─────────────────┘
```
