"""Shared pytest fixtures for BookMind tests."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Iterator

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture()
def tmp_workdir(monkeypatch) -> Iterator[Path]:
    d = Path(tempfile.mkdtemp(prefix="bookmind-test-"))
    monkeypatch.setenv("BOOKMIND_OUTPUT_DIR", str(d / "reports"))
    monkeypatch.setenv("BOOKMIND_CACHE_DIR", str(d / "cache"))
    monkeypatch.setenv("BOOKMIND_LOG_LEVEL", "WARNING")
    from bookmind import config

    config.reset_settings()
    yield d
    shutil.rmtree(d, ignore_errors=True)
