"""
tests/test_trace.py — trace construction tests.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from search import find_definition
from trace import build_trace


def make_repo(files):
    root = Path(tempfile.mkdtemp(prefix="repo-"))
    for path, content in files.items():
        full = root / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
    return root


def test_resolved_when_both_defined_and_cooccur():
    repo = make_repo({"a.py": "def start():\n    pass\n\ndef target():\n    pass\n"})
    trace = build_trace("start", "target", [repo])
    assert trace.resolved is True
    assert any(h.symbol == "start->target" and h.status == "found" for h in trace.hops)


def test_unresolved_when_target_missing():
    repo = make_repo({"a.py": "def start():\n    pass\n"})
    trace = build_trace("start", "target", [repo])
    assert trace.resolved is False
    assert any(h.status == "missing" for h in trace.hops)


def test_start_definition_locations_present():
    repo = make_repo({"a.py": "def start():\n    pass\n"})
    defs = find_definition("start", repo)
    assert defs
