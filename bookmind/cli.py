"""BookMind CLI。

支持：
- analyze  : 深度解读 PDF
- ask      : 基于本书的问答
- export   : 重新导出某份 insight
- doctor   : 依赖与配置检查
- skills   : 列出/检查可分发的 Skills
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from . import __version__
from .config import get_settings
from .logging_config import configure_logging, get_logger
from .models import LanguageCode, Mode, ReadingRequest, READER_GOALS
from .orchestrator import Orchestrator

app = typer.Typer(add_completion=False, help="BookMind - 整本书深度解读多智能体")
console = Console()
log = get_logger("cli")


def _print_banner() -> None:
    console.print(f"[bold cyan]BookMind[/bold cyan] v{__version__} — 整本书深度解读多智能体", highlight=False)


@app.command()
def analyze(
    pdf: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="PDF 文件路径"),
    mode: Mode = typer.Option(Mode.DEEP, "--mode", "-m", help="阅读模式"),
    goal: str = typer.Option("通识理解", "--goal", "-g", help=f"读者目标: {READER_GOALS}"),
    language: LanguageCode = typer.Option(LanguageCode.ZH_CN, "--lang", help="输出语言"),
    export: List[str] = typer.Option(["markdown", "html", "json"], "--export", "-e", help="导出格式"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="输出目录"),
    max_quote: int = typer.Option(60, "--max-quote", help="每条引用最大字数"),
    enable_ocr: bool = typer.Option(False, "--ocr", help="启用 OCR"),
    no_cache: bool = typer.Option(False, "--no-cache", help="禁用缓存"),
) -> None:
    """深度解读一本 PDF 书。"""
    _print_banner()
    configure_logging()
    req = ReadingRequest(
        file_path=str(pdf),
        mode=mode,
        reader_goal=goal,
        output_language=language,
        export_formats=export,
        max_quote_words=max_quote,
        enable_ocr=enable_ocr,
        enable_cache=not no_cache,
        output_dir=str(out) if out else "",
    )
    orch = Orchestrator()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as p:
        p.add_task("正在解读 PDF…", total=None)
        result = orch.analyze(req)
    console.print("[bold green]✓ 完成[/bold green]")
    console.print(f"输出目录: {result['result'].get('output_dir', '-')}")
    console.print(f"质量分: {result['result'].get('quality_report', {}).get('score', '-')}")
    console.print(f"用时: {result['elapsed_sec']} s")


@app.command()
def ask(
    index: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="索引文件路径 (chunks.sqlite)"),
    question: str = typer.Argument(..., help="你的问题"),
) -> None:
    """基于整本书的问答（需要先 build_index）。"""
    _print_banner()
    orch = Orchestrator()
    out = orch.ask(str(index), question)
    console.print(out.get("answer", ""))
    if out.get("citations"):
        console.print("\n[dim]引用：[/dim]")
        for c in out["citations"][:5]:
            console.print(f"  - {c.get('label', c.get('chapter_title', ''))}")


@app.command()
def export(
    insight: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="*.insight.json"),
    fmt: str = typer.Option("html", "--fmt", help="导出格式: markdown/html/json/csv/anki/obsidian/mermaid"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="输出目录"),
) -> None:
    """重新导出某份 insight.json。"""
    _print_banner()
    orch = Orchestrator()
    p = orch.export(insight, fmt, out)
    console.print(f"[bold green]✓[/bold green] 已导出: {p}")


@app.command()
def doctor() -> None:
    """依赖与配置检查。"""
    _print_banner()
    orch = Orchestrator()
    info = orch.doctor()
    table = Table(title="依赖检查")
    table.add_column("依赖", style="cyan")
    table.add_column("状态", style="green")
    for name, status in info["deps"].items():
        table.add_row(name, str(status))
    console.print(table)
    console.print("\n[bold]配置：[/bold]")
    console.print(json.dumps(info.get("settings", {}), ensure_ascii=False, indent=2))
    if not info["ok"]:
        console.print("[red]✗ 部分必选依赖缺失[/red]")
        sys.exit(1)
    console.print("[green]✓[/green] BookMind 已就绪")


@app.command("skills")
def skills_cmd() -> None:
    """列出可分发的 Skills。"""
    from .skills_runtime.registry import discover_skills

    _print_banner()
    skills = discover_skills()
    table = Table(title="可分发的 Skills")
    table.add_column("Skill", style="cyan")
    table.add_column("版本")
    table.add_column("描述")
    for s in skills:
        table.add_row(s["name"], s.get("version", "-"), s.get("description", ""))
    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()