---
name: book-deep-reading
description: Deeply analyze a full PDF book with multi-agent reading workflow, including structure, chapter summaries, concepts, arguments, critical analysis, application plan, notes, mindmap, and export.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [book, pdf, reading, research, knowledge-management, python]
    category: productivity
    requires_toolsets: [terminal]
    config:
      - key: bookmind.output_dir
        description: Directory for generated book reports
        default: "~/BookMind/reports"
        prompt: "Where should BookMind save reports?"
      - key: bookmind.cache_dir
        description: Directory for cache and parsed PDF data
        default: "~/.bookmind/cache"
        prompt: "Where should BookMind cache parsed books?"
---

# Book Deep Reading

## When to Use
Use this skill when the user uploads or references a PDF book and asks for full-book reading, deep interpretation, chapter-by-chapter summary, concept extraction, reading notes, study cards, mindmap, or book Q&A.

## Procedure
1. Confirm the PDF path or locate the most recent uploaded PDF in the active workspace.
2. Ask for missing parameters only if essential. Otherwise default to:
   - mode: `deep`
   - reader_goal: `通识理解`
   - output_language: `zh-CN`
   - export_formats: `markdown,html,json`
3. Run the BookMind pipeline through `python -m bookmind.cli analyze`.
4. If the book is large, process chapter by chapter and save intermediate outputs.
5. Generate final report and return the report path.
6. If the user asks follow-up questions, use the generated index and citations.

## Inputs
- `file_path` (str, required): absolute path to the PDF
- `mode` (str, optional): `quick|standard|deep|expert`
- `goal` (str, optional): one of the predefined `reader_goal`s
- `output_language` (str, optional): `zh-CN|en-US`
- `export` (str, optional): comma-separated list, e.g. `markdown,html,json,obsidian,anki,mermaid`
- `enable_ocr` (bool, optional)
- `output_dir` (str, optional)

## Safety and Copyright
- Do not output large verbatim sections from copyrighted books.
- Summarize and analyze instead.
- Short quotations must be limited and include page citation.
- Never claim the book says something without chapter/page support.

## Verification
- Confirm parsed page count.
- Confirm chapter count.
- Confirm report files exist.
- Confirm `quality_report.json` has no blocking errors.

## Example
```bash
python -m bookmind.cli analyze /path/to/book.pdf \
  --mode deep \
  --goal 通识理解 \
  --export markdown,html,json,obsidian,anki,mermaid \
  --output-dir ~/BookMind/reports
```

## Failure Handling
- If the PDF is encrypted or unreadable, ask the user to provide a decrypted copy.
- If OCR is required but not installed, return a structured message and suggest installing `pytesseract` or `ocrmypdf`.
- If mode is `expert` and `quality_report.score < 80`, mark a warning at the top of the report.
