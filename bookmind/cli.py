"""BookMind CLI - Typer 实现。"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from .config import get_settings, reset_settings
from .exceptions import BookMindError
from .logging_config import configure_logging, get_logger
from .models import Mode, LanguageCode, ReadingRequest, READER_GOALS
from .orchestrator import Orchestrator

app = typer.Typer(
    name="bookmind",
    help="BookMind - 整本书深度解读多智能体 CLI",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()
log = get_logger("cli")


def _parse_list(s: str) -> List[str]:
    return [x.strip() for x in s.split(",") if x.strip()]


@app.command()
def analyze(
    file_path: str = typer.Argument(..., help="PDF 文件路径"),
    mode: Mode = typer.Option(Mode.DEEP, "--mode", "-m", help="quick / standard / deep / expert"),
    goal: str = typer.Option("通识理解", "--goal", "-g", help=f"读者目标，可选: {READER_GOALS}"),
    output_language: LanguageCode = typer.Option(LanguageCode.ZH_CN, "--output-language", "-l"),
    export: str = typer.Option("markdown,html,json", "--export", "-e", help="导出格式，逗号分隔"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o"),
    enable_ocr: bool = typer.Option(False, "--enable-ocr"),
    enable_cache: bool = typer.Option(True, "--enable-cache/--disable-cache"),
    max_quote_words: int = typer.Option(60, "--max-quote-words"),
):
    """分析一本 PDF 并输出深度解读报告。"""
    configure_logging()
    s = get_settings()
    out_dir = output_dir or s.output_dir
    request = ReadingRequest(
        file_path=file_path,
        mode=mode,
        reader_goal=goal,
        output_language=output_language,
        export_formats=_parse_list(export),
        max_quote_words=max_quote_words,
        enable_ocr=enable_ocr,
        enable_cache=enable_cache,
        output_dir=str(out_dir),
    )
    orch = Orchestrator()
    with console.status("[bold green]BookMind 正在解读整本书…[/bold green]"):
        try:
            result = orch.analyze(request)
        except BookMindError as e:
            console.print(Panel(str(e), title="错误", border_style="red"))
            raise typer.Exit(code=1)
    data = result.get("result", {})
    console.print(Panel.fit(
        f"[bold]书名：[/bold] {data.get('metadata', {}).get('title', '?')}\n"
        f"[bold]作者：[/bold] {data.get('metadata', {}).get('author') or '—'}\n"
        f"[bold]总页数：[/bold] {data.get('metadata', {}).get('total_pages', 0)}\n"
        f"[bold]模式：[/bold] {data.get('mode')}\n"
        f"[bold]输出目录：[/bold] {data.get('output_dir')}\n"
        f"[bold]耗时：[/bold] {result.get('elapsed_sec', 0)}s",
        title="解读完成",
        border_style="green",
    ))
    # 列出文件
    out = Path(data.get("output_dir", out_dir))
    if out.exists():
        tbl = Table(title="生成文件", show_lines=False)
        tbl.add_column("文件")
        for p in sorted(out.glob("*")):
            tbl.add_row(str(p))
        console.print(tbl)
    console.print(f"\n[bold]报告路径：[/bold]{data.get('output_dir')}")


@app.command()
def ask(
    index_path: str = typer.Argument(..., help="index.sqlite 路径"),
    question: str = typer.Argument(..., help="问题"),
    top_k: int = typer.Option(5, "--top-k"),
):
    """基于已建好的索引进行问答。"""
    configure_logging()
    orch = Orchestrator()
    result = orch.ask(index_path, question)
    if not result["success"]:
        console.print(Panel(result.get("answer", "失败"), border_style="red"))
        raise typer.Exit(code=1)
    console.print(Panel(result["answer"], title="答案", border_style="cyan"))
    if result.get("citations"):
        console.print(JSON(json.dumps(result["citations"], ensure_ascii=False, indent=2)))


@app.command()
def export(
    insight_path: Path = typer.Argument(..., help="book_insight.json 路径"),
    format: str = typer.Option("markdown", "--format", "-f", help="markdown / html / json / csv / anki / obsidian / mermaid / pdf"),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
):
    """把 BookInsight 导出为指定格式。"""
    configure_logging()
    orch = Orchestrator()
    out = out_dir or get_settings().output_dir
    p = orch.export(insight_path, format, out)
    console.print(f"[green]已导出：[/green] {p}")


@app.command()
def doctor():
    """依赖与配置健康检查。"""
    configure_logging()
    orch = Orchestrator()
    res = orch.doctor()
    tbl = Table(title="依赖检查", show_lines=False)
    tbl.add_column("模块", style="bold")
    tbl.add_column("状态")
    for k, v in res["deps"].items():
        color = "green" if v == "ok" else ("yellow" if "optional" in v else "red")
        tbl.add_row(k, f"[{color}]{v}[/{color}]")
    console.print(tbl)
    console.print(Panel(JSON(json.dumps(res.get("settings", {}), ensure_ascii=False, indent=2)), title="配置"))


@app.command()
def clean_cache(
    yes: bool = typer.Option(False, "--yes", "-y", help="跳过确认"),
):
    """清理解析缓存。"""
    configure_logging()
    s = get_settings()
    if not yes and not typer.confirm(f"确认清空 {s.cache_dir} ?", default=False):
        raise typer.Abort()
    shutil.rmtree(s.cache_dir, ignore_errors=True)
    s.ensure_dirs()
    console.print(f"[green]已清空：[/green] {s.cache_dir}")


@app.command()
def doctor_doctor():  # pragma: no cover - 兼容别名
    doctor()


if __name__ == "__main__":
    app()
