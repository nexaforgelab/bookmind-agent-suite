---
name: book-concept-map
description: Extract core concepts, merge synonyms, and produce a concept glossary with definitions, author usage, related concepts, and applications.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [pdf, concept, knowledge-graph]
    category: productivity
    requires_toolsets: [terminal]
---

# Book Concept Map

## When to Use
Use this skill to produce a glossary of core concepts from a parsed book.

## Procedure
1. Collect concept candidates from all chapter insights.
2. Cluster synonyms using a configurable synonym table.
3. Build a `Concept` entry per cluster.
4. Output JSON / Obsidian notes.

## Safety
- Concept definitions must be derived from the book, not invented.

## Failure Handling
- If fewer than 5 concepts are detected, return a warning and re-run with extended windows.

## Example
```bash
python skills/book-concept-map/scripts/run_concept_map.py /path/to/book.pdf
```
