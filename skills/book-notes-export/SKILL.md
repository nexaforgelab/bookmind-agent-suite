---
name: book-notes-export
description: Generate Markdown / Obsidian / Anki / CSV / HTML / JSON exports from a parsed book and its BookInsight.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, notes, obsidian, anki, export]
    category: productivity
    requires_toolsets: [terminal]
---

# Book Notes Export

## When to Use
Use this skill to produce downstream study / knowledge artifacts from a `book_insight.json`.

## Procedure
1. Validate the `book_insight.json` file.
2. Render Markdown report with citations.
3. Optionally render HTML / Anki CSV / Obsidian vault / Mermaid.
4. Return absolute paths.

## Safety
- Clip quotes to the configured `max_quote_words`.
- Write only into the configured output directory.

## Example
```bash
python skills/book-notes-export/scripts/run_notes_export.py /path/to/book.pdf --export markdown,obsidian,anki
```
