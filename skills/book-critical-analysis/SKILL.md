---
name: book-critical-analysis
description: Critically analyze a book's arguments, identify strengths, weaknesses, hidden assumptions, and provide constructive counter-points grounded in the text.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, critical-thinking, analysis]
    category: productivity
    requires_toolsets: [terminal]
---

# Book Critical Analysis

## When to Use
Use this skill to evaluate the strength of the author's arguments.

## Procedure
1. Extract argument chains from the `book_insight`.
2. For each claim, identify evidence, examples, hidden assumptions.
3. Mark each as `strong / weak / outdated / context-dependent`.
4. Suggest counter-points grounded in the text.

## Safety
- Avoid attacking the author personally.
- Base every critique on textual evidence.

## Failure Handling
- If arguments are not extractable, return an empty critical list and a clear warning.

## Example
```bash
python skills/book-critical-analysis/scripts/run_critical_analysis.py /path/to/book.pdf --mode expert
```
