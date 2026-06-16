---
name: book-qa
description: Ask questions about a book. Uses FTS5 + chapter/page citations. Returns "I don't know" when the book has no relevant evidence.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, qa, knowledge-management]
    category: productivity
    requires_toolsets: [terminal]
---

# Book QA

## When to Use
Use this skill to ask a question about a book whose index has been built (`chunks.sqlite`).

## Procedure
1. Run FTS5 query against the book index.
2. Return up to 5 evidence snippets with chapter/page labels.
3. If no results, return a clear "no evidence" message.

## Safety
- Do not hallucinate answers.
- Always include citations for any claim.

## Failure Handling
- If the index is missing, ask the user to run `book-deep-reading` first to build the index.

## Example
```bash
python skills/book-qa/scripts/run_qa.py /path/to/index.sqlite "作者的核心观点是什么？"
```
