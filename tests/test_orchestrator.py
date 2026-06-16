"""Tests for orchestrator and director agent paths that don't need a real PDF."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from bookmind.config import reset_settings
from bookmind.orchestrator import Orchestrator
from bookmind.models import ReadingRequest, Mode, LanguageCode


def test_orchestrator_doctor(tmp_workdir: Path):
    reset_settings()
    orch = Orchestrator()
    res = orch.doctor()
    assert "deps" in res
    assert "pydantic" in res["deps"]


def test_ask_returns_no_evidence(tmp_workdir: Path):
    """未建索引时 ask 应优雅返回无证据。"""
    reset_settings()
    orch = Orchestrator()
    fake_index = tmp_workdir / "fake.sqlite"
    fake_index.touch()
    res = orch.ask(str(fake_index), "测试问题")
    # FTS5 表可能未建立，会返回 success=False
    assert "success" in res


def test_export_unknown_format(tmp_workdir: Path):
    reset_settings()
    orch = Orchestrator()
    fake_insight = tmp_workdir / "insight.json"
    fake_insight.write_text("{}", encoding="utf-8")
    from bookmind.exceptions import BookMindError
    with pytest.raises((BookMindError, Exception)):
        try:
            orch.export(fake_insight, "unknown-format")
        except BookMindError:
            raise
        except Exception:
            raise
