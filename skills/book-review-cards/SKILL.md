---
name: book-review-cards
description: Generate spaced-repetition review cards (basic, understanding, application, critical) from a parsed book, exportable to Anki CSV or Obsidian.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, srs, anki, learning]
    category: productivity
    requires_toolsets: [terminal]
---

# Book Review Cards

## When to Use
Use this skill to generate review cards for spaced repetition from a book's chapter insights.

## Procedure
1. Pull `book_insight.chapter_insights` and `concept_glossary`.
2. Generate basic / understanding / application / critical cards.
3. Export as Anki CSV.

## Safety
- Do not include copyrighted long quotes.
- Each card must include a citation when claiming a fact from the book.

## Example
```bash
python skills/book-review-cards/scripts/run_review_cards.py /path/to/book.pdf
```
