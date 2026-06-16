---
name: book-chapter-summarize
description: Generate per-chapter insights including one-sentence summary, key points, concepts, examples, argument chain, follow-up questions, and page citations.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, reading, summary, knowledge-management]
    category: productivity
    requires_toolsets: [terminal]
---

# Book Chapter Summarize

## When to Use
Use this skill to drill into each chapter of a parsed book, producing a `ChapterInsight` per chapter.

## Procedure
1. Ingest & segment chapters.
2. For each chapter: extract sentences, score key points, identify concepts, find examples, build argument chain, generate follow-up questions.
3. Persist results to `book_insight.json`.

## Safety
- Short quotes only; respect `max_quote_words`.
- All claims must include chapter or page citations.

## Failure Handling
- If a chapter text is empty, skip and emit a warning.
- If score is low for a chapter, mark it for re-run in the `quality_report`.

## Example
```bash
python skills/book-chapter-summarize/scripts/run_chapter_summarize.py /path/to/book.pdf
```
