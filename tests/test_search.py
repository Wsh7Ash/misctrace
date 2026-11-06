"""
tests/test_search.py — search primitive tests.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from search import find_definition, find_references, search_symbol


def make_repo(files):
    root = Path(tempfile.mkdtemp(prefix="repo-"))
    for path, content in files.items():
        full = root / path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
    return root


def test_finds_python_definition():
    repo = make_repo({"a.py": "def handle():\n    pass\n\nhandle()\n"})
    defs = find_definition("handle", repo)
    assert len(defs) == 1
    assert defs[0].kind == "definition"
    assert "def handle" in defs[0].snippet


def test_finds_references_excludes_definition():
    repo = make_repo({"a.py": "def handle():\n    pass\n\nhandle()\n"})
    refs = find_references("handle", repo)
    assert all(r.kind == "reference" for r in refs)
    assert len(refs) >= 1


def test_search_symbol_returns_both():
    repo = make_repo({"a.py": "def handle():\n    pass\n\nhandle()\n"})
    r = search_symbol("handle", [repo])
    assert r.definitions
    assert r.references
